import pickle

from matplotlib import pyplot as plt
import networkx as nx

from kegg_kgml_parser.parse_KGML import KGML2Graph

kegg_f = 'kegg/hsa04150.xml'
kegg = KGML2Graph(kegg_f)

if 'evex' not in globals():
    evex_f = open('evex/Homo_Sapiens/g', 'r')
    evex = pickle.load(evex_f)
    evex_f.close()

root = 2475

edges_with_pr = []
for target in evex[root]:
    try:
        edges_with_pr.append((target, evex[root][target][0]['pre_pr']))
    except KeyError:
        print 'an edge has no pr'
sorted_edges_with_pr = sorted(edges_with_pr, key = lambda x: x[1], reverse = True)
[sorted_edges, sorted_pr] = zip(*sorted_edges_with_pr)

kegg_edges = kegg[root].keys()
hits = []
ranks = []
false_neg = []
false_neg_ranks = []
for target in kegg_edges:
    if target in sorted_edges:
        hits.append(target)
        ranks.append(sorted_edges.index(target))
    else:
        false_neg.append(target)
recall = 1.0 * len(hits)/len(kegg_edges)
print 'recall:', recall
print ranks, 'out of', len(sorted_edges), 'edges'
nranks = [1.0*rank/len(sorted_edges) for rank in ranks]
print nranks

def f_score(recall, gain):
    return recall and gain and 2*recall*gain/(recall+gain)

pr = []
err = 0
for source, target in evex.edges():
    try:
        pr.append(evex[source][target][0]['pre_pr'])
    except KeyError:
        err = err + 1
pr.sort()
print err
plt.plot(pr)
plt.show()
