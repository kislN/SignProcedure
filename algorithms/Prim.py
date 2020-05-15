import networkx as nx
from hypotheses.tests import *

# input: matrix of correlations, list of tickers of stocks
# output: MST
def create_Prim_MST(coef_matrix, stocks):
    G = nx.Graph()
    G.add_node(stocks[0])
    vert_i = 0
    vert_j = 0

    while len(G.nodes) < len(stocks):
        max_ij = []
        for stock_i in G.nodes:
            vert_i = stocks.index(stock_i)
            vert_j = vert_i
            for j in range(len(stocks)):
                if stocks[j] not in G.nodes and stocks[j] != stock_i:
                    vert_j = j
                    for k in range(j + 1, len(stocks)):
                        if stocks[k] not in G.nodes and stocks[k] != stock_i:
                            if coef_matrix[vert_i][vert_j] < coef_matrix[vert_i][k]:
                                vert_j = k
                    break
            if vert_i != vert_j:
                max_ij.append((vert_i, vert_j))

        if len(max_ij) != 0:

            vert_i = max_ij[0][0]
            vert_j = max_ij[0][1]

            for itr in range(1, len(max_ij)):
                if coef_matrix[vert_i][vert_j] < coef_matrix[max_ij[itr][0]][max_ij[itr][1]]:
                    vert_i = max_ij[itr][0]
                    vert_j = max_ij[itr][1]

            G.add_edge(stocks[vert_i], stocks[vert_j])
    return G

# input: matrix of returns of stocks, list of tickers of stocks, alpha for test, kind of test
# params: we can put the parameter kind_of_test as 'simple', 'complex_rand' or 'complex_max'
# output: MST
def create_Prim_hypot_MST(ret_inds, stocks, alpha=0.05, kind_of_test='simple'):
    if kind_of_test == 'simple':
        test_3 = test_ijk
        test_4 = test_ijkl
    elif kind_of_test == 'complex_rand':
        test_3 = complex_rand_test_ijk
        test_4 = complex_rand_test_ijkl
    elif kind_of_test == 'complex_max':
        test_3 = complex_max_test_ijk
        test_4 = complex_max_test_ijkl

    G = nx.Graph()
    G.add_node(stocks[0])
    vert_i = 0
    vert_j = 0

    while len(G.nodes) < len(stocks):
        max_ij = []
        for stock_i in G.nodes:
            vert_i = stocks.index(stock_i)
            vert_j = vert_i
            for j in range(len(stocks)):
                if stocks[j] not in G.nodes and stocks[j] != stock_i:
                    vert_j = j
                    for k in range(j + 1, len(stocks)):
                        if stocks[k] not in G.nodes and stocks[k] != stock_i:
                            if test_3(vert_i, vert_j, k, ret_inds, alpha) != 1:
                                vert_j = k
                    break
            if vert_i != vert_j:
                max_ij.append((vert_i, vert_j))

        # print('max_ij: ', max_ij)

        if len(max_ij) != 0:

            vert_i = max_ij[0][0]
            vert_j = max_ij[0][1]

            for itr in range(1, len(max_ij)):

                if vert_i == max_ij[itr][0]:  # тупой костыль, потом переделаю
                    if test_3(vert_i, vert_j, max_ij[itr][1], ret_inds, alpha) != 1:
                        vert_j = max_ij[itr][1]

                elif vert_i == max_ij[itr][1]:
                    if test_3(vert_i, vert_j, max_ij[itr][0], ret_inds, alpha) != 1:
                        vert_j = max_ij[itr][0]

                elif vert_j == max_ij[itr][0]:
                    if test_3(vert_j, vert_i, max_ij[itr][1], ret_inds, alpha) != 1:
                        vert_i = max_ij[itr][1]

                elif vert_j == max_ij[itr][1]:
                    if test_3(vert_j, vert_i, max_ij[itr][0], ret_inds, alpha) != 1:
                        vert_i = max_ij[itr][0]

                else:
                    if test_4(vert_i, vert_j, max_ij[itr][0], max_ij[itr][1], ret_inds, alpha) != 1:
                        vert_i = max_ij[itr][0]
                        vert_j = max_ij[itr][1]
            # print('take edge {}-{}'.format(stocks[vert_i], stocks[vert_j]))
            G.add_edge(stocks[vert_i], stocks[vert_j])
    return G

