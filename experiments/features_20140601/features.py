import os, sys
import time
import pickle
import random
from multiprocessing import Pool

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

sys.path.insert(1, os.path.abspath('../../'))
from toolbox.graph_io.evex.nx import import_graph
from toolbox.graph_io.kegg.parse_KGML import KGML2Graph

syn_f = '../../data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
rel_f = '../../data/evex/Homo_Sapiens/EVEX_relations_9606.tab'
evex = import_graph(nx.Graph(), syn_f, rel_f)
isolated_nodes = [n for n in evex.nodes_iter() if not evex[n]]
evex.remove_nodes_from(isolated_nodes)
print 'evex has %d nodes and %d edges' % (evex.number_of_nodes(), evex.number_of_edges())

conn_com = nx.connected_components(evex)
print map(len, conn_com)
#as can be seen, the largest connected component of evex comprises the majority of the graph
#so the graph is made connected by adding an edge between a random node in the largest connected component and one in each of the other connected components
largest_conn_com = conn_com[0]
for com in conn_com[1:]:
    n1 = random.choice(com)
    n2 = random.choice(largest_conn_com)
    evex.add_edge(n1, n2)
print 'evex has %d nodes and %d edges' % (evex.number_of_nodes(), evex.number_of_edges())

pathway_f = '../../data/kegg/hsa04151.xml'
kegg = KGML2Graph(pathway_f)
kegg = kegg.to_undirected()

"""
#features for nodes
#calculating features of kegg is meaningless, this part is only a demonstration of which features are computed
dc = nx.degree_centrality(kegg)
cc = nx.closeness_centrality(kegg)
bc = nx.betweenness_centrality(kegg)
#cfcc = nx.current_flow_closeness_centrality(kegg)   #only applicable to connected undirected graphs
#cfbc = nx.current_flow_betweenness_centrality(kegg)   #only applicable to connected undirected graphs
#acfbc = nx.approximate_current_flow_betweenness_centrality(kegg)   #only applicable to connected undirected graphs
ec = nx.eigenvector_centrality_numpy(kegg)
kc = nx.katz_centrality_numpy(kegg)
#cce = nx.communicability_centrality_exp(kegg)   #only applicable to undirected graphs. it doesn't seem to make much sense and it causes segmentation fault... maybe due to long loops... so i removed it
lc = nx.load_centrality(kegg)
trg = nx.triangles(kegg)   #only applicable to undirected graphs
dgr = nx.degree(kegg)
cls = nx.clustering(kegg)   #only applicable to undirected graphs
scls = nx.square_clustering(kegg)

#features for edges
ebc = nx.edge_betweenness_centrality(kegg)
#ecfbc = nx.edge_current_flow_betweenness_centrality(kegg)   #only applicable to connected undirected graphs
#ce = nx.communicability_exp(kegg)   #it calculates something for every pair of nodes in graph. it's too crazy. i dont wanna try it. and, btw, it applies to undirected graphs only
#cbc = nx.communicability_betweenness_centrality(kegg)   #crazy for the same reason. and it applies to undirected graphs only. and all i got were nan's when i used it with undirected kegg sample graph
"""

#use multiprocessing.Pool to compute evex features in parallel
funcs = {'degree_centrality' : nx.degree_centrality,
         'closeness_centrality' : nx.closeness_centrality,
         'betweenness_centrality' : nx.betweenness_centrality,
         'eigenvector_centrality_numpy' : nx.eigenvector_centrality_numpy,
         'katz_centrality_numpy' : lambda x: nx.katz_centrality_numpy(x, alpha = 1./45),   #according to results of eigenvector_centrality, lambda = 43.***, alpha < 1/lambda makes it coverge
         'eigenvector_centrality' : nx.eigenvector_centrality,
         'katz_centrality' : lambda x: nx.katz_centrality(x, max_iter = 10000,  alpha = 1.0/45),   #according to results of eigenvector_centrality, lambda = 43.***, alpha < 1/lambda makes it coverge
         'communicability_centrality' : nx.communicability_centrality,
         #'communicability_centrality_exp' : nx.communicability_centrality_exp,
         'load_centrality' : nx.load_centrality,
         'triangles' : nx.triangles,
         'degree' : nx.degree,
         'clustering' : nx.clustering,
         'square_clustering' : nx.square_clustering,
         'edge_betweenness_centrality' : nx.edge_betweenness_centrality,
         'pagerank' : nx.pagerank}

def foo(feature_name):
    try:
        print feature_name
        t1 = time.time()
        func = funcs[feature_name]
        feature = func(evex)
        print 'calculation finished, %f min spent' % ((time.time()-t1)/60.0, )
        with open('output/features/'+feature_name, 'w') as f:
            pickle.dump(feature, f)
        print feature_name, 'saved', time.ctime()
        return {feature_name : 1}
    except:
        print feature_name, sys.exc_info()
        return {feature_name : 0}

pool = Pool(3, maxtasksperchild = 1)
features = ['degree', 'triangles', 'degree_centrality', 'clustering', 'eigenvector_centrality', 'pagerank','katz_centrality_numpy', 'closeness_centrality', 'betweenness_centrality', 'load_centrality', 'communicability_centrality', 'edge_betweenness_centrality', 'square_clustering']
results = pool.map_async(foo, features)
print results.get()
pool.close()
pool.join()

