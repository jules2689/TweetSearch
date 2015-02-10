TweetSearch
==========

| Name            | SN      |
|-----------------|---------|
| Julian Nadeau   | 6008161 |
| Emilienne Pugin | 5214350 | 

Setup
---
 - Ensure you have Python 2.7 installed.
 - Run `pip install -r requirements.txt` from the base directory.

How to run
---
 1. Run `pip install -r requirements.txt`
 2. Run `python -i run.py`
 3. Wait for the index to occur
 4. Batch Queries are then performed and results are printed onto the screen.

How to Evalutate
---
 1. Download the tree_eval script from the assignment page.
 2. Point your terminal to the unzipped dir and type 'make'
 3. If `make` doesn't work you might need to install Xcode. 
 4. Test it worked with `make quicktest`
 5. Run `./trec_eval Trec_microblog11-qrels.txt results.txt`

Now when you run run.py it will take the query texts, and batch run them, and just dump in console directly the content of the results file

---

How was the work divided
---
The work was divided in a very ad-hoc manner, combined with a bit of Agile development. What this means to say is that the requirements for this assignment was treated as a series of stories broken down as such:

 1. Preprocessing
 2. Indexing
 3. Retrieval and Ranking
 4. Results
 5. Evaluation
 6. Report
 7. Cleanup and Verification of Code
 8. Optimizations

During the initial stages, Julian started by writing a small preprocessing script. This was developed at first to present a simple word frequency pattern.

After the initial preprocessing of the tweets, Emilienne worked to integration Whoosh to perform our indexing and our retrieval/ranking. Whoosh provided a good backbone for both of these features so that they went hand in hand.

Emilienne then provided the outputted results in the correct format since these are a result of the retrieval process.

Next, Evaluation was used to determine weak points in the indexing method. Once these weak points were discovered, optimization stories were further flushed out. This was determined by both team members.

The Report was then started as a way to take note and verify the code structure (as the functionality portion was filled in). This report was started by Julian.

During the reporting phase, Julian took the time to split up classes that had become too large and cleanup the code. He split the concerns of various sections into their own classes and renamed code where necessary. He removed unused requirements and imports, as well as vestigial methods.

Optimizations were then performed by both team members. These optimizations were determined through analysis, evaluation and discussions.

Discussions were held between the team members throughout the project to determine which sections must be completed and which goals we were to reach.

---

Functionality
---
 - Using the `run.py` script, `BatchRunQueries` are setup and performed. 
 - The `BatchRunQueries` script first setups up a `Indexer` object which initially calls the `Preprocessing` script, which removes all invalid information (punctuation etc.).
 - The `Indexer` then creates an index on the resulting text.
 - Next, `BatchRunQueries` extracts all queries from the `topics_MB1-50.txt` and extracts individual queries using the `BeautifulSoup` Library, an information scraping library for Python.
 - After the queries are parsed, the script runs each query against the `Indexer` one by one.

### Preprocessing

**preprocess**
This is the initial call to the Preprocessor. It reads in the data and preprocesses it.
Finally, it returns the processed tweets.

**process_text**
First, all punctionation is removed. 
This is accomplished using a "translate" method in Python and the string.puncuation list.
Finally, an array of text is returned by splitting the text by newline (each tweet is a line).

### Indexing
Indexing is accomplished using the `Whoosh` library available for Python. This library allows us to define an index "Schema"
```Schema(title=TEXT(stored=True), content=TEXT(stored=True, analyzer=StemmingAnalyzer(stoplist=stop_words)))```

This schema indicates that we have a title and content, both text and both stored in the index, and that we want to analyze using Stemming.
The Stemming Analyzer also takes care of removing and ignoring stop words that we manually define.
The library takes care of the fine detailed implementation.

```
  for tweet in self.tweets:
    tweet = tweet.split("\t")
    tweetNum = tweet[0]
    tweetContent = tweet[1]
    writer.add_document(title=u(tweetNum), content=u(tweetContent))
```

This piece of code loops through the tweets and starts to build the text. For each tweet, we split on the tab character.
The first section is the tweetNum, which is stored as the title.
The second section is split on the space and then preprocessed to remove invalid words.
Finally, we write the document to the corpus of documents in the indexer.

### Retrieval and Ranking
The retrieval and ranking also uses the `Whoosh` library.

First, we constuct a query object that looks through the "content" in the index described by our schema.
Second, with an index searcher that uses TF IDF weighting, we search the corpus of documents and extract up to 1000 results.
We then print the results to the console using the TrecEval format.

Note: The query is performed using a Stemming Analyzer, which will analyze and ignore stop words.


TODO
---
- write a README file (plain text or Word format) [15 points for this report] including:
  * √ your names and student numbers. Specify how the tasks were divided between the team members
  * √ a detailed note about the functionality of your programs
  * √ complete instructions on how to run them
  * Explain the algorithms, data structures, and optimizations that you used in each of the three steps. How big was the vocabulary? Include a sample of 100 tokens from your vocabulary. Include the first 10 answers to queries 1 and 25. Discuss your final results.
- √ include the file named Results with the results for all the 49 test queries, in the required format.
- √ make sure all your programs run correctly.
- submit your assignment, including programs, README file, and Results file, as a zip file through Blackboard Learn.
- **don’t include the initial text collection or any external tools.**

