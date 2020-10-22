import networkx as nx
from hypotheses.sign_tests import *


def create_Prim_MST(corr, stocks):
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
                            if corr[vert_i][vert_j] < corr[vert_i][k]:
                                vert_j = k
                    break
            if vert_i != vert_j:
                max_ij.append((vert_i, vert_j))

        if len(max_ij) != 0:
            vert_i = max_ij[0][0]
            vert_j = max_ij[0][1]

            for itr in range(1, len(max_ij)):
                if corr[vert_i][vert_j] < corr[max_ij[itr][0]][max_ij[itr][1]]:
                    vert_i = max_ij[itr][0]
                    vert_j = max_ij[itr][1]

            G.add_edge(stocks[vert_i], stocks[vert_j])
    return G


def create_Prim_hypot_MST(ret_inds, stocks, alpha=0.05, one_sided=True, kind='not_rand'):
    if one_sided:
        method_name = 'one_sided'
    else:
        method_name = 'two_sided'

    test = Test(alpha, ret_inds)

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
                            if getattr(test, method_name)([vert_i, vert_j, k], kind) != 1:
                            # if test_3(vert_i, vert_j, k, ret_inds, alpha) != 1:
                                vert_j = k
                    break
            if vert_i != vert_j:
                max_ij.append((vert_i, vert_j))

        if len(max_ij) != 0:

            vert_i = max_ij[0][0]
            vert_j = max_ij[0][1]

            for itr in range(1, len(max_ij)):

                if vert_i == max_ij[itr][0]:
                    if getattr(test, method_name)([vert_i, vert_j, max_ij[itr][1]], kind) != 1:
                    # if test_3(vert_i, vert_j, max_ij[itr][1], ret_inds, alpha) != 1:
                        vert_j = max_ij[itr][1]

                elif vert_i == max_ij[itr][1]:
                    if getattr(test, method_name)([vert_i, vert_j, max_ij[itr][0]], kind) != 1:
                    # if test_3(vert_i, vert_j, max_ij[itr][0], ret_inds, alpha) != 1:
                        vert_j = max_ij[itr][0]

                elif vert_j == max_ij[itr][0]:
                    if getattr(test, method_name)([vert_j, vert_i, max_ij[itr][1]], kind) != 1:
                    # if test_3(vert_j, vert_i, max_ij[itr][1], ret_inds, alpha) != 1:
                        vert_i = max_ij[itr][1]

                elif vert_j == max_ij[itr][1]:
                    if getattr(test, method_name)([vert_j, vert_i, max_ij[itr][0]], kind) != 1:
                    # if test_3(vert_j, vert_i, max_ij[itr][0], ret_inds, alpha) != 1:
                        vert_i = max_ij[itr][0]

                else:
                    if getattr(test, method_name)([vert_i, vert_j, max_ij[itr][0], max_ij[itr][1]], kind) != 1:
                    # if test_4(vert_i, vert_j, max_ij[itr][0], max_ij[itr][1], ret_inds, alpha) != 1:
                        vert_i = max_ij[itr][0]
                        vert_j = max_ij[itr][1]
            # print('take edge {}-{}'.format(stocks[vert_i], stocks[vert_j]))
            G.add_edge(stocks[vert_i], stocks[vert_j])
    return G

