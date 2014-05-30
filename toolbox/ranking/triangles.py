import math

import networkx as nx
from matplotlib import pyplot as plt
from scipy import stats

def count_triangles(g, n):
    triangle = 0
    nbrs = set(g.neighbors(n))
    for nbr in nbrs:
        nbrs_of_nbr = set(g.neighbors(nbr))
        common_nbrs = nbrs_of_nbr & nbrs
        triangle = triangle + len(common_nbrs)
    return triangle/2
    

if __name__ == '__main__':
    import sys, os.path
    path = os.path.abspath('../../')
    sys.path.insert(1, path)
    from toolbox.graph_io.evex.nx import import_graph

    syn_f = '../../data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
    rel_f = '../../data/evex/Homo_Sapiens/EVEX_relations_9606.tab'
    evex = import_graph(nx.Graph(), syn_f, rel_f)
    nbunch = [n for n in evex.nodes_iter() if not evex[n]]
    evex.remove_nodes_from(nbunch)

    triangles = [count_triangles(evex, n) for n in evex.nodes_iter()]

    plt.hist(triangles, bins = 100)
    plt.show()

    degrees = [evex.degree(n) for n in evex.nodes_iter()]
    plt.hist(degrees, bins = 100)
    plt.show()

    plt.scatter(degrees, triangles)
    plt.show()
    print stats.linregress(degrees, triangles)
    
    log_d, log_t = zip(*[(math.log(d), math.log(t)) for d, t in zip(degrees, triangles) if t])
    plt.scatter(log_d, log_t)
    plt.show()
    print stats.linregress(log_d, log_t)
