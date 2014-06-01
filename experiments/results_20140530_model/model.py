import pickle
from collections import Counter
from math import log, exp

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import networkx as nx

with open('data/evex/Homo_Sapiens/evex_graph.graph', 'r') as f:
    evex = pickle.load(f)

nbunch = []
for n in evex.nodes_iter():
    if not evex[n]:
        nbunch.append(n)
evex.remove_nodes_from(nbunch)
    
degrees = [evex.degree(n) for n in evex.nodes_iter()]
plt.hist(degrees, bins = 100)
plt.show()

freq = Counter(degrees)
dgr = freq.keys()
occr = freq.values()

total_degrees = len(degrees)
#d_range = range(1, max(dgr) + 1)
#freq_range = [freq.get(d) or 0 for d in d_range]
#freq_range = [1.0*f/total_degrees for f in freq_range]
new_freq = {}
for i in range(0, len(dgr)-1):
    di = dgr[i]
    di1 = dgr[i+1]
    if not new_freq.has_key(di):
        new_freq[di] = freq[di]
    if di1-di > 1:
        new_freq[di1] = 1.0*(freq[di1])/(di1-di)
d_range = new_freq.keys()
freq_range = new_freq.values()
freq_range = [1.0*i/total_degrees for i in freq_range]

plt.scatter(d_range, freq_range)
plt.show()

log_d = map(log, d_range)
log_f = map(log, freq_range)
plt.scatter(log_d, log_f)
plt.show()
plt.scatter(d_range, log_f)
plt.show()

def lin_regr(x, y, show = True):
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    print slope, intercept, r**2, p, std_err
    plt.scatter(x, y)
    y_prime = [i*slope+intercept for i in x]
    plt.plot(x, y_prime)
    plt.show()
    return (slope, intercept, r, p, std_err)
    
#growing network model where new nodes attach to existing nodes uniformly randomly
lin_regr(d_range, log_f)

#growing network model with preferential attachment
lin_regr(log_d, log_f)

#hybrid model
#log(1 - F(d)) = x*log(m+amx) - x * log(d + amx)
#where x = 2 / (1 - a)
d_range = range(1, max(dgr))
F = lambda d: 1.0*len([dgr for dgr in degrees if dgr <= d])/len(degrees)
m = 31
a = 0.05
x = 2.0/(1-a)
F_prime = lambda d: 1-((m+a*m*x)/(d+a*m*x))**x
f = [F(d) for d in d_range]
f_prime = [F_prime(d) for d in d_range]
plt.hold(True)
right = [log(d+a*m*x) for d in d_range]
left = [log(1-F(d)) for d in d_range]
slope, intercept, r, p, std_err = lin_regr(right, left)
a_prime = 1+2.0/slope
x_prime = 2.0/(1-a_prime)
m_prime = exp(intercept/x_prime)/(1+a_prime*x_prime)
print a_prime, m_prime
plt.scatter(d_range, f)
plt.scatter(d_range, f_prime)
plt.show()

'''
#log(1 - F(d)) = x*log(m+amx) - x * log(d + amx)
#where x = 2 / (1 - a)
F = lambda d: 1.0*len([dgr for dgr in degrees if dgr <= d])/len(degrees)

m = 1.0*sum(degrees)/len(degrees)/2
d_range = range(10, max(dgr))

m = 10
a = 0.7
m_prime = 27
a_prime = 0.1
while abs(m_prime-m) > 2 or abs(a_prime-a) > 0.01:
    a = a_prime
    m = m_prime
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
'''

