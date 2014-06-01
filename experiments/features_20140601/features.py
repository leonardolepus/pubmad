import os, sys
import pickle
from multiprocessing import Pool

import networkx as nx

sys.path.insert(1, os.path.abspath('../../'))
from toolbox.graph_io.evex.nx import import_graph
from toolbox.graph_io.kegg.parse_KGML import KGML2Graph

syn_f = '../../data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
rel_f = '../../data/evex/Homo_Sapiens/EVEX_relations_9606.tab'
evex = import_graph(nx.Graph(), syn_f, rel_f)
isolated_nodes = [n for n in evex.nodes_iter() if not evex[n]]
evex.remove_nodes_from(isolated_nodes)

pathway_f = '../../data/kegg/hsa04151.xml'
kegg = KGML2Graph(pathway_f)
kegg = kegg.to_undirected()

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
cce = nx.communicability_centrality_exp(kegg)   #only applicable to undirected graphs
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

#use multiprocessing.Pool to compute evex features in parallel
funcs = {'degree_centrality' : nx.degree_centrality,
         'closeness_centrality' : nx.closeness_centrality,
         'betweenness_centrality' : nx.betweenness_centrality,
         'eigenvector_centrality_numpy' : nx.eigenvector_centrality_numpy,
         'katz_centrality_numpy' : nx.katz_centrality_numpy,
         'communicability_centrality_exp' : nx.communicability_centrality_exp,
         'load_centrality' : nx.load_centrality,
         'triangles' : nx.triangles,
         'degree' : nx.degree,
         'clustering' : nx.clustering,
         'square_clustering' : nx.square_clustering,
         'edge_betweenness_centrality' : nx.edge_betweenness_centrality}

def foo(feature_name):
    try:
        func = funcs[feature_name]
        feature = func(evex)
        with open('features/'+feature_name, 'w') as f:
            pickle.dump(feature, f)
        return {feature_name : 1}
    except:
        print feature_name, sys.exc_info()
        return {feature_name : 0}

pool = Pool(3, maxtasksperchild = 1)
features = ['degree', 'triangles', 'degree_centrality', 'clustering', 'square_clustering', 'closeness_centrality', 'betweenness_centrality', 'eigenvector_centrality_numpy', 'katz_centrality_numpy', 'communicability_centrality_exp', 'load_centrality', 'edge_betweenness_centrality']
results = pool.map_async(foo, features)
print results.get()
pool.close()
pool.join()
