import json
import sys
import threading

from elasticsearch import Elasticsearch

# processed_text = 'service for'
# m = {'world': processed_text}
# n = json.dumps(m)
# o = json.loads(n)
# try:
#     es = Elasticsearch([{'host': '192.168.12.39', 'port': 9200}])
#     result = es.index(index="english-dictionary", doc_type='doc', body=o, id=processed_text)
# except Exception as e:
#     print(sys.exc_info()[0])
from flask import app

search_query = '{"query":{"bool":{}},"from":#counter,"size":1,"sort":[],"aggs":{}}'
index_name = 'english-dictionary'
es = Elasticsearch([{'host': '192.168.12.39', 'port': 9200}])


def clean_dict(fromval, toval):
    count = list(range(27290, 800000))
    for counter in count:
        try:
            searchQuery = str.replace(search_query, "#counter", str(counter))
            rest = es.search(index=index_name, body=searchQuery)
            data = [doc for doc in rest['hits']['hits']]
            for doc1 in data:
                processed_text = doc1['_source']['world']
                m = {'word': processed_text}
                n = json.dumps(m)
                o = json.loads(n)
                try:
                    result = es.index(index="english-dictionary-us", doc_type='doc', body=o, id=o)
                    if result['result']== 'created':
                        print(result, processed_text)
                    else:
                        print(processed_text,result['_version'])
                except Exception as e:
                    print(sys.exc_info()[0])


        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])


if __name__ == "__main__":
    # t1 = threading.Thread(target=clean_dict(27290, 100000))
    # t2 = threading.Thread(target=clean_dict(100000, 200000))
    # t3 = threading.Thread(target=clean_dict(200000, 300000))
    # t4 = threading.Thread(target=clean_dict(300000, 400000))
    # t5 = threading.Thread(target=clean_dict(400000, 500000))
    # t6 = threading.Thread(target=clean_dict(500000, 600000))
    # t7 = threading.Thread(target=clean_dict(600000, 700000))
    t8 = threading.Thread(target=clean_dict(700000, 800000))

    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    # t7.start()
    t8.start()

    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    # t6.join()
    # t7.join()
    # t8.join()
