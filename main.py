import csv
import networkx as nx
import matplotlib.pyplot as plt


def construct_graph(file):
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
            edge = (source, target, {'confidence' : confidence,
                                     'negation' : negation,
                                     'speculation' : speculation,
                                     'coarse_type' : coarse_type,
                                     'coarse_polarity' : coarse_polarity,
                                     'refined_type' : refined_type,
                                     'refined_polarity' : refined_polarity})
            g.add_edge(source, target, object = event_id, confidence = confidence, negation = negation, speculation = speculation, coarse_type = coarse_type, coarse_polarity = coarse_polarity, refined_type = refined_type, refined_polarity = refined_polarity)
    print 'a MultiDiGraph is constructed'
    print 'graph has', g.number_of_nodes(), 'nodes'
    print 'graph has', g.number_of_edges(), 'edges'
    return g


