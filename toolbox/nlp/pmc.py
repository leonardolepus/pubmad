import xml.etree.ElementTree as xet
import itertools

import nltk
import networkx as nx
import matplotlib.pyplot as plt

f = '''../../../Google_Drive/Projects/pubmad/data/pmc/Autophagy/Autophagy_2013_Sep_1_9(9)_1418-1430.nxml'''
tree = xet.parse(f)
root = tree.getroot()
abstract = root.find('.//abstract')
ab_texts = []
for p in abstract:
    ab_texts.append(p.text)
    for child in p:
        if child.tag in ['italic']:
            ab_texts.append(child.text)
            ab_texts.append(child.tail)
ab_text = ' '.join(ab_texts)
print ab_text

bd_texts = []
body = root.find('.//body')
for p in root.find('.//body')[0]:
    bd_texts.append(p.text)
    for child in p:
        if child.tag in ['italic']:
            bd_texts.append(child.text)
            bd_texts.append(child.tail)

bd_texts = [p for p in bd_texts if p is not None]
bd_text = ' '.join(bd_texts)

def to_graph(s):
    sents = nltk.sent_tokenize(s)
    sw = nltk.corpus.stopwords.words('english')
    g = nx.Graph()
    for sent in sents:
        words = nltk.word_tokenize(sent)
        clean_words = [w for w in words if w not in sw]
        edges = [e for e in itertools.combinations(clean_words, 2)]
        g.add_edges_from(edges)
    print 'g has %d nodes and %d edges' % (g.number_of_nodes(), g.number_of_edges())
    return g

ab_graph = to_graph(ab_text)
bd_text = to_graph(bd_text)


nx.draw(ab_graph)
plt.show()

nx.draw(ab_graph)
plt.show()

dgr = nx.degree(g)
clst = nx.clustering(g)

for s, t in g.edges_iter():
    
