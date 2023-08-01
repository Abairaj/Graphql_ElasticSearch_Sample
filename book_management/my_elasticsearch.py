from elasticsearch import Elasticsearch
# creating connection with elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# defining document data

doc = {
    'title': 'Aadujeevitham',
    'content': 'The novel written by Benyamin'
}


# index the document

es.index(index='my_index', id=1, body=doc)


# searching the document

# define search query
query = {
    'query': {
        'match': {
            'name': 'Benyamin'
        }
    }
}


# search for documents
result = es.search(index='my_index', body=query)
print(result)
