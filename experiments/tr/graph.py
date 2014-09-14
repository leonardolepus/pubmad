import os, re, pickle
import networkx as nx

DATA_PATH = '../../data/graph/edge_count/'

files = os.listdir(DATA_PATH)
files = [re.match('part-\d{5}', a) for a in files]
files = [a.group() for a in files if a is not None]
files.sort()
print files

g = nx.Graph()
edge_list = []
for file_name in files:
    with open(DATA_PATH+file_name, 'r') as f:
        for line in f:
            line.strip()
            edge, count = line.split('\t')
            count = int(count)
            source, target = edge.split('==')
            edge = (source, target, dict(weight=count))
            edge_list.append(edge)
    g.add_edges_from(edge_list)
    print file_name

with open('../../data/graph/pickle_graph', 'w') as f:
    pickle.dump(g, f)
with open('../../data/graph/graphml', 'w') as f:
    nx.write_graphml(g, f)
    
adj = nx.adjacency_matrix(g)
with open('../../data/graph/pickle_adj', 'w') as f:
    pickle.dump(adj, f)
