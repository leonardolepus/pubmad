import pickle
from collections import Counter
from math import log

from scipy import stats
from matplotlib import pyplot as plt
import networkx as nx

with open('data/evex/Homo_Sapiens/evex_graph.graph', 'r') as f:
    evex = pickle.load(f)

degrees = [evex.degree(n) for n in evex.nodes_iter()]
plt.hist(degrees, bins = 100)
plt.show()

freq = Counter(degrees)
dgr = freq.keys()
occr = freq.values()

del dgr[0]
del occr[0]

plt.scatter(dgr, occr)
plt.show()

log_dgr = map(log, dgr)
log_occr = map(log, occr)

plt.scatter(log_dgr, log_occr)
plt.show()

plt.scatter(dgr, log_occr)
plt.show()

def lin_regr(x, y):
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    print slope, intercept, r**2, p
    plt.scatter(x, y)
    y_prime = [i*slope+intercept for i in x]
    plt.plot(x, y_prime)
    plt.show()

lin_regr(dgr, log_occr)

lin_regr(log_dgr, log_occr)

