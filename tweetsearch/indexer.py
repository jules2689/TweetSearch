#!/usr/bin/env python
# coding=utf-8
import pdb
import os

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from whoosh import scoring
from whoosh import qparser

import preprocessing as Preprocessing

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

class Indexer:
  def __init__(self):
    self.tweets = []
    self.preprocessor = Preprocessing.Preprocessing()
    #Stemmer also stems the query content
    stop_words = self.preprocessor.stops()
    analyzer = StemmingAnalyzer(stoplist=stop_words)
    analyzer.cachesize = -1 # Unbounded caching, but worse memory performance
    file("results.txt", "w")
    file("topResults.txt", "w")
    
    self.schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True, analyzer=analyzer))

  def run(self):
    self.tweets = self.preprocessor.preprocess()

    if not os.path.exists("tweetsearch/indexdir"):
      os.mkdir("tweetsearch/indexdir")
    self.index = self.whoosh_it()

  def query(self, search_query_num, search_query):
    qp = QueryParser("content", schema=self.schema, group=qparser.OrGroup)
    q = qp.parse(search_query)

    with self.index.searcher(weighting=scoring.TF_IDF()) as searcher:
      results = searcher.search(q, limit=1000)
      reader = self.index.reader()
      self.print_results_to_file(search_query_num, search_query, results)
      self.print_top_query_results(search_query_num, search_query, results)

  def print_results_to_file(self, queryNum, query, results):
    with open("results.txt", "a") as f: 
      for hit in results:
        f.write('%s Q0 %s %d %f awesomenessRun\n' % (queryNum, hit["title"], hit.rank, hit.score))

  def print_top_query_results(self, queryNum, query, results):
    if (queryNum == 1) or (queryNum == 25):
      with open("topResults.txt", "a") as f:

        f.write('Results for query: %s, %s\n' % (queryNum, query))

        for hit in results:
          if hit.rank < 10:
            f.write('#%d: %s with score = %d\n' % (hit.rank + 1, hit["content"], hit.score))
        f.write('\n')


  def whoosh_it(self):
    print "Building Index..."

    ix = create_in("tweetsearch/indexdir", self.schema)
    writer = ix.writer()

    # Add all tweets as documents with title = tweet number
    for tweet in self.tweets:
      tweet = tweet.split("\t")
      tweetNum = tweet[0]
      tweetContent = tweet[1]
      writer.add_document(title=u(tweetNum), content=u(tweetContent))

    writer.commit()
    print "Done building index"
    return ix
