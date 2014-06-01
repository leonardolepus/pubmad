#applicable to directed graph only

import pickle
import networkx as nx
import matplotlib.pyplot as plt


def find_induction(g, e):
    #find edges that may induce e
    #i.e. if e=a->c, e1=a->b, e2=b->c, then return [(e, e1), (e, e2)]
    s, t = e
    s_down = set(g.successors(s))
    t_up = set(g.predecessors(t))
    mediators = s_down & t_up
    induced_by = []
    for m in mediators:
        induced_by.append((s, m))
        induced_by.append((m, t))
    return [(e, e_prime) for e_prime in induced_by]


def induction_graph(g):
    ind = nx.DiGraph()
    for e in g.edges_iter():
        ind.add_edges_from(find_induction(evex, e))
    return ind


if __name__ == '__main__':
    with open('../../data/evex/Homo_Sapiens/evex_digraph.graph', 'r') as evex_f:
        evex = pickle.load(evex_f)
    evex_i = induction_graph(evex)
    dc = nx.degree_centrality(evex_i)
    plt.hist(dc.values(), bins = 100)
    plt.show()
