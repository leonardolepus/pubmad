'''
in this experiment various transitiveness are calculated, and their distributions and associations are examined
the data shows that
a. if a node is connected to one end of an edge, it is more likely to be connected to the other end, compared to a randomly chosen node in the whole graph
b. there is no association found between various transitivenesses of the same edge

currently I am not sure wether all edges allow transitive inductions at the same possiblity and the observed distribution is simply out of randomness, or indeed some of the edges are inherently different from the others
'''

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

import networkx as nx

from toolbox.graph_io.evex.nx import import_graph
from toolbox.ranking.transitiveness import trans, ditrans


evex_synonyms = 'data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
evex_relations = 'data/evex/Homo_Sapiens/EVEX_relations_9606.tab'

graph = import_graph(nx.Graph(), evex_synonyms, evex_relations)

as_at = []
at_as = []
for e in graph.edges_iter():
    trns = trans(graph, e)
    s, t = e
    attr = graph[s][t]
    attr.update(trns)
    as_at.append(trns['as_at'])
    at_as.append(trns['at_as'])

plt.hold(False)

degree_centrality = nx.degree_centrality(graph)
plt.hist(degree_centrality.values(), bins = 100)
plt.savefig('graph_degree_centrality_hist.png')
plt.hist(as_at, bins = 100)
plt.savefig('graph_as_at_hist.png')
plt.hist(at_as, bins = 100)
plt.savefig('graph_at_as_hist.png')
samples = np.random.random_integers(len(as_at), size = 1000)
as_at_sample = [as_at[i] for i in samples]
at_as_sample = [at_as[i] for i in samples]
plt.scatter(as_at_sample, at_as_sample)
plt.savefig('graph_as_at_sample_at_as_sample.png')


digraph = import_graph(nx.DiGraph(), evex_synonyms, evex_relations)

as_at = []
at_as = []
ta_sa = []
sa_ta = []
bs_bt = []
bt_bs = []
for e in digraph.edges_iter():
    trns = ditrans(digraph, e)
    s, t = e
    attr = digraph[s][t]
    attr.update(trns)
    as_at.append(trns['as_at'])
    at_as.append(trns['at_as'])
    ta_sa.append(trns['ta_sa'])
    sa_ta.append(trns['sa_ta'])
    bs_bt.append(trns['bs_bt'])
    bt_bs.append(trns['bt_bs'])

plt.hold(False)

degree_centrality = nx.degree_centrality(digraph)
plt.hist(degree_centrality.values(), bins = 100)
plt.savefig('digraph_degree_centrality_hist.png')
plt.hist(as_at, bins = 100)
plt.savefig('digraph_as_at_hist.png')
plt.hist(at_as, bins = 100)
plt.savefig('digraph_at_as_hist.png')
plt.hist(ta_sa, bins = 100)
plt.savefig('digraph_ta_sa_hist.png')
plt.hist(sa_ta, bins = 100)
plt.savefig('digraph_sa_ta_hist.png')
plt.hist(bt_bs, bins = 100)
plt.savefig('digraph_bt_bs_hist.png')
plt.hist(bs_bt, bins = 100)
plt.savefig('digraph_bs_bt_hist.png')
samples = np.random.random_integers(len(as_at), size = 10000)
[as_at_sample, at_as_sample, sa_ta_sample, ta_sa_sample, bt_bs_sample, bs_bt_sample] = [[population[i] for i in samples] for population in [as_at, at_as, sa_ta, ta_sa, bt_bs, bs_bt]]
plt.scatter(as_at_sample, at_as_sample)
plt.savefig('digraph_as_at_sample_at_as_sample.png')
plt.scatter(sa_ta_sample, ta_sa_sample)
plt.savefig('digraph_sa_ta_sample_ta_sa_sample.png')
plt.scatter(bt_bs_sample, bs_bt_sample)
plt.savefig('digraph_bt_bs_sample_bs_bt_sample.png')
plt.scatter(at_as_sample, sa_ta_sample)
plt.savefig('digraph_at_as_sample_sa_ta_sample.png')
plt.scatter(at_as, sa_ta)
plt.savefig('digraph_at_as_sa_ta.png')
plt.hexbin(at_as, sa_ta, bins = 'log')
plt.savefig('digraph_at_as_sa_ta_hexbin.png')
