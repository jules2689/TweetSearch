from sets import Set
import re, string
import os

class Preprocessing:

  def preprocess(self):
    text = open(self.path('data.txt'), 'r').read()
    text = text.encode('utf-8','replace')

    print "Processing Text..."
    tweets = self.process_text(text)
    print "Finished Processing Text..."
    return tweets

  def process_text(self, text):
    print "Removing punctuation..."
    text = self.remove_punctuation(text)
    return text.split("\n")

  def remove_punctuation(self, text):
    table = string.maketrans("","")
    return text.translate(table, string.punctuation)

  def stops(self):
    stops = Set()
    file = open(self.path('stops.txt'), 'r')
    for stop in file:
      stops.add(stop.replace("\n",""))
    return stops

  def path(self, file_name):
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)
    return directory + "/" + file_name