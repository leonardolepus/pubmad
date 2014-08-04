#used to retrieve mesh terms from pubmed and construct a network
import itertools

import matplotlib.pyplot as plt
import networkx as nx
from Bio import Entrez


EMAIL = 'leonardolepus@gmail.com'


def retrieve_graph_from_query(query, graph, max_records = null):
    Entrez.email = EMAIL
    #get number of records
    handle = Entrez.esearch(db = 'pubmed', term = query, retmode = 'text')
    records = Entrez.read(handle)
    handle.close()
    records_number = records['Count']
    #get uids
    handle = Entrez.esearch(db = 'pubmed', term = query, retmax = records_number, retmode = 'text')
    records = Entrez.read(handle)
    handle.close()
    uids = records['IdList']
    if max_records > 0:
        uids = uids[0:max_records] if max_records < len(uids) else uids
    for uid in uids:
        handle = Entrez.efetch(db = 'pubmed', id = uid, retmode = 'xml')
        entre = Entrez.read(handle)
        handle.close()
        try:
            mesh = [str(m['DescriptorName']) for m in entre[0]['MedlineCitation']['MeshHeadingList']]
            edge_list = [e for e in itertools.combinations(mesh, 2)]
            graph.add_edges_from(edge_list)
            print 'retrieved %d of %d' % (uids.index(uid) + 1, len(uids))
        except KeyError:
            pass


def retrieve_bin_occr(entity1, entity2, field1 = ' ', field2 = ' '):
    Entrez.email = EMAIL
    query = '''"%s"[%s] AND "%s"[%s]''' % (entity1, field1, entity2, field2)
    print query
    handle = Entrez.esearch(db = 'pubmed', term = query, retmode = 'text')
    records = Entrez.read(handle)
    handle.close()
    records_number = int(records['Count'])
    print records_number
    return records_number


def retrieve_graph_from_entities(entities, graph):
    for e1, e2 in itertools.combinations(entities, 2):
        occr = retrieve_bin_occr(e1, e2)
        edge_list = [(e1, e2) for i in range(occr)]
        graph.add_edges_from(edge_list)


def retrieve_index_from_uid(uid, corpus):
    Entrez.email = EMAIL
    handle = Entrez.efetch(db = 'pubmed', id = uid, retmode = 'xml')
    entre = Entrez.read(handle)
    handle.close()
    try:
        mesh = [str(m['DescriptorName']) for m in entre[0]['MedlineCitation']['MeshHeadingList']]
        corpus[uid] = mesh
        print 'retrieved %s' % (uid, )
        return 1
    except KeyError:
        print '%s is not index, skipped' % (uid, )
        return 0

    
if __name__ == '__main__':        
    g = nx.MultiGraph()
    query = 'hydrogen sulfide[Mesh]'
    retrieve_graph_from_query(query, g)
    print 'graph has %d nodes, %d edges' % (g.number_of_nodes(), g.number_of_edges())
    nx.draw(g)
    plt.show()

    entities = ['hydrogen sulfide', "alzheimer's", "parkinson's", 'stroke', 'inflammation', 'apoptosis']
    g = nx.MultiGraph()
    retrieve_graph_from_entities(entities, g)
    nx.draw(g, with_lables = True)
    plt.show()


    #construct list of uids
    Entrez.email = EMAIL
    handle = Entrez.esearch(db = 'pubmed', term = '''("1900"[Date - MeSH] : "3000"[Date - MeSH])''', retmode = 'text')
    records = Entrez.read(handle)
    handle.close()
    count = int(records['Count'])
    for retstart in range(10000000, count, 100000):
        handle = Entrez.esearch(db = 'pubmed', term = '''("1900"[Date - MeSH] : "3000"[Date - MeSH])''', retstart = retstart, retmax = 100000, retmode = 'text')
        records = Entrez.read(handle)
        handle.close()
        uids = records['IdList']
        for uid in uids:
            if retrieve_index_from_uid(uid, corpus):
                break
        break


