import pickle
import matplotlib.pyplot as plt

from toolbox.graph_io.kegg.kegg_kgml_parser.parse_KGML import KGML2Graph


with open('evex_digraph.graph', 'r') as evex_f:
    evex = pickle.load(evex_f)

kegg_f = 'data/kegg/hsa04150.xml'
kegg = KGML2Graph(kegg_f)

evex_as_at = []
evex_at_as = []
for s, t in evex.edges_iter():
    evex_as_at.append(evex[s][t]['as_at'])
    evex_at_as.append(evex[s][t]['at_as'])

as_at = []
at_as = []
for s, t in kegg.edges_iter():
    if evex.has_edge(s, t):
        as_at.append(evex[s][t]['as_at'])
        at_as.append(evex[s][t]['at_as'])

plt.hold(True)
plt.hist(evex_as_at, bins = 100, range = (0, 1), normed = True)
plt.hist(as_at, bins = 100, range = (0, 1), normed = True)
plt.savefig('evex_as_at_vs_kegg_as_at')
plt.close()
plt.hist(evex_at_as, bins = 100, range = (0, 1), normed = True)
plt.hist(at_as, bins = 100, range = (0, 1), normed = True)
plt.savefig('evex_at_as_vs_kegg_at_as')
plt.close()
