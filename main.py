import copy
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import time

'''to-do list:
draw connected components of a graph
convert a multigraph to graph
page rank'''


def import_graph(file):
    g = nx.MultiDiGraph()
    ebunch = []
    with open(file,'r') as f:
        next(f)
        reader=csv.reader(f,delimiter='\t')
        for event_id, source, target, confidence, negation, speculation, coarse_type, coarse_polarity, refined_type, refined_polarity in reader:
            event_id = int(event_id)
            source = int(source)
            target = int(target)
            confidence = float(confidence)
            negation = int(negation)
            speculation = int(speculation)
            edge = (source, target, {'general_event_id' : event_id,
                                     'confidence' : confidence,
                                     'negation' : negation,
                                     'speculation' : speculation,
                                     'coarse_type' : coarse_type,
                                     'coarse_polarity' : coarse_polarity,
                                     'refined_type' : refined_type,
                                     'refined_polarity' : refined_polarity})
            ebunch.append(edge)
            if len(ebunch) >= 5000:
                break
    g.add_edges_from(ebunch)
    print 'a MultiDiGraph is constructed'
    print 'graph has', g.number_of_nodes(), 'nodes'
    print 'graph has', g.number_of_edges(), 'edges'
    return g


def transitiveness_graph(g):
    t = nx.DiGraph()
    nbunch = []
    ebunch = []
    for n, nbr in g.edges():
        attr = copy.deepcopy(g[n][nbr][0])
        general_event_id = attr['general_event_id']
        attr['source'] = n
        attr['target'] = nbr
        node = (general_event_id, attr)
        nbunch.append(node)
    t.add_nodes_from(nbunch)
    nodes = g.nodes()
    for node1 in nodes:
        node2s = g[node1]
        for node2 in node2s:
            node3s = g[node2]
            for node3 in node3s:
                if node3 in node2s:
                    edge1 = node2s[node2][0]['general_event_id']
                    edge2 = node3s[node3][0]['general_event_id']
                    edge3 = node2s[node3][0]['general_event_id']
                    ebunch.append((edge1, edge2))
                    ebunch.append((edge2, edge3))
                    #t.add_edges_from([(edge1, edge3), (edge2, edge3)])
    t.add_edges_from(ebunch)
    print 'the transitiveness_graph is computed'
    print 'graph has', t.number_of_nodes(), 'nodes'
    print 'graph has', t.number_of_edges(), 'edges'
    return t


def plot(g, file = None, weighted = False, weighted_edge = False):
    pos=nx.spring_layout(g)
    if weighted:
        weights = [g.node[n][weighted] for n in g]
        max_weight = max(weights)
        node_size = [100 * weight / max_weight for weight in weights]
    else:
        node_size = 10
    nx.draw_networkx_nodes(g,pos,node_size=node_size)
    nx.draw_networkx_edges(g,pos,alpha=0.4)
    if file:
        plt.savefig(file)
        plt.close()
    else:
        plt.show()
        plt.close()


def reverse(g):
    rg = nx.DiGraph()
    rg.add_nodes_from(g.nodes())
    for n, nbr in g.edges():
        rg.add_edge(nbr, n)
    return rg

    
def save_data(obj, path):
    f = open(path, 'w')
    pickle.dump(obj, f)
    f.close()


if __name__ == '__main__':
    file = 'data/Homo_Sapiens/EVEX_relations_9606.tab'
    t1 = time.time()
    g = import_graph(file)
    t2 = time.time()
    print 'load relations', t2 - t1
    t= transitiveness_graph(g)
    t3 = time.time()
    print 'find transitive relations', t3 - t2
    #plot(g, 'relations')
    pr = nx.pagerank(t)
    t4 = time.time()
    print 'pagerank', t4 - t3
    for node in pr:
        t.node[node]['confirming_weight'] = pr[node]
    t5 = time.time()
    print 'write pr into graph', t5 - t4
    #plot(t, 'good_confirming_relations', 'confirming_weight')
    t_rev = reverse(t)
    t6 = time.time()
    print 'reverse t', t6 - t5
    pr_rev = nx.pagerank(t_rev)
    t7 = time.time()
    print 'pagerank', t7 - t6
    for node in pr:
        t.node[node]['predicting_weight'] = pr_rev[node]
    t8 = time.time()
    print 'write pr into graph', t8 - t7
    #plot(t, 'good_predicting_relations', 'predicting_weight')
    save_data(g, 'data/g')
    save_data(t, 'data/t')
    save_data(pr, 'data/conf_pr')
    save_data(pr_rev, 'data/pre_pr')
