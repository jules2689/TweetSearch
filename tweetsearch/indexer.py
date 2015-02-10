#!/usr/bin/env python
# coding=utf-8
import pdb
import os

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from whoosh import scoring

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
    self.schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True, analyzer=StemmingAnalyzer(stoplist=stop_words)))

  def run(self):
    self.tweets = self.preprocessor.preprocess()

    if not os.path.exists("tweetsearch/indexdir"):
      os.mkdir("tweetsearch/indexdir")
    self.index = self.whoosh_it()

  def query(self, search_query_num, search_query):
    qp = QueryParser("content", schema=self.schema)
    q = qp.parse(search_query)

    with self.index.searcher(weighting=scoring.TF_IDF()) as searcher:
      results = searcher.search(q, limit=1000)
      reader = self.index.reader()
      self.print_results(search_query_num, search_query, results)

  def print_results(self, queryNum, query, results):
    for hit in results:
      print queryNum, " Q0 ", hit["title"], " ", hit.rank, " ", hit.score, " awesomenessRun"

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
