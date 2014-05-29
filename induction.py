import pickle
import networkx as nx
import matplotlib.pyplot as plt

with open('data/evex/Homo_Sapiens/evex_digraph.graph', 'r') as evex_f:
    evex = pickle.load(evex_f)

def find_induction(g, e):
    s, t = e
    s_down = set(g.successors(s))
    t_up = set(g.predecessors(t))
    mediators = s_down & t_up
    induced_by = []
    for m in mediators:
        induced_by.append((s, m))
        induced_by.append((m, t))
    return [(e, e_prime) for e_prime in induced_by]

evex_i = nx.DiGraph()
for e in evex.edges_iter():
    evex_i.add_edges_from(find_induction(evex, e))

#pr = nx.pagerank(evex_i)
dc = nx.degree_centrality(evex_i)
plt.hist(dc.values(), bins = 100)
plt.show()

evex_i_inverse = evex_i.reverse()
