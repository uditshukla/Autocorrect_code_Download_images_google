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

search_query = '{"query":{"bool":{}},"from":#counter,"size":100000,"sort":[],"aggs":{}}'

index_name = 'english-dictionary'
es = Elasticsearch([{'host': '192.168.12.39', 'port': 9200}])


def clean_dict(fromval, toval):
    count = list(range(fromval, toval, 100000))
    for counter in count:
        try:
            searchQuery = str.replace(search_query, "#counter", str(counter))
            rest = es.search(index=index_name, body=searchQuery)
            data = [doc for doc in rest['hits']['hits']]
            for doc1 in data:
                processed_text = doc1['_source']['world']
                w_search_query = '{"query":{"bool":{"must":[{"term":{"word.keyword":"' + processed_text + '"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}'
                w_search_response = es.search(index='english-dictionary-us', body=w_search_query)
                data1 = w_search_response['hits']['total']

                if data1 == 1:
                    print('trap', counter , processed_text)
                else:
                    m = {'word': processed_text}
                    n = json.dumps(m)
                    o = json.loads(n)
                    try:
                        result = es.index(index="english-dictionary-us", doc_type='doc', body=o, id=o)
                        if result['result'] == 'created':
                            print(result, processed_text)
                        else:
                            print(processed_text, result['_version'])
                    except Exception as e:
                        print(sys.exc_info()[0])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])

    # counter += 1000


if __name__ == "__main__":
    # t1 = threading.Thread(target=clean_dict(27290, 100000))
    t2 = threading.Thread(target=clean_dict(200000, 800000))
    # t3 = threading.Thread(target=clean_dict(200000, 300000))
    # t4 = threading.Thread(target=clean_dict(300000, 400000))
    # t5 = threading.Thread(target=clean_dict(400000, 500000))
    # t6 = threading.Thread(target=clean_dict(500000, 600000))
    # t7 = threading.Thread(target=clean_dict(600000, 700000))
    # t8 = threading.Thread(target=clean_dict(10000, 800000))
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    # t7.start()
    # t8.start()
    #
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    # t6.join()
    # t7.join()
    # t8.join()
