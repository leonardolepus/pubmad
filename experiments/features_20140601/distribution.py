import pickle
import os, sys
import itertools

import matplotlib.pyplot as plt
from scipy import stats

sys.path.insert(1, os.path.abspath('../../'))
from toolbox.graph_io.kegg.parse_KGML import KGML2Graph

features = {}
for feature_file in os.listdir('../../data/evex/Homo_Sapiens/features/'):
    with open('../../data/evex/Homo_Sapiens/features/'+feature_file, 'r') as f:
        try:
            features[feature_file] = pickle.load(f)
        except:
            print feature_file, sys.exc_info()
edge_betweenness_centrality = features['edge_betweenness_centrality']
del features['edge_betweenness_centrality']


def distribution(x, label):
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title(label+'_hist')
    ax1.hist(x, bins = 100, histtype = 'step')
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_title(label+'_cumulative_normalized')
    ax2.hist(x, bins = 100, cumulative = True, normed = True, histtype = 'step')
    plt.savefig(label)

for i in features:
    x = features[i].values()
    distribution(x, i)


pathway_f = '../../data/kegg/hsa04151.xml'
kegg = KGML2Graph(pathway_f)
kegg = kegg.to_undirected()

for i in features:
    ev = features[i]
    ke = [ev[j] for j in kegg.nodes_iter() if j in ev]
    ev = ev.values()
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title(i+'_hist')
    ax1.hist(ev, bins = 100, histtype = 'step', label = 'evex', normed = True)
    ax1.hist(ke, bins = 100, histtype = 'step', label = 'kegg', normed = True)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_title(i+'_cumulative_normalized')
    ax2.hist(ev, bins = 100, cumulative = True, normed = True, histtype = 'step', label = 'evex')
    ax2.hist(ke, bins = 100, cumulative = True, normed = True, histtype = 'step', label = 'kegg')
    plt.savefig(i+'_evex_VS_kegg')
    

    
