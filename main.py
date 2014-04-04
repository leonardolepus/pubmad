import copy
import csv
import networkx as nx
import matplotlib.pyplot as plt

'''to-do list:
draw connected components of a graph
convert a multigraph to graph
page rank'''


def import_graph(file):
    g = nx.MultiDiGraph()
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
            #g.add_edge(source, target, object = event_id, confidence = confidence, negation = negation, speculation = speculation, coarse_type = coarse_type, coarse_polarity = coarse_polarity, refined_type = refined_type, refined_polarity = refined_polarity)
            g.add_edges_from([edge])
            if g.number_of_edges() >= 5000:
                break
    print 'a MultiDiGraph is constructed'
    print 'graph has', g.number_of_nodes(), 'nodes'
    print 'graph has', g.number_of_edges(), 'edges'
    return g


def transitiveness_graph(g):
    t = nx.DiGraph()
    for n, nbr in g.edges():
        attr = copy.deepcopy(g[n][nbr][0])
        general_event_id = attr['general_event_id']
        attr['source'] = n
        attr['target'] = nbr
        node = (general_event_id, attr)
        t.add_nodes_from([node])
    nodes = g.nodes()
    for node1 in nodes:
        node2s = g[node1].keys()
        for node2 in node2s:
            node3s = g[node2].keys()
            for node3 in node3s:
                if node3 in node2s:
                    edge1 = g[node1][node2][0]['general_event_id']
                    edge2 = g[node2][node3][0]['general_event_id']
                    edge3 = g[node1][node3][0]['general_event_id']
                    t.add_edges_from([(edge1, edge3), (edge2, edge3)])
    print 'the transitiveness_graph is computed'
    print 'graph has', t.number_of_nodes(), 'nodes'
    print 'graph has', t.number_of_edges(), 'edges'
    return t
        
if __name__ == '__main__':
    file = 'data/Homo_Sapiens/EVEX_relations_9606.tab'
    g = import_graph(file)
    pos=nx.spring_layout(g)
    nx.draw_networkx_nodes(g,pos,node_size=20)
    nx.draw_networkx_edges(g,pos,alpha=0.4)
    plt.savefig('relations.tif')
    plt.close()
    t= transitiveness_graph(g)
    pos=nx.spring_layout(t)
    nx.draw_networkx_nodes(t,pos,node_size=20)
    nx.draw_networkx_edges(t,pos,alpha=0.4)
    plt.savefig('relations_of_relations.tif')
    plt.close()
