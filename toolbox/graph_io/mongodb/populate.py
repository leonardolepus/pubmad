import pymongo
from pymongo import MongoClient

ADDR = 'localhost'
PORT = 27017
term_tag = {}

client = MongoClient(ADDR, PORT)
db = client['pubmad']
coll = db['graph']
posts = []
for line in sys.stdin:
    line = line.stripe()
    edge, ref = line.split('\t')
    source, target = edge.split('==')
    ref = ref.split(';;')
    post = {'source' : source,
            'source_tags' : term_tag.get(source, []),
            'target' : target,
            'target_tags' : term_tag.get(target, []),
            'edge_tags' : [],
            'refs' : ref,
            'weight' : len(ref)}
    posts.append(post)
    if len(posts) > 100:
        coll.insert(posts)    #if error, pickle dump posts, upsert later
        posts = []
if posts:
    coll.insert(posts)    #if error, pickle dump posts, upsert later
