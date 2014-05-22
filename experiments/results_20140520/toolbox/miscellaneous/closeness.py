import csv
import pickle

from matplotlib import pyplot as plt
import networkx as nx

from kegg_kgml_parser.parse_KGML import KGML2Graph




'''
if 'evex' not in globals():
    evex_f = open('evex/Homo_Sapiens/g', 'r')
    evex = pickle.load(evex_f)
    evex_f.close()
'''

import csv
import pickle

from matplotlib import pyplot as plt
import networkx as nx

from kegg_kgml_parser.parse_KGML import KGML2Graph




'''
if 'evex' not in globals():
    evex_f = open('evex/Homo_Sapiens/g', 'r')
    evex = pickle.load(evex_f)
    evex_f.close()
'''


f = 'evex/Homo_Sapiens/EVEX_relations_9606.tab'
evex = import_graph(f)
akt = 207
mtor = 2475
source = akt
cl = [(t, closeness((source, t), evex)) for t in evex[source]]
sorted_cl = sorted(cl, key = lambda x: x[1], reverse = True)
ts, cls = zip(*sorted_cl)
cl_dict = {}
for t, c in cl:
    cl_dict[t] = c

kegg_f = 'kegg/hsa04151.xml'
kegg = KGML2Graph(kegg_f)

kegg_edges = kegg[source].keys()
hits = []
ranks = []
false_neg = []
false_neg_ranks = []
for target in kegg_edges:
    if target in ts:
        hits.append(target)
        ranks.append(ts.index(target))
    else:
        false_neg.append(target)
recall = 1.0 * len(hits)/len(kegg_edges)
print 'recall:', recall
print ranks, 'out of', len(ts), 'edges'
nranks = [1.0*rank/len(ts) for rank in ranks]
print nranks

def f_score(recall, gain):
    return recall and gain and 2*recall*gain/(recall+gain)

plt.plot(cls)
plt.show()


f = 'evex/Homo_Sapiens/EVEX_relations_9606.tab'
evex = import_graph(f)
akt = 207
mtor = 2475
source = akt
cl = [(t, closeness((source, t), evex)) for t in evex[source]]
sorted_cl = sorted(cl, key = lambda x: x[1], reverse = True)
ts, cls = zip(*sorted_cl)
cl_dict = {}
for t, c in cl:
    cl_dict[t] = c

kegg_f = 'kegg/hsa04151.xml'
kegg = KGML2Graph(kegg_f)

kegg_edges = kegg[source].keys()
hits = []
ranks = []
false_neg = []
false_neg_ranks = []
for target in kegg_edges:
    if target in ts:
        hits.append(target)
        ranks.append(ts.index(target))
    else:
        false_neg.append(target)
recall = 1.0 * len(hits)/len(kegg_edges)
print 'recall:', recall
print ranks, 'out of', len(ts), 'edges'
nranks = [1.0*rank/len(ts) for rank in ranks]
print nranks

def f_score(recall, gain):
    return recall and gain and 2*recall*gain/(recall+gain)

plt.plot(cls)
plt.show()

