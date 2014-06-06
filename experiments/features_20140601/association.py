import pickle
import os, sys
import itertools

import matplotlib.pyplot as plt
from scipy import stats

features = {}
for feature_file in os.listdir('../../data/evex/Homo_Sapiens/features/'):
    with open('../../data/evex/Homo_Sapiens/features/'+feature_file, 'r') as f:
        try:
            features[feature_file] = pickle.load(f)
        except:
            print feature_file, sys.exc_info()
edge_betweenness_centrality = features['edge_betweenness_centrality']
del features['edge_betweenness_centrality']

def association(x, y, xlabel, ylabel):
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    y_prime = [i*slope+intercept for i in x]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(xlabel+'_VS_'+ylabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.text(min(x), max(y), '%s = %f*%s %f\nr^2 = %f' % (ylabel, slope, xlabel, intercept, r**2))
    ax.scatter(x, y)
    ax.plot(x, y_prime)
    plt.savefig('output/'+xlabel+'_'+ylabel+'.png')

for i, j in itertools.product(features, features):
    fi = features[i].values()
    fj = features[j].values()
    association(fi, fj, i, j)

