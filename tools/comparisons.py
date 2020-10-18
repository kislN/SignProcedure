import numpy as np
import plotly.graph_objs as go
import pandas as pd
from tqdm import tqdm

from tools.data_transform import *
from algorithms.Kruskal import create_Kruskal_MST, create_Kruskal_hypot_MST
from algorithms.Prim import *
from hypotheses.sign_tests import Test
from distributions.multivariate_normal import norm_seq
from distributions.multivariate_t import student_seq, t_seq


def count_rate_proc(ref_MST, ref_corr, observ_num, stocks, iters=1000, measure='pearson', distr='normal', dof=1, rate=0.5):
    counter = 0
    ref_degrees = sorted(ref_MST.degree)
    if distr == 'mix':
        rate_list = np.random.choice([0, 1], p=[1 - rate, rate], size=iters)

    for itr in tqdm(range(iters)):

        if distr == 'normal':
            new_rets = norm_seq(ref_corr, observ_num)
        elif distr == 'student':
            new_rets = t_seq(ref_corr, dof, observ_num)
        elif distr == 'mix':
            if rate_list[itr] == 1:
                new_rets = norm_seq(ref_corr, observ_num)
            else:
                new_rets = t_seq(ref_corr, dof, observ_num)

        if measure == 'pearson':
            new_corr = np.corrcoef(new_rets)
        elif measure == 'sign':
            new_inds = indicators(new_rets)
            new_corr = get_sign_matrix(new_inds)

        G1 = create_Kruskal_MST(new_corr, stocks)
        # G2 = create_Prim_MST(new_corr, stocks) # for testing both algorithms
        new_degrees = sorted(G1.degree)

        # if new_degrees != sorted(G2.degree):
        #     return -1
        if ref_degrees == new_degrees:
            counter += 1
    return counter/iters


def count_rate_test(ref_MST, ref_corr, observ_num, stocks, iters=1000, one_sided=True, kind='not_rand', distr='normal',
                    dof=1, alphas=[0.1], rate=0.5):
    counter_prim = 0
    counter_kruskal = 0
    ref_degrees = sorted(ref_MST.degree)
    if distr == 'mix':
        rate_list = np.random.choice([0, 1], p=[1 - rate, rate], size=iters)

    dict_alpha = {}
    for alpha in alphas:
        for itr in tqdm(range(iters)):

            if distr == 'normal':
                new_rets = norm_seq(ref_corr, observ_num)
            elif distr == 'student':
                new_rets = t_seq(ref_corr, dof, observ_num)
            elif distr == 'mix':
                if rate_list[itr] == 1:
                    new_rets = norm_seq(ref_corr, observ_num)
                else:
                    new_rets = t_seq(ref_corr, dof, observ_num)

            new_inds = indicators(new_rets)
            G_Prim = create_Prim_hypot_MST(new_inds, stocks, alpha, one_sided, kind)
            G_Kruskal = create_Kruskal_hypot_MST(new_inds, stocks, alpha, one_sided, kind)

            if ref_degrees == sorted(G_Prim.degree):
                counter_prim += 1
            if ref_degrees == sorted(G_Kruskal.degree):
                counter_kruskal += 1
        dict_alpha[str(alpha) + '_alpha'] = {'Prim': counter_prim/iters, 'Kruskal': counter_kruskal/iters}

    return dict_alpha


def compare_norm(ref_MST, ref_corr, stocks, observ_num=[20], iters=1000, alphas=[0.1]):
    dict_obs = {}
    for observ in observ_num:
        dict_rates = {}
        dict_rates['pearson'] = count_rate_proc(ref_MST, ref_corr, observ, stocks, iters, measure='pearson',
                                                distr='normal')
        dict_rates['sign'] = count_rate_proc(ref_MST, ref_corr, observ, stocks, iters, measure='pearson',
                                             distr='normal')

        dict_rates['oneSided_notRand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=True,
                                                         kind='not_rand', distr='normal', alphas=alphas)
        dict_rates['oneSided_rand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=True,
                                                         kind='rand', distr='normal', alphas=alphas)
        dict_rates['oneSided_max'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=True,
                                                      kind='max', distr='normal', alphas=alphas)
        dict_rates['twoSided_rand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=False,
                                                      kind='rand', distr='normal', alphas=alphas)
        dict_rates['twoSided_max'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=False,
                                                      kind='max', distr='normal', alphas=alphas)

        dict_obs[str(observ) + '_obs'] = dict_rates

    return dict_obs


