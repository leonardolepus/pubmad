import pickle
import matplotlib.pyplot as plt

from toolbox.graph_io.kegg.kegg_kgml_parser.parse_KGML import KGML2Graph

def hist(x, y, path, **args):
    plt.hold(True)
    plt.hist(x, **args)
    plt.hist(y, **args)
    plt.savefig(path)
    plt.close()

with open('data/evex/Homo_Sapiens/evex_digraph.graph', 'r') as evex_f:
    evex = pickle.load(evex_f)

kegg_f = 'data/kegg/hsa04151.xml'
kegg = KGML2Graph(kegg_f)

evex_as_at = []
evex_at_as = []
evex_ta_sa = []
evex_sa_ta = []
evex_bt_bs = []
evex_bs_bt = []
s = 207
for t in evex[207]:
    evex_as_at.append(evex[s][t]['as_at'])
    evex_at_as.append(evex[s][t]['at_as'])
    evex_ta_sa.append(evex[s][t]['ta_sa'])
    evex_sa_ta.append(evex[s][t]['sa_ta'])
    evex_bt_bs.append(evex[s][t]['bt_bs'])
    evex_bs_bt.append(evex[s][t]['bs_bt'])

as_at = []
at_as = []
ta_sa = []
sa_ta = []
bt_bs = []
bs_bt = []
s = 207
for t in kegg[207]:
    if evex.has_edge(s, t):
        as_at.append(evex[s][t]['as_at'])
        at_as.append(evex[s][t]['at_as'])
        ta_sa.append(evex[s][t]['ta_sa'])
        sa_ta.append(evex[s][t]['sa_ta'])
        bt_bs.append(evex[s][t]['bt_bs'])
        bs_bt.append(evex[s][t]['bs_bt'])

evex_trans = (evex_as_at, evex_at_as, evex_sa_ta, evex_ta_sa, evex_bt_bs, evex_bs_bt)
kegg_trans = (as_at, at_as, sa_ta, ta_sa, bt_bs, bs_bt)
fig_names = ('as_at', 'at_as', 'sa_ta', 'ta_sa', 'bt_bs', 'bs_bt')
for x, y, path in zip(evex_trans, kegg_trans, fig_names):
    hist(x, y, path, bins = 100, range = (0, 1), normed = True, cumulative = True)

'''    
plt.hold(True)
plt.hist(evex_as_at, bins = 100, range = (0, 1), normed = True, cumulative = True)
plt.hist(as_at, bins = 100, range = (0, 1), normed = True, cumulative = True)
plt.savefig('evex_as_at_vs_kegg_as_at')
plt.close()
plt.hist(evex_at_as, bins = 100, range = (0, 1), normed = True, cumulative = True)
plt.hist(at_as, bins = 100, range = (0, 1), normed = True, cumulative = True)
plt.savefig('evex_at_as_vs_kegg_at_as')
plt.close()
'''
