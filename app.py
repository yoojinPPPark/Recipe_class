#!/usr/bin/python

from unittest import result
from flask import Flask, render_template, request
from progpkg import crawl, analysis, elastic, put_in_elastic

app = Flask(__name__)

@app.route('/') # 접속url

def index():
  topword=elastic.get_top_word()
  return render_template('home.html', result1=topword[0], result2=topword[1], result3=topword[2], result4=topword[3], result5=topword[4])
  
@app.route('/search', methods = ["POST", "GET"]) #second page
def recipe():
  if request.method == "POST":
    addSource = request.form["include"]
    
    put_in_elastic.putin(addSource) # 검색어 elasticsearch에 집어넣기
    
    subList = list(request.form["exclude"].split())
    word_i = crawl.crawl(addSource, subList)
    tfidf = []
    for res in word_i:
      tfidf.append(analysis.analysisTFIDF(res['recipe']))
  return render_template('search.html', addSource = addSource, subList = subList, tfidf = tfidf, word_i = word_i)

if __name__=="__main__":
  app.run(debug=True)
