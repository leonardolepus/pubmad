def trans_graph(e, g):
    #calculates transitiveness of an edge in a graph
    s, t = e
    s_neighbors = g.neighbors(s)
    t_neighbors = g.neighbors(t)
    s_neighbors.remove(t)
    t_neighbors.remove(s)
    common_neighbors = [n for n in s_neighbors if n in t_neighbors]
    return len(s_neighbors and (len(t_neighbors) and 1.0 * len(common_neighbors) ** 2 / (len(s_neighbors) * len(t_neighbors))) ** 0.5

