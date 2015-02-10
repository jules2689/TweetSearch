#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import os
import indexer as Indexer

class BatchRunQueries:

	def __init__(self):
		self.queryNums = []
		self.queryTexts = []

	def run(self):
		self.extract_queries()
		idx = Indexer.Indexer()
		idx.run()

		print "Running Queries on index:"
		i = 0
		for query in self.queryTexts:
			idx.query(self.queryNums[i], query)
			i += 1

	def path(self, file_name):
		full_path = os.path.realpath(__file__)
		directory = os.path.dirname(full_path)
		return directory + "/" + file_name

	def extract_queries(self):
		print "Extracting queries from file..."
		text = open(self.path('topics_MB1-50.txt'), 'r').read()
		soup = BeautifulSoup(text)

		for nums in soup.find_all('num'):
			num = int(nums.string.split(" ")[2].replace("MB",""))
			self.queryNums.append(num)

		for text in soup.find_all('title'):
			self.queryTexts.append(text.string)

