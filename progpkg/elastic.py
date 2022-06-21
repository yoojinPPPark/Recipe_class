#!/usr/bin/python
from elasticsearch import Elasticsearch

def get_top_word():
    es_host="http://localhost:9200"
    es = Elasticsearch(es_host)
    
    accu_words=es.search(index='accumulated_words_dictionary', body={'query':{'match':{"accu_word":'accumulated_word'}}})
    accu_word_dict=accu_words['hits']['hits'][0]['_source']['word_dict']
    top_word_d = dict(sorted(accu_word_dict.items(), key=lambda x:x[1], reverse=True))
    print(top_word_d)
    top_list=[]
    cnt=0
    for item in top_word_d.keys():
        top_list.append(item)
        cnt+=1
        if(cnt>=5):
            break
    return top_list

if __name__=="__main__":
    top_list=get_top_word()
    print(top_list)