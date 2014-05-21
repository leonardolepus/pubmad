from scipy.stats import beta


'''
in comments of this module,
a-b means there's an edge between a and b
a->b means there's a directed edge from a to b
a--b means there's a path between a and b, ignoring direction of edges
a-->b means there's a path between a and b
'''


def binom_interval(success, total, confint = 0.95):
    quantile = 1 - confint
    lower = beta.ppf(quantile, success, total - success + 1)
    #upper = beta.ppf(1 - quantile, success + 1, total - success)
    return lower
    
def trans(g, e, method = 'beta'):
    #calculates transitiveness of an edge in a graph
    #at_as = P(a-t|a-s)
    #as_at = P(a-s|a-t))
    if method == 'ratio':
        func = lambda a, b: b and 1.0 * a / b
    elif method == 'beta':
        func = binom_interval
    else:
        func = method

    s, t = e
    s_neighbors = g.neighbors(s)
    t_neighbors = g.neighbors(t)
    s_neighbors.remove(t)
    t_neighbors.remove(s)
    common_neighbors = [n for n in s_neighbors if n in t_neighbors]
    return {'at_as' : func(len(common_neighbors), len(s_neighbors)),
            'as_at' : func(len(common_neighbors), len(t_neighbors))}


def ditrans(g, e, method = 'beta'):
    #calculates transitiveness of an edge in a digraph
    #four types of transitiveness are defined, they are:
    #at_as = P(a->t|a->s)
    #as_at = P(a->s|a->t)
    #sa_ta = P(s->a|t->a)
    #ta_sa = P(t->a|s->a)
    #bt_bs = P(b-t|b-s)
    #bs_bt = P(b-s|b-t)
    if method == 'ratio':
        func = lambda a, b: b and 1.0 * a / b
    elif method == 'beta':
        func = binom_interval
    else:
        func = method

    s, t = e
    s_succ = set(g.successors(s))
    s_pred = set(g.predecessors(s))
    s_neig = s_succ | s_pred
    t_succ = set(g.successors(t))
    t_pred = set(g.predecessors(t))
    t_neig = t_succ | t_pred
    c_succ = s_succ & t_succ
    c_pred = s_pred & t_pred
    c_neig = s_neig & t_neig
    return {'at_as' : func(len(c_pred), len(s_pred)),
            'as_at' : func(len(c_pred), len(t_pred)),
            'sa_ta' : func(len(c_succ), len(t_succ)),
            'ta_sa' : func(len(c_succ), len(s_succ)),
            'bt_bs' : func(len(c_neig), len(s_neig)),
            'bs_bt' : func(len(c_neig), len(t_neig))}

