import pickle
import csv
import matplotlib.pyplot as plt
import networkx as nx

from toolbox.graph_io.kegg.parse_KGML import KGML2Graph
from toolbox.graph_io.evex.nx import import_graph

evex_syno = 'data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
evex_rel = 'data/evex/Homo_Sapiens/EVEX_relations_9606.tab'
evex = import_graph(nx.MultiDiGraph(), evex_syno, evex_rel)

kegg_f = 'data/kegg/hsa04151.xml'
kegg = KGML2Graph(kegg_f)

report = {}
with open('data/evex/Homo_Sapiens/EVEX_articles_9606.tab', 'r') as f:
    next(f)
    reader = csv.reader(f, delimiter = '\t')
    for r, a in reader:
        r = int(r)
        if report.has_key(r):
            report[r].append(a)
        else:
            report[r] = [a]

def count_report(g, e, report):
    s, t = e
    if g.has_edge(s, t):
        attrs = g[s][t]
        reported_in = set()
        for attr in attrs.values():
            general_event_id = attr['general_event_id']
            if report.has_key(general_event_id):
                reported_in = reported_in | set(report[general_event_id])
        return len(reported_in)
    else:
        return None

kegg_report = {}
for e in kegg.edges_iter():
    num_report = count_report(evex, e, report)
    if num_report is not None:
        kegg_report[e] = num_report

evex_report = {}
for e in evex.edges_iter():
    num_report = count_report(evex, e, report)
    evex_report[e] = num_report

plt.hold(True)
plt.hist(evex_report.values(), bins = 100, normed = False, cumulative = False)
plt.hist(kegg_report.values(), bins = 100, normed = False, cumulative = False)
plt.show()
