import numpy as np
from tools.data_transform import *
from algorithms.Kruskal import create_Kruskal_MST
from algorithms.Prim import *

def compare_MSTs(ref_MST, ref_corr, observ_num, stocks, iters=1000):
  counter = 0
  ref_degrees = sorted(ref_MST.degree)

  for itr in range(iters):
    new_rets = get_norm_seq(ref_corr, observ_num)
    new_corr = np.corrcoef(new_rets)

    G1 = create_Kruskal_MST(new_corr, stocks)
    G2 = create_Prim_hypot_MST(new_corr, stocks) # for testing both algorithms

    new_degrees = sorted(G1.degree)

    if new_degrees != sorted(G2.degree):
      return -1

    if ref_degrees == new_degrees:
        counter += 1

  return counter/iters


# def compare_procedures(ref_MST, iters=1000, alphas=[0.2, 0.15, 0.1, 0.05], seq_nums=[100]):
#     for alpha in alphas:
#         print('alpha = ', alpha)
#         for seq_num in seq_nums:
#             count_corr = 0
#             count_simple = 0
#             count_compl_rand = 0
#             count_compl_max = 0
#             for iter in range(iters):
#                 new_rets = get_norm_seq(corr, seq_num)
#                 new_inds = get_inds_matrix(new_rets)
#                 G_corr = create_Prima_MST(np.corrcoef(new_rets), stcks)
#                 G_hypoth = create_hypot_MST(new_inds, stcks, alpha)
#                 G_compl_rand = create_hypot_MST(new_inds, stcks, alpha, kind_of_test='complex_rand')
#                 G_compl_max = create_hypot_MST(new_inds, stcks, alpha, kind_of_test='complex_max')
#                 if sorted(ref_MST.degree) == sorted(G_corr.degree):
#                     count_corr += 1
#                 if sorted(ref_MST.degree) == sorted(G_hypoth.degree):
#                     count_simple += 1
#                 if sorted(ref_MST.degree) == sorted(G_compl_rand.degree):
#                     count_compl_rand += 1
#                 if sorted(ref_MST.degree) == sorted(G_compl_max.degree):
#                     count_compl_max += 1
#
#             print('observations number = {} \n \
#       rate of the same: \n \
#       procedure of correlation: {} \n \
#       simple hypothetical procedure: {} \n \
#       complex (rand) hypothetical procedure: {} \n \
#       complex (max) hypothetical procedure: {}'.format(seq_num, \
#                                                        count_corr / iters, \
#                                                        count_simple / iters, \
#                                                        count_compl_rand / iters, \
#                                                        count_compl_max / iters))

"""temporarily here"""

# def draw_rates(data_x, data_y, alpha, corr, stocks, title, title_x='x', title_y='y'):
#     # title_matrix = 'corr matrix:<br> __'
#     title_matrix = title + ' при заданной матрице корреляции:<br> __'
#     for st in stocks:
#         title_matrix += st + '__'
#     title_matrix += '<br>'
#     for i, c in enumerate(corr):
#         title_matrix += str(stocks[i]) + ' ' + str(c) + '<br>'
#
#     fig = go.Figure(layout={'title': {'text': title_matrix,
#                                       'y': 0.95,
#                                       'x': 0.075,
#                                       'xanchor': 'left',
#                                       'yanchor': 'top'},
#                             'font': {'size': 15, 'family': 'Courier'},
#                             'template': 'plotly_dark'})
#
#     for i in range(len(alpha)):
#         fig.add_trace(go.Bar(name='alpha = ' + str(alpha[i]), x=data_x, y=data_y[i]))
#
#     fig.update_xaxes(title_text=title_x)
#     fig.update_yaxes(title_text=title_y)
#
#     fig.show()
#
# def test_rates(corr, stocks, kind_of_test, seq_num_list=np.arange(20, 200, 20), alpha_list=[0.1, 0.05, 0.01], iters=1000, title='', title_x='', title_y=''):
#
#   if kind_of_test == 'simple':
#     test_3 = test_ijk
#     test_4 = test_ijkl
#   elif kind_of_test == 'complex_rand':
#     test_3 = complex_rand_test_ijk
#     test_4 = complex_rand_test_ijkl
#   elif kind_of_test == 'complex_max':
#     test_3 = complex_max_test_ijk
#     test_4 = complex_max_test_ijkl
#
#   rate_list = []
#
#   for i, alpha in enumerate(alpha_list):
#     print('alpha = ', alpha)
#     rate_list.append([])
#     for seq_num in seq_num_list:
#       count = 0
#
#       for j in range(iters):
#         new_rets = get_norm_seq(corr, seq_num)
#         new_inds = get_inds_matrix(new_rets)
#         if (len(corr) == 3):
#           count += test_3(0, 1, 2, new_inds, alpha)
#         else:
#           count += test_4(0, 1, 2, 3, new_inds, alpha)
#
#       rate_list[i].append(count/iters)
#
#   draw_rates(seq_num_list, rate_list, alpha_list, corr, stocks, title, title_x, title_y)