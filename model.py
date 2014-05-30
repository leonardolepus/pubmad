import pickle
from collections import Counter
from math import log, exp

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import networkx as nx

with open('data/evex/Homo_Sapiens/evex_graph.graph', 'r') as f:
    evex = pickle.load(f)

degrees = [evex.degree(n) for n in evex.nodes_iter() if evex.degree(n)]
plt.hist(degrees, bins = 100)
plt.show()

freq = Counter(degrees)
dgr = freq.keys()
occr = freq.values()

plt.scatter(dgr, occr)
plt.show()

log_dgr = map(log, dgr)
log_occr = map(log, occr)

plt.scatter(log_dgr, log_occr)
plt.show()

plt.scatter(dgr, log_occr)
plt.show()

def lin_regr(x, y, show = True):
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    print slope, intercept, r**2, p, std_err
    plt.scatter(x, y)
    y_prime = [i*slope+intercept for i in x]
    plt.plot(x, y_prime)
    plt.show()

lin_regr(dgr, log_occr)

lin_regr(log_dgr, log_occr)

#log(1 - F(d)) = x*log(m+amx) - x * log(d + amx)
#where x = 2 / (1 - a)
F = lambda d: 1.0*len([dgr for dgr in degrees if dgr <= d])/len(degrees)

m = 1.0*sum(degrees)/len(degrees)/2
d_range = range(1, max(d_range))

m = 10
a = 0.7
m_prime = 40
a_prime = 0.9
while abs(m_prime-m) > 2 or abs(a_prime-a) > 0.1:
    a = (a+a_prime)/2
    m = (m+m_prime)/2
    x = 2.0/(1-a)
    right = [log(d+a*m*x) for d in d_range]
    left = [log(1-F(d)) for d in d_range]
    slope, intercept, r, p, std_err = stats.linregress(right, left)
    print slope, intercept, r**2, p, std_err
    lin_regr(right, left)
    a_prime = 1+2.0/slope
    x_prime = 2.0/(1-a_prime)
    m_prime = exp(intercept/x_prime)/(1+a_prime*x_prime)
    print a_prime, m_prime

m = 40
for a in np.arange(0.01, 0.97, 0.05):
    x = 2.0/(1-a)
    right = [log(d+a*m*x) for d in d_range]
    left = [log(1-F(d)) for d in d_range]
    slope, intercept, r, p, std_err = stats.linregress(right, left)
    lin_regr(right, left)
    #slope is -x
    a_prime = 1+2.0/slope
    print a
    print a_prime
    print abs(a_prime - a)
    if abs(a_prime - a) < 0.01:
        break

m = 40
a = 0.06
x = 2.0/(1-a)
F_prime = lambda d: 1-((m+a*m*x)/(d+a*m*x))**x
f = [F(d) for d in d_range]
f_prime = [F_prime(d) for d in d_range]
plt.hold(True)
plt.scatter(d_range, f)
plt.scatter(d_range, f_prime)
plt.show()
