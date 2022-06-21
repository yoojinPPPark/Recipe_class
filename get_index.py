#!/usr/bin/python

import sys
from elasticsearch import Elasticsearch

es_host="http://localhost:9200"
es=Elasticsearch(es_host)
    
index_list=[]
index_list=es.indices.get(index='*')
index_list=sorted(index_list, reverse=True)
    
if "control_words2" in index_list:
    print("yes")
else:
    print("no")