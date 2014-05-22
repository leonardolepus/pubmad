import re
import pickle
import os

from matplotlib import pyplot as plt
import scipy.stats as stats
import networkx as nx

from kegg_kgml_parser.parse_KGML import KGML2Graph

kegg_fs = os.listdir('kegg')
kegg_fs = ['kegg/'+i for i in kegg_fs if re.match('hsa04012.xml', i)]
keggs = []
for kegg_f in kegg_fs:
    kegg = KGML2Graph(kegg_f)
    keggs.append(kegg)
kegg = nx.compose_all(keggs)

if 'evex' not in globals():
    evex_f = open('evex/Homo_Sapiens/g', 'r')
    evex = pickle.load(evex_f)
    evex_f.close()

def filter_g(g):
    return g

evex = filter_g(evex)
kegg = filter_g(kegg)

prs = [evex[source][target][0]['pre_pr'] for source, target in evex.edges_iter() if evex[source][target][0].has_key('pre_pr')]

'''
for source, target in evex.edges_iter():
    try:
        prs.append(evex[source][target][0]['pre_pr']))
    except KeyError:
        print 'an edge has no pr'
sorted_edges_with_pr = sorted(edges_with_pr, key = lambda x: x[1], reverse = True)
[sorted_edges, sorted_pr] = zip(*sorted_edges_with_pr)
'''
        
hits = []
hits_pr = []
false_neg = []
for source, target in kegg.edges_iter():
    if evex.has_edge(source, target) and evex[source][target][0].has_key('pre_pr'):
        hits.append((source, target))
        hits_pr.append(evex[source][target][0]['pre_pr'])
    else:
        false_neg.append((source, target))
recall = 1.0 * len(hits)/len(kegg.edges())
print 'recall =', len(hits), '/', len(kegg.edges()), '=', recall
percentile = [stats.percentileofscore(prs, i) for i in hits_pr]
percentile.sort()
plt.plot(percentile)
plt.show()
'''
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
'''
