import os, sys, pickle, time

from Bio import Entrez

Entrez.email = 'codefetcher@gmail.com'
batch_size = 100

def fetch_batch(webenv, query_key, retstart, retmax = batch_size):
    for i in range(10):
        try:
            handle = Entrez.esearch(db = 'pubmed', term = '', WebEnv = webenv, query_key = query_key, retstart = retstart,  retmax = retmax, retmode = 'text', usehistory = 'y')
            records = Entrez.read(handle)
            handle.close()
            uids = records['IdList']
            print 'batch starting with', retstart, 'fetched'
            return uids
        except:
            if i == 9:
                print retstart, sys.exc_info()
                return 0

def fetch_doc(uids, batch):
    for i in range(10):
        try:
            handle = Entrez.efetch(db = 'pubmed', id = uids, retmode = 'xml')
            content = handle.read()
            handle.close()
            with open('./pubmed_batches/%s.xml' % (batch, ), 'w') as f:
                f.write(content)
            print 'docs in batch', batch, 'fetched'
            return 1
        except:
            if i == 9:
                print 'docs in batch', batch, 'failed', sys.exc_info()
                return 0
    
    
#get uids
handle = Entrez.esearch(db = 'pubmed', term = '''("1900/01/01"[Date - Publication] : "3000"[Date - Publication])''', retmax = 10, retmode = 'text', usehistory = 'y')
records = Entrez.read(handle)
handle.close()
count = int(records['Count'])
webenv = records['WebEnv']
query_key = records['QueryKey']

t = time.time()
failed_batches = []
for retstart in range(0, count, batch_size):
    uids = fetch_batch(webenv, query_key, retstart, batch_size)
    if not uids:
        failed_batches.append(retstart)
        break
    else:
        ret = fetch_doc(uids, retstart)
        if not ret:
            failed_batches.append(retstart)
        else:
            print time.time() - t
