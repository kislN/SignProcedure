import networkx as nx

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

