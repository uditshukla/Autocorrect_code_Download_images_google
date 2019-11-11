import hashlib
import json
import sys

import yaml
from elasticsearch import Elasticsearch

def de_duplication(str):
    import hashlib
    hash_object = hashlib.sha256(str.encode(str))
    hex_dig = hash_object.hexdigest()
    print(hex_dig.hexdigest())
    return hex_dig

#Code to ingest Dictionary Data to local Dictionary
# with open('/home/uditshashankshukla/Desktop/words_dictionary.json') as json_file:
#     data = json.load(json_file)
#     for item in data:
#         m = { 'world': item}
#         n = json.dumps(m)
#         o = json.loads(n)
#         try:
#             es = Elasticsearch([{'host': '192.168.12.39', 'port': 9200}])
#             result = es.index(index="english-dictionary", doc_type='doc', body=o ,id=item)
#         except yaml.YAMLError as exc:
#             print(exc)
#Code to ingest Dictionary Data to local Dictionary


search_query = '{"query":{"bool":{}},"from":#counter,"size":1,"sort":[],"aggs":{}}'
index_name = 'advanced-ontology-tagged'
es = Elasticsearch([{'host': '192.168.12.39', 'port': 9200}])
count = list(range(399376))
for counter in count:
    if counter > 200000:
        try:
            searchQuery = str.replace(search_query, "#counter", str(counter))
            rest = es.search(index=index_name, body=searchQuery)
            data = [doc for doc in rest['hits']['hits']]
            for doc1 in data:
                processed_text = doc1['_source']['article']['ontology']
                m = {'world': processed_text}
                n = json.dumps(m)
                o = json.loads(n)
                try:
                    es = Elasticsearch([{'host': '192.168.12.39', 'port': 9200}])
                    result = es.index(index="english-dictionary", doc_type='doc', body=o, id=counter)
                except Exception as e:
                        print(sys.exc_info()[0])


        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])