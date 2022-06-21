#!/usr/bin/python
import re
import requests
from konlpy.tag import Kkma
from konlpy.utils import pprint
from elasticsearch import Elasticsearch
import math
from nltk import word_tokenize

es_host="http://localhost:9200"
sent_list=[]
word_d={}

def process_new_sentence(s):
    sent_list.append(s)
    splited = s.split(' ')
    for word in splited:
        if word not in word_d.keys():
            word_d[word]=0
        word_d[word]+=1

def compute_tf(s):
    bow=set()
    wordcount_d={}
    
    splited = s.split(' ')
    for spl in splited:
        if spl not in wordcount_d.keys():
            wordcount_d[spl]=0
        wordcount_d[spl]+=1
        bow.add(spl)
    
    tf_d={}
    for word, cnt in wordcount_d.items():
        tf_d[word]=cnt/float(len(bow))
        
    return tf_d

def compute_idf():
    Dval = len(sent_list)
    bow=set()
    
    for ii in range(0, len(sent_list)):
        splited=sent_list[ii].split(' ')
        for sp in splited:
            bow.add(sp)
            
    idf_d={}
    for tt in bow:
        cnt=0
        for ss in sent_list:
            if tt in ss.split(' '):
                cnt+=1
        idf_d[tt]=math.log(Dval/float(cnt))
    return idf_d

def analysisTFIDF(recipe):
    #1. RECIPE TEXT를 받아오면 명사만 추출해서 str만들기
    hfi_str=re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+', '', recipe)
    kkma=Kkma()
    sentence=''
    wlist=kkma.pos(hfi_str)
    for w in wlist:
        if w[1] =="NNG":
            sentence+=w[0]+' '
    #print(sentence)
    
    #2. ElasticSearch에서 word dict가져오기
    es=Elasticsearch(es_host)
    control_words=es.search(index='control_words2', body={'query':{'match':{"control_word":'control'}}})
    control_word_list=control_words['hits']['hits'][0]['_source']['word_list']

    #3. TFIDF 계산하기
    for ee in range(0,4,1):
        process_new_sentence(control_word_list[ee])
    process_new_sentence(sentence)
    
    idf_d=compute_idf()

    tf_d=compute_tf(sentence)
    tf_idf_d={}
    for word, tfval in tf_d.items():
        tf_idf_d[word]=tfval*idf_d[word]
        #print(word, tfval*idf_d[word])
        
    tfidf_dict = dict(sorted(tf_idf_d.items(), key=lambda x: x[1], reverse=True))
    nn=0
    top10_d={}
    for key, val in tfidf_dict.items():
        top10_d[key]=val
        nn+=1
        if(nn==10):
            break
    print(top10_d)

    #4. SCORE높은 TOP10개 단어를 RETURN
    return top10_d
    
if __name__=='__main__':
    #두부닭가슴살유부초밥 재료
    recipe='냉동 (or 훈제)닭가슴살을 삶아서 찢어준다 찢은 닭가슴살 작게 잘라준다(가위나 칼 사용) 유부에 들어가니깐 기호대로 크기는 알아서^^ 두부를 물에 데쳐서 건진 다음 자른 닭가슴살과 함께 버무린다 이때 소금이나 후추로 조금 간을 해요 버물버물/ 잘 두부랑 닭가슴살이 섞이도록 무쳐주세요 유부초밥 안에 있는 후레이크와 소스 넣아주세요 다시 버물려줍니다 잘 버물려지면 유부의 물기를 짜서 두부닭가슴살을 유부안에 담아줍니다 완성!'
    analysisTFIDF(recipe)
    