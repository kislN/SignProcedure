import networkx as nx
from functools import cmp_to_key
from hypotheses.sign_tests import *
from distributions.multivariate_normal import norm_seq
from tools.data_transform import *


def create_Kruskal_MST(corr, stocks):
    dict_edges = []
    for i in range(len(stocks)):
        for j in range(i + 1, len(stocks)):
            dict_edges.append((corr[i][j], stocks[i], stocks[j]))

    dict_edges.sort(key=lambda i: i[0], reverse=True)
    G = nx.Graph()
    G.add_edge(dict_edges[0][1], dict_edges[0][2])

    for edge in dict_edges:
        if (edge[2] not in G.nodes()) or (
                edge[2] in G.nodes() and edge[1] not in nx.node_connected_component(G, edge[2])):
            G.add_edge(edge[1], edge[2], weight=edge[0])
        if len(list(G.nodes)) == len(stocks) and nx.is_connected(G):
            return G

    print('Error Kruskal')


def edges(stocks):
    N = len(stocks)
    list_edges = []
    for i in range(N):
        for j in range(i + 1, N):
            list_edges.append((i, j))
    return list_edges


class EdgeComparator:
    def __init__(self, ret_inds, alpha, one_sided, kind):
        if one_sided:
            self.method_name = 'one_sided'
        else:
            self.method_name = 'two_sided'
        self.kind = kind
        self.test = Test(alpha, ret_inds)

    def comparator(self, a, b):
        compared_list = list(set(a + b))
        t = getattr(self.test, self.method_name)(compared_list, self.kind)
        if t:
            return 1
        else:
            return -1


def create_Kruskal_hypot_MST(ret_inds, stocks, alpha=0.05, one_sided=True, kind='not_rand'):

    list_edges = edges(stocks)
    edge_class = EdgeComparator(ret_inds, alpha, one_sided, kind)
    list_edges = sorted(list_edges, key=cmp_to_key(edge_class.comparator))

    G = nx.Graph()
    G.add_edge(stocks[list_edges[0][0]], stocks[list_edges[0][1]])

    for edge in list_edges:
        if (stocks[edge[1]] not in G.nodes()) or (
                stocks[edge[1]] in G.nodes() and stocks[edge[0]] not in nx.node_connected_component(G, stocks[edge[1]])):
            G.add_edge(stocks[edge[0]], stocks[edge[1]])
        if len(list(G.nodes)) == len(stocks) and nx.is_connected(G):
            return G

    print('Error Kruskal')


# stcks = ['a', 'b', 'c', 'd', 'e']
# corr = [[1.0, 0.9, 0.0, 0.5, 0.5],
#         [0.9, 1.0, 0.0, 0.0, 0.0],
#         [0.0, 0.0, 0.1, 0.0, 0.0],
#         [0.5, 0.0, 0.0, 0.1, 0.0],
#         [0.5, 0.0, 0.0, 0.0, 0.1]]
#
# article_corr = [[1.0000, 0.7220, 0.4681, 0.4809, 0.6209, 0.5380, 0.6252], \
#                 [0.7220, 1.0000, 0.4395, 0.5979, 0.6381, 0.5725, 0.6666], \
#                 [0.4681, 0.4395, 1.0000, 0.3432, 0.3468, 0.2740, 0.4090], \
#                 [0.4809, 0.5979, 0.3432, 1.0000, 0.4518, 0.4460, 0.4635], \
#                 [0.6209, 0.6381, 0.3468, 0.4518, 1.0000, 0.5640, 0.5994], \
#                 [0.5380, 0.5725, 0.2740, 0.4460, 0.5640, 1.0000, 0.4969], \
#                 [0.6252, 0.6666, 0.4090, 0.4635, 0.5994, 0.4969, 1.0000]]
#
# article_stocks = ['A', 'AA', 'AAP', 'AAPL', 'AAWW', 'ABAX', 'ACCO']
#
# new_rets = norm_seq(article_corr, 100)
# new_inds = indicators(new_rets)
#
# create_Kruskal_hypot_MST(new_inds, article_stocks, 0.5)
