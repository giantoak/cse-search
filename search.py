#!/usr/bin/python

import requests
from lxml import etree
import sys

api_key = ''
cses = {
        'popular': ['015103381357823281146:kiuelzzaubo',
            '015103381357823281146:gsblggetojm'],
        'russian_forums': ['015103381357823281146:9axbw_q6hny',
            '015103381357823281146:i9c4sed-izm'],
        'dating': ['015103381357823281146:oo7sq2bqwjo']
        }

def make_document_trees(query, documents):
    sys.stderr.write(str(len(documents)) + '\n')
    root = etree.Element('searchresult')
    qelem = etree.Element('query')
    qelem.text = query
    root.append(qelem)
    i = 0
    for r in documents:
        doc = etree.Element('document', id=str(i))
        
        # Create XML nodes
        title_elem = etree.Element('title')
        title_elem.text = r['title']
        url_elem = etree.Element('url')
        url_elem.text = r['link']
        snippet_elem = etree.Element('snippet')
        snippet_elem.text = r['snippet']

        doc.append(title_elem)
        doc.append(url_elem)
        doc.append(snippet_elem)

        i += 1
        root.append(doc)

    return root

def google_to_carrot2(query, results):
    ''' Reformats Google API search results in Carrot2 input XML '''
    
    docs = []
    for result in results:
        try:
            docs.extend(result['items'])
        except KeyError:
            continue
    
    tree = make_document_trees(query, docs)
    return etree.tostring(tree)

def make_google_query(cse, api_key, query, offset=0):
    ''' Make a Google Custom Search API query:
        
        cse - custom search engine ID
        api_key - google custom search api key
        query - search query
        offset - starting page'''

    search_string = "https://www.googleapis.com/customsearch/v1?key={api}&cx={cse_id}&q={query}&lowRange={offset}&highRange={offset2}"
    q = search_string.format(api=api_key, cse_id=cse, query=query, offset=offset,
            offset2=offset+10)

    r = requests.get(q)
    
    return r.json()


# Read input from command line 
query_str = sys.argv[1]

results = []
for c in cses['popular'] + cses['dating']:
    result = make_google_query(c, api_key, query_str)
    
    results.append(result)
    
    # Do two searches if there are enough results
    if int(result['searchInformation']['totalResults']) > 20:
        result = make_google_query(c, api_key, query_str, 10)
        results.append(result)

c2 = google_to_carrot2(query_str, results)
sys.stdout.write(c2)