def compare_stud(ref_MST, ref_corr, stocks, observ_num=[20], iters=1000, alphas=[0.1], dofs=[2]):
    dict_obs = {}
    for observ in observ_num:
        dict_dof = {}
        for dof in dofs:
            dict_rates = {}
            dict_rates['pearson'] = count_rate_proc(ref_MST, ref_corr, observ, stocks, iters, measure='pearson',
                                                    distr='student', dof=dof)
            dict_rates['sign'] = count_rate_proc(ref_MST, ref_corr, observ, stocks, iters, measure='pearson',
                                                 distr='student', dof=dof)

            dict_rates['oneSided_notRand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=True,
                                                             kind='not_rand', distr='student', dof=dof, alphas=alphas)
            dict_rates['oneSided_rand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=True,
                                                          kind='rand', distr='student', dof=dof, alphas=alphas)
            dict_rates['oneSided_max'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=True,
                                                         kind='max', distr='student', dof=dof, alphas=alphas)
            dict_rates['twoSided_rand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=False,
                                                          kind='rand', distr='student', dof=dof, alphas=alphas)
            dict_rates['twoSided_max'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters, one_sided=False,
                                                         kind='max', distr='student', dof=dof, alphas=alphas)
            dict_dof[str(dof) + '_dof'] = dict_rates

        dict_obs[str(observ) + '_obs'] = dict_dof

    return dict_obs


def compare_mix(ref_MST, ref_corr, stocks, observ_num=[20], iters=1000, alphas=[0.1], dofs=[2], norm_rates=[0.5]):
    dict_obs = {}
    for observ in observ_num:
        dict_norm_rate = {}
        for norm_rate in norm_rates:
            dict_dof = {}
            for dof in dofs:
                dict_rates = {}
                dict_rates['pearson'] = count_rate_proc(ref_MST, ref_corr, observ, stocks, iters, measure='pearson',
                                                        distr='student', dof=dof)
                dict_rates['sign'] = count_rate_proc(ref_MST, ref_corr, observ, stocks, iters, measure='pearson',
                                                     distr='student', dof=dof)

                dict_rates['oneSided_notRand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters,
                                                                 one_sided=True, kind='not_rand', distr='student',
                                                                 dof=dof, alphas=alphas, rate=norm_rate)
                dict_rates['oneSided_rand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters,
                                                              one_sided=True, kind='rand', distr='student',
                                                              dof=dof, alphas=alphas, rate=norm_rate)
                dict_rates['oneSided_max'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters,
                                                             one_sided=True, kind='max', distr='student',
                                                             dof=dof, alphas=alphas, rate=norm_rate)
                dict_rates['twoSided_rand'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters,
                                                              one_sided=False, kind='rand', distr='student',
                                                              dof=dof, alphas=alphas, rate=norm_rate)
                dict_rates['twoSided_max'] = count_rate_test(ref_MST, ref_corr, observ, stocks, iters,
                                                             one_sided=False, kind='max', distr='student',
                                                             dof=dof, alphas=alphas, rate=norm_rate)
                dict_dof[str(dof) + '_dof'] = dict_rates

            dict_norm_rate[str(norm_rate) + '_nRate'] = dict_dof

        dict_obs[str(observ) + '_obs'] = dict_norm_rate

    return dict_obs







