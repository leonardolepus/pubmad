import pickle
import matplotlib.pyplot as plt

with open('data/evex/Homo_Sapiens/evex_digraph.graph', 'r') as evex_f:
    evex = pickle.load(evex_f)

def type1_trans(g, n):
    preds = set(g.predecessors(n))
    succs = set(g.successors(n))
    count = 0
    for pred in preds:
        new_succs = set(g.successors(pred))
        common_succs = succs & new_succs
        count = count + len(common_succs)
    return len(preds) and len(succs) and 1.0 * count / (len(preds) * len(succs))

node_trans_type1 = [type1_trans(evex, n) for n in evex.nodes_iter()]
plt.hist(node_trans_type1, bins = 100)
plt.show()
node_trans_type1_non_zeros = [i for i in node_trans_type1 if i]
plt.hist(node_trans_type1_non_zeros, bins = 100)

dc = [evex.node[n].get('degree_centrality') for n in evex.nodes_iter()]
plt.hist(dc, bins = 100)
plt.show()

node_trans_type1_high_dc = [a for a, b in zip(node_trans_type1, dc) if a and b > 0.0005]
plt.hist(node_trans_type1_high_dc, bins = 100)
plt.show()
