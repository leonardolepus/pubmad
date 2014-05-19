import csv
import networkx as nx


def import_nodes(g, syno_f):
    #add node from syno_f
    before = g.number_of_nodes()
    with open(syno_f, 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter = '\t')
        for entrezgene_id, symbol_type, symbol in reader:
            entrezgene_id = int(entrezgene_id)
            if g.has_node(entrezgene_id):
                names = g.node[entrezgene_id].get('names', [])
            else:
                names = []
            names.append(symbol)
            attr = {}
            attr['names'] = names
            if symbol_type == 'official_symbol':
                attr['name'] = symbol
            g.add_node(entrezgene_id, attr)
        f.close()
        after = g.number_of_nodes()
        print after - before, 'nodes imported'


def import_edges(g, rel_f):
    #add edge from rel_f
    before = g.number_of_edges()
    ebunch = []
    with open(rel_f,'r') as f:
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
    after = g.number_of_edges()
    print after - before, 'edges imported'
    
def import_graph(g, syno_f, rel_f):
    import_nodes(g, syno_f)
    import_edges(g, rel_f)
    print 'graph has', g.number_of_nodes(), 'nodes'
    print 'graph has', g.number_of_edges(), 'edges'
    return g


if __name__ == '__main__':
    syno_f = '../../../data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
    rel_f = '../../../data/evex/Homo_Sapiens/EVEX_relations_9606.tab'
    graph = import_graph(nx.DiGraph(species = "Homo_Sapiens"), syno_f, rel_f)
    
