#!/usr/bin/env python
# coding=utf-8
import nltk
from nltk.corpus import stopwords
import re, string
import os
import pdb

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

class WordDistribution:
  def __init__(self):
    self.tweets = []
    self.stops = self.stops()
    self.schema = Schema(title=TEXT(stored=True), content=TEXT)

  def run(self):
    self.setup_text()
    if not os.path.exists("indexdir"):
      os.mkdir("indexdir")
    index = self.whoosh_it()
    query = "world"
    self.whoosh_query_index(index, query)

  def setup_text(self):
    text = open(self.path('data.txt'), 'r').read()
    text = text.encode('utf-8','replace')

    print "Processing Text..."
    self.tweets = self.process_text(text)
    print "Finished Processing Text..."

  def process_text(self, text):
    print "Removing punctuation..."
    text = self.remove_punctuation(text)
    return text.split("\n")

  def remove_punctuation(self, text):
    table = string.maketrans("","")
    return text.translate(table, string.punctuation)

  def valid_word(self, word):
    valid = len(word) > 3
    valid = valid and word.lower() not in self.stops
    return valid

  def present_distribution(self):
    fdist = FreqDist(self.tweets)
    print fdist.most_common(100)

  def whoosh_it(self):
    print "Building Index..."

    ix = create_in("indexdir", self.schema)
    writer = ix.writer()

    # Add all tweets as documents with title = tweet number
    for tweet in self.tweets:
      tweetNum = tweet.split(" ")[0]
      tweetContent = tweet.split(" ")[1:]
      tweetContent = " ".join(self.process_word_list(tweetContent))
      writer.add_document(title=u(tweetNum), content=u(tweetContent))

    writer.commit()
    print "Done building index"
    return ix

  def whoosh_query_index(self, index, query):
    print "Starting query"
    # Make a search on the index:
    with index.searcher() as searcher:
     query = QueryParser("content", index.schema).parse(query)
     results = searcher.search(query)
     for result in results:
        print result
    print "Done query"

  def process_word_list(self, words):
    return [w for w in words if self.valid_word(w)]

  def stops(self):
    stops = set(stopwords.words('english'))
    file = open(self.path('stops.txt'), 'r')
    for stop in file:
      stops.add(stop.replace("\n",""))
    return stops

  def path(self, file_name):
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)
    return directory + "/" + file_name