def compare_procedures(corr, stcks, ref_MST, iters=1000, alphas=[0.2, 0.15, 0.1, 0.05], seq_nums=[100]):
    for alpha in alphas:
        print('alpha = ', alpha)
        for seq_num in seq_nums:
            count_corr = 0
            count_simple = 0
            count_compl_rand = 0
            count_compl_max = 0
            for iter in range(iters):
                new_rets = norm_seq(corr, seq_num)
                new_inds = indicators(new_rets)
                G_corr = create_Prim_MST(np.corrcoef(new_rets), stcks)
                G_hypoth = create_Prim_hypot_MST(new_inds, stcks, alpha)
                G_compl_rand = create_Prim_hypot_MST(new_inds, stcks, alpha, kind_of_test='complex_rand')
                G_compl_max = create_Prim_hypot_MST(new_inds, stcks, alpha, kind_of_test='complex_max')
                if sorted(ref_MST.degree) == sorted(G_corr.degree):
                    count_corr += 1
                if sorted(ref_MST.degree) == sorted(G_hypoth.degree):
                    count_simple += 1
                if sorted(ref_MST.degree) == sorted(G_compl_rand.degree):
                    count_compl_rand += 1
                if sorted(ref_MST.degree) == sorted(G_compl_max.degree):
                    count_compl_max += 1

            print('observations number = {} \n \
      rate of the same: \n \
      procedure of correlation: {} \n \
      simple hypothetical procedure: {} \n \
      complex (rand) hypothetical procedure: {} \n \
      complex (max) hypothetical procedure: {}'.format(seq_num, \
                                                       count_corr / iters, \
                                                       count_simple / iters, \
                                                       count_compl_rand / iters, \
                                                       count_compl_max / iters))

"""temporarily here"""


def draw_rates(data_x, data_y, alpha, corr, stocks, title, title_x='x', title_y='y'):
    # title_matrix = 'corr matrix:<br> __'
    print('Correlations matrix:')
    for row in corr:
        print(row)
    title_matrix = 'матрица корреляций:<br>'
    # for st in stocks:
        # title_matrix += st + '__'
    # title_matrix += '<br>'
    for i, c in enumerate(corr):
        # title_matrix += str(stocks[i]) + ' ' + str(c) + '<br>'
        title_matrix += str(c) + '<br>'

    fig = go.Figure(layout={'title': {'text': title,
                                      'y': 0.87,
                                      'x': 0.075,
                                      'xanchor': 'left',
                                      'yanchor': 'top'
                                      },
                            'font': {'size': 15, 'family': 'Courier'},
                            'template': 'seaborn'})
    for i in range(len(alpha)):
        fig.add_trace(go.Bar(name='alpha = ' + str(alpha[i]), x=data_x, y=data_y[i]))
    fig.update_xaxes(title_text=title_x)
    fig.update_yaxes(title_text=title_y)
    fig.update_layout(
        annotations=[
            dict(
                x=1.3,
                y=0.6,
                showarrow=False,
                text=title_matrix,
                xref="paper",
                yref="paper"
            ),
        ],
    )

    fig.show()


def test_rates(corr, stocks, one_sided=True, kind='not_rand', seq_num_list=np.arange(20, 200, 20),
               alpha_list=[0.1, 0.05, 0.01], iters=1000, title='', title_x='', title_y=''):

    if one_sided:
        method_name = 'one_sided'
    else:
        method_name = 'two_sided'

    if len(corr) == 3:
        compared_list = [0, 1, 2]
    elif len(corr) == 4:
        compared_list = [0, 1, 2, 3]
    else:
        print('Wrong matrix side')
        return

    rate_list = []
    for i, alpha in enumerate(alpha_list):
        print('alpha = ', alpha)
        rate_list.append([])
        for seq_num in seq_num_list:
            count = 0
            for j in range(iters):
                new_rets = norm_seq(corr, seq_num)
                new_inds = indicators(new_rets)
                test = Test(alpha, new_inds)
                count += getattr(test, method_name)(compared_list, kind)
            rate_list[i].append(count/iters)

    draw_rates(seq_num_list, rate_list, alpha_list, corr, stocks, f'{title}, {method_name}, {kind}', title_x, title_y + str(iters))
