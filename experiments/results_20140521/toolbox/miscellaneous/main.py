import copy
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import time
import operator





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



    
def save_data(obj, path):
    f = open(path, 'w')
    pickle.dump(obj, f)
    f.close()


def process_data():
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


conf_pr_in = open('data/Homo_Sapiens/conf_pr', 'r')
conf_pr = pickle.load(conf_pr_in)
conf_pr_out = open('data/Homo_Sapiens/conf_pr.tab', 'w')
for event_id in conf_pr:
    conf_pr_out.write(str(event_id) + ', ' + str(conf_pr[event_id]) + '\n')
conf_pr_out.close()

pre_pr_in = open('data/Homo_Sapiens/pre_pr', 'r')
pre_pr = pickle.load(pre_pr_in)
pre_pr_out = open('data/Homo_Sapiens/pre_pr.tab', 'w')
for event_id in pre_pr:
    pre_pr_out.write(str(event_id) + ', ' + str(pre_pr[event_id]) + '\n')
pre_pr_out.close()

t_in = open('data/Homo_Sapiens/t', 'r')
t = pickle.load(t_in)

g_in = open('data/Homo_Sapiens/g', 'r')
g = pickle.load(g_in)

sorted_conf_pr = sorted(conf_pr.iteritems(), key = operator.itemgetter(1), reverse = True)
sorted_pre_pr = sorted(pre_pr.iteritems(), key = operator.itemgetter(1), reverse = True)


def find_downstream(gr, root, depth, known = []):
    if not depth or not gr[root]:
        return [root]
    else:
        nbunch = [root]
        for i in gr[root].keys():
            if i not in known:
                nbunch = nbunch + find_downstream(gr, i, depth -1, nbunch)
        return nbunch


akt_d = find_downstream(g, 207, 1)
akt_sub = nx.subgraph(g, akt_d)

for node in conf_pr:
    t.node[node]['conf_pr'] = conf_pr[node]
    source = t.node[node]['source']
    target = t.node[node]['target']
    g.edge[source][target][0]['conf_pr'] = conf_pr[node]

for node in pre_pr:
    t.node[node]['pre_pr'] = pre_pr[node]
    source = t.node[node]['source']
    target = t.node[node]['target']
    g.edge[source][target][0]['pre_pr'] = pre_pr[node]

plot(akt_sub, 'akt_sub')

nx.write_edgelist(g, 'data/Homo_Sapiens/g_edgelist', delimiter = ', ')
nx.write_edgelist(t, 'data/Homo_Sapiens/t_edgelist', delimiter = ', ')

nlrp3 = find_downstream(g, 114548, 1)
nlrp3_sub = nx.subgraph(g, nlrp3)
nlrp3_ebunch = [nlrp3_sub[n1][n2][0]['general_event_id'] for n1, n2 in nlrp3_sub.edges()]
nlrp3_t = nx.subgraph(t, nlrp3_ebunch)

def rank_paths(g, source):
    targets_attr = [(target, g[source][target][0]) for target in g[source].keys()]
    targets = [(target, target_attr['pre_pr']) for target, target_attr in targets_attr]
    sorted_targets = sorted(targets, key = lambda x: x[1])
    sorted_targets.reverse()
    print sorted_targets

akt = rank_paths(g, 207)
