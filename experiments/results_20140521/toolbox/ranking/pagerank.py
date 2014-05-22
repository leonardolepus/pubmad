def transitiveness_graph(g):
    #used to generate transitiveness graph of a multidigraph
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


def reverse(g):
    rg = nx.DiGraph()
    rg.add_nodes_from(g.nodes())
    for n, nbr in g.edges():
        rg.add_edge(nbr, n)
    return rg
