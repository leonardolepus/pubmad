def import_evex(gtype = 'graph', connected = True):
    import networkx as nx
    from toolbox.graph_io.evex.nx import import_graph
    syn_f = 'data/evex/Homo_Sapiens/EVEX_synonyms_9606.tab'
    rel_f = 'data/evex/Homo_Sapiens/EVEX_relations_9606.tab'
    if gtype == 'graph':
        g = nx.Graph()
    elif gtype == 'digraph':
        g = nx.DiGraph()
    elif gtype == 'multidigraph':
        g = nx.MultiDiGraph()
    g = import_graph(g, syn_f, rel_f)
    if connected:
        if g.is_directed():
            isolated_nodes = [n for n in g.nodes_iter() if not g[n] and not g.predecessors(n)]
        else:
            isolated_nodes = [n for n in g.nodes_iter() if not g[n]]
        g.remove_nodes_from(isolated_nodes)
    print 'g has', g.number_of_nodes(), 'nodes'
    print 'g has', g.number_of_edges(), 'edges'
    return g


def load_evex(gtype = 'graph'):
    import pickle
    if gtype == 'graph':
        pickle_f = 'data/evex/Homo_Sapiens/evex_graph.graph'
    elif gtype == 'digraph':
        pickle_f = 'data/evex/Homo_Sapiens/evex_digraph.graph'
    with open(pickle_f, 'r') as f:
        g = pickle.load(f)
    print 'g has', g.number_of_nodes(), 'nodes'
    print 'g has', g.number_of_edges(), 'edges'
    return g


def import_kegg(gtype = 'digraph'):
    from toolbox.graph_io.kegg.parse_KGML import KGML2Graph
    pathway_f = 'data/kegg/hsa04151.xml'
    return KGML2Graph(pathway_f)

if __name__ == '__main__':
    evex = import_evex()
    evex = load_evex()
    kegg = import_kegg()
