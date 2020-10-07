import networkx as nx
from hypotheses.sign_tests import *


# input: matrix of correlations, list of ticks of stocks
# output: MST
def create_Kruskal_MST(cor, stocks):
    dict_edges = []
    for i in range(len(stocks)):
        for j in range(i + 1, len(stocks)):
            dict_edges.append((cor[i][j], stocks[i], stocks[j]))

    dict_edges.sort(key=lambda i: i[0], reverse=True)
    # print(dict_edges)
    G = nx.Graph()
    G.add_edge(dict_edges[0][1], dict_edges[0][2])

    for edge in dict_edges:
        if (edge[2] not in G.nodes()) or (
                edge[2] in G.nodes() and edge[1] not in nx.node_connected_component(G, edge[2])):
            # print(i[1], ' ', i[2])
            G.add_edge(edge[1], edge[2], weight=edge[0])
        if len(list(G.nodes)) == len(stocks) and nx.is_connected(G):
            return G

    print('Error Kruskal')


class Pair:
    def __init__(self, stock_1, stock_2, i, j, test_3, test_4, ret_inds, alpha):
        self.stock_1 = stock_1
        self.stock_2 = stock_2
        self.i = i
        self.j = j
        self.test_3 = test_3
        self.test_4 = test_4
        self.ret_inds = ret_inds
        self.alpha = alpha

    def comparator(a, b):
        inter = set([a.i, a.j]) & set([b.i, b.j])
        aa = list(set([a.i, a.j]) - inter)
        bb = list(set([b.i, b.j]) - inter)
        if len(inter) == 0:
            return a.test_4(a.i, a.j, b.i, b.j, a.ret_inds, a.alpha)
        else:
            inter = list(inter)[0]
            return a.test_3(inter, aa, bb, a.ret_inds, a.alpha)

# input: matrix of correlations, list of ticks of stocks
# output: MST
def create_Kruskal_hypot_MST(ret_inds, stocks, alpha=0.05, kind_of_test='simple'):
    if kind_of_test == 'simple':
        test_3 = test_ijk
        test_4 = test_ijkl
    elif kind_of_test == 'complex_rand':
        test_3 = complex_rand_test_ijk
        test_4 = complex_rand_test_ijkl
    elif kind_of_test == 'complex_max':
        test_3 = complex_max_test_ijk
        test_4 = complex_max_test_ijkl

    dict_edges = []
    for i in range(len(stocks)):
        for j in range(i + 1, len(stocks)):

            dict_edges.append((stocks[i], stocks[j], i, j))

    dict_edges.sort(cmp=cmp())
    G = nx.Graph()
    G.add_edge(dict_edges[0][1], dict_edges[0][2])

    for edge in dict_edges:
        if (edge[2] not in G.nodes()) or (
                edge[2] in G.nodes() and edge[1] not in nx.node_connected_component(G, edge[2])):
            G.add_edge(edge[1], edge[2], weight=edge[0])
        if len(list(G.nodes)) == len(stocks) and nx.is_connected(G):
            return G

    print('Error Kruskal')

