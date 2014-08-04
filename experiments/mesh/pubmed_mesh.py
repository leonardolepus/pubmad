import sys, pickle

from Bio import Entrez

Entrez.email = 'codefetcher@gmail.com'

def retrieve_index(mesh, retmax = 10000):
    try:
        handle = Entrez.esearch(db = 'pubmed', term = '''"%s"[Mesh]''' % (mesh, ), retmode = 'text')
        records = Entrez.read(handle)
        handle.close()
        records_number = int(records['Count'])
        print 'term = %s, has %d records' % (mesh, records_number)
    except:
        print 'term = %s, failed to retrieve records number' % (mesh, ), sys.exc_info()
        return 0
    uids = []
    failed_batches = []
    for retstart in range(0, records_number, retmax):
        for i in range(10):
            try:
                handle = Entrez.esearch(db = 'pubmed', term = '''"%s"[Mesh]''' % (mesh, ), retstart = retstart, retmax = retmax, retmode = 'text')
                records = Entrez.read(handle)
                handle.close()
                uids = uids + records['IdList']
                print 'mesh = %s, batch = %d, success' % (mesh, retstart)
                break
            except:
                if i == 9:
                    failed_batches.append(retstart)
                    print 'mesh = %s, batch = %d, fail' % (mesh, retstart), sys.exc_info()
    return [uids, failed_batches]
                    

if __name__ == '__main__':
    with open('mesh_list', 'r') as f:
        terms = pickle.load(f)
    failed_terms = []
    for term in terms:
        ret = retrieve_index(term)
        if not ret:
            failed_terms.append(term)
        else:
            [uids, failed_batches] = ret
            if failed_batches:
                failed_terms.append(term)
            else:
                print uids
        break
