#used to retrieve mesh terms from pubmed and construct a network

from Bio import Entrez, Medline

EMAIL = 'leonardolepus@gmail.com'
keywords = 'hydrogen sulfide[Mesh]'

Entrez.email = EMAIL
handle = Entrez.esearch(db = 'pubmed', term = keywords, retmax = 10000000, retmode = 'text')
records = Entrez.read(handle)
handle.close()
#for id in records['IdList']:
#id = records['IdList'][0]
id = '24912238'
handle = Entrez.efetch(db = 'pubmed', id = id, retmode = 'xml')
entre = Entrez.read(handle)
try:
    mesh = [m['DescriptorName'] for m in entre[0]['MedlineCitation']['MeshHeadingList']]
    add_to_graph(mesh, g)
except KeyError:
    pass

def add_to_graph(entity_list, g):
    
