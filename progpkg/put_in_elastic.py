from elasticsearch import Elasticsearch

def putin(addWord):
    es_host="http://localhost:9200"
    es=Elasticsearch(es_host)
    
    accu_words=es.search(index='accumulated_words_dictionary', body={'query':{'match':{"accu_word":'accumulated_word'}}})
    accu_word_dict=accu_words['hits']['hits'][0]['_source']['word_dict']
    print(accu_word_dict)
    if addWord not in accu_word_dict.keys():
        accu_word_dict[addWord]=0
    accu_word_dict[addWord]+=1
    print(accu_word_dict)
    
    eee={"accu_word":'accumulated_word',
    "word_dict":accu_word_dict}
    res=es.index(index='accumulated_words_dictionary', id=1, document=eee)
    
if __name__=="__main__":
    putin("계란")