#!/usr/bin/env python
# coding=utf-8

import nltk
from nltk.book import *
from nltk.corpus import stopwords
import re, string
import os
import pdb

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

class WordDistribution:
  def __init__(self):
    self.words = []
    self.stops = self.stops()

  def path(self, file_name):
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)
    return directory + "/" + file_name

  def stops(self):
    stops = set(stopwords.words('english'))
    file = open(self.path('stops.txt'), 'r')
    for stop in file:
      stops.add(stop.replace("\n",""))
    return stops

  def remove_punctuation(self, text):
    table = string.maketrans("","")
    return text.translate(table, string.punctuation)

  def process_text(self, text):
    print "Replacing NewLines..."
    text = text.replace("\n"," ")
    print "Removing punctuation..."
    text = self.remove_punctuation(text)
    return text.split(" ")

  def valid_word(self, word):
    valid = len(word) > 3
    valid = valid and word.lower() not in self.stops
    return valid

  def process_word_list(self, words):
    print "Processing valid words (stop words, alpha only words)..."
    return [w for w in words if self.valid_word(w)]

  def present_distribution(self):
    fdist = FreqDist(self.words)
    print fdist.most_common(100)

  def setup_text(self):
    text = open(self.path('data.txt'), 'r').read()
    text = text.encode('utf-8','replace')

    print "Processing Text..."
    text = self.process_text(text)
    self.words += self.process_word_list(text)
    print "Finished Processing Text..."

  def run(self):
    self.setup_text()
    self.present_distribution()
