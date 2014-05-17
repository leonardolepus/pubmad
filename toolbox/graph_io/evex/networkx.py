import copy
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import time
import operator


def import_as_graph(file):
    g = nx.Graph()
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
        f.close()
    g.add_edges_from(ebunch)
    print 'a MultiDiGraph is constructed'
    print 'graph has', g.number_of_nodes(), 'nodes'
    print 'graph has', g.number_of_edges(), 'edges'
    return g


def import_as_digraph(synonyms_file, relations_file):
    pass


def import_as_multidigraph(synonyms_file, relations_file):
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


