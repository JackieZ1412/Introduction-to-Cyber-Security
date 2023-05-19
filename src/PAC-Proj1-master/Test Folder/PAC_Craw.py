import networkx as nx
import matplotlib.pyplot as plt
import copy
import codecs
import os

def __find_k_cliques(G, k):
    rcl = nx.find_cliques_recursive(G)
    k_cliques_list = []
    while True:
        edge_list = []
        try:
            clique_list = next(rcl)
            if len(clique_list) != k:
                continue
            else:
                for i in range(len(clique_list)):
                    for j in range(i+1, len(clique_list)):
                        edge_list.append(G.has_edge(clique_list[i], clique_list[j]))
                        edge_list.append(G.has_edge(clique_list[j], clique_list[i]))

                if all(has_edge is True for has_edge in edge_list):
                    k_cliques_list.append(clique_list)

        except StopIteration:
            break

    if len(k_cliques_list) == 0:
        return None
    else:
        return k_cliques_list

def __calc_node_cnc(G_undirected, target_node, k_clique):
    sum_cnc = 0
    for node in k_clique:
        if target_node != node:
           sum_cnc += len(sorted(nx.common_neighbors(G_undirected, target_node, node)))
    return float(sum_cnc)

def find_k_clique_seed(lgraph, rgraph, k, e):
    seed_mapping = dict()
    seed_mappings = []
    lgraph_k_clqs = __find_k_cliques(lgraph, k)
    rgraph_k_clqs = __find_k_cliques(rgraph, k)
    lgraph_undirected = lgraph.to_undirected()
    rgraph_undirected = rgraph.to_undirected()

    if lgraph_k_clqs is not None and rgraph_k_clqs is not None:
        for lgraph_k_clq in lgraph_k_clqs:
            for rgraph_k_clq in rgraph_k_clqs:
                for lnode in lgraph_k_clq:
                    for rnode in rgraph_k_clq:
                        lnode_cnc = __calc_node_cnc(lgraph_undirected, lnode, lgraph_k_clq)
                        rnode_cnc = __calc_node_cnc(rgraph_undirected, rnode, rgraph_k_clq)
                        lnode_degree = float(lgraph.degree(lnode))
                        rnode_degree = float(rgraph.degree(rnode))

                        if (1-e <= (lnode_cnc/rnode_cnc) <= 1+e) and (1-e <= (lnode_degree/rnode_degree) <= 1+e):
                            seed_mapping[lnode] = rnode
                            break

                if len(seed_mapping) == k:
                    seed_mappings.append(copy.deepcopy(seed_mapping))
                    seed_mapping.clear()

    return seed_mappings

def plot_graph(graph, filename):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_size=50, with_labels=True)
    plt.savefig(filename)
    plt.show()

def read_graph(filename):
    graph = nx.Graph()
    with codecs.open(filename, "r", "utf-8") as fp:
        for line in fp:
            node1, node2 = line.strip().split("\t")
            graph.add_edge(node1, node2)
    return graph

if __name__ == "__main__":
    lgraph = read_graph("lgraph.txt")
    rgraph = read_graph("rgraph.txt")
    plot_graph(lgraph, "lgraph.png")
    plot_graph(rgraph, "rgraph.png")
    seed_mappings = find_k_clique_seed(lgraph, rgraph, 4, 0.1)
    print(seed_mappings)