import os, re
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
