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

How to Evaluate
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
First, all punctuation is removed. 
This is accomplished using a "translate" method in Python and the string.punctuation list.
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

First, we construct a query object that looks through the "content" in the index described by our schema.
Second, with an index searcher that uses TF IDF weighting, we search the corpus of documents and extract up to 1000 results.
We then print the results to the console using the TrecEval format.

Note: The query is performed using a Stemming Analyzer, which will analyze and ignore stop words.

---

Algorithms, Data Structures, and Optimizations
---

### Algorithms

#### Preprocessing
None in use.

#### Indexing
There is a StemmingAnalyzer being used by the schema.

Stemming is a heuristic process whereby the suffix (and sometimes prefix) of words is removed. For example the word "rendered", would be stemmed to "render", as would "renders", "rendering", "rendered" etc.

The Stemming algorithm also removes stop words specified by a list.

The Stemming algorithm employs a variety of algorithms including Porter and Porter2, Paice Husk, and Lovins.

##### Porter and Porter2
These algorithms work by following a series of grammatical replacement steps through what can be described as a series of transitional graphs.

The algorithm works by moving along a series of suffix replacements that replace the terminating characters of words with a reduced character set, with the end goal of removing the suffix and leaving an English word. Unfortunately, the Porter algorithm will sometimes overstem a word, which mean to say a word like "general" will accidentally become "gener". The Porter 2 algorithm sought to reduce these errors by including a number of different suffixes that Porter did not include. 

##### Paice Husk
This is a conflation based iterative stemmer that is known to be strong and aggressive. The algorithm used a single table of rules, each of which may remove or replace the suffix of a word. This methodology sought to avoid the overstemming problem mentioned above with the "Porter" algorithm. The algorithm follows 4 main steps:

  1. Select the relevant section and inspect the last letter of the word. If present, examine using the first rule of the relevant section in the rule table.
  2. Check if the rule applies. If the last letters of term do not match with the rule or acceptability conditions are not satisfied go to stage 4, otherwise continue to stage 3.
  3. Apply the rule to the word. Remove or replace the suffix as necessary. Finally, check the termination symbol and either terminate or return to stage 1.
  4. Look for another rule that applies to the word. As you move to the next row in the table, if the section letter of the rules table changes, finalize the word, otherwise return to stage 2.

##### Lovins
Originally incluenced by technical vocabulary, the Lovins stemmer has 294 endings, 29 conditions and 35 transformation rules, with each ending associated to a condition. Lovins is a noticeably larger algorithm than the Porter algorithm due to its extensive suffix list. However the larger size is supplemented by a faster algorithm.

The algorithm works as follows:
1. The longest suffix (ending) that is found which satisfies the associated condition, is removed. 
2. The 35 rules are applied to transform the ending. This step is performed whether or not an ending is removed in the first step. 

#### Scoring and Retrieval

##### BM25F
By default Whoosh uses the BM25F scoring algorithm for use in analysis.

BM25F is a ranking function used by search engines. It ranks documents based on their relevance to a search query. The algorithm is a "bag-of-words" retrieval function, which means that it is a simplified representation, or set, of words.

A rank is determined by the number of query terms in a given document regardless of any inter-relationship between query terms (for example, close proximity in a document).

The score is based on the inverse document frequency (IDF) and the overall term frequency weighted by the length of the document.

##### TF-IDF
Currently, the scoring analysis in use is TF_IDF.

TF IDF is the product of 2 statistics, the "term frequency" (TF) and the "inverse document frequency" (IDF). The term frequency can be determined by any number of methods including the "raw frequency" and an "augmented frequency" which weights the frequency based on the length of the document.

This algorithm bases the relevance of a document on a the term frequency and the inverse term frequency so that common words, such as "the" is does not impact the results, as it will irrelevantly be more common in many documents.

As you can see, these algorithms are very similar and were used to simply experiment with their differences. Due to their similarity and the relatively small index, the differences were not significant.

### Data Structures
The majority of the preprocessing, indexing and retrieval is performed using Libraries and classes.

#### Preprocessing
 - General Tweet content is initially held in a simple Array prior to indexing.

#### Indexing
 - The index is held in a combination of an "index" and a "schema" object, the schema is only used in the initial creation.
 - The "schema" object stores information about the type of data and which data should be stored.
 - The "index" consumes the "schema" and created a "FileStorage" object which is stored in the "tweetsearch/indexdir" directory

#### Scoring and Retrieval
 - The "searcher" object that is used forms a sort of buffer that must closed at the end.
 - The "searcher" object consumes a "query" object that is constructed from a basic string
 - The execution of a search returns a "result" object, which is essentially just a list of hashes. Each has represents a document in the corpus.

### Optimizations for all sections
Initial optimizations included adding stop words. Initially, no stop words were being removed. Our first step was to manually remove the stop words on preprocessing, but this proved to be a difficult task as the preprocessor did not differentiate between the tweet id and the content. We later moved this task to the time of indexing, but this proved to be a huge slow down on indexing (increasing the indexing time a few times over). Finally, it was determined that the Whoosh library supports a StemmingAnalyzer that will remove words from a stop list, and so the stop words was moved there with great success.

With regards to the StemmingAnalyzer, we switched the type of cache from "least recently used" (LRU) to an unbounded cache to decrease batch query time, but reduce memory performance. As a number of queries are being performed in quick succession, it may be necessary to use a number of cached stemming words. Since it can be assumed that the index is relatively small, and the memory capacity large, this unbounded cache may give a performance boost with no detriment due to the larger memory footprint.


TODO
---
- write a README file (plain text or Word format) [15 points for this report] including:
  * √ your names and student numbers. Specify how the tasks were divided between the team members
  * √ a detailed note about the functionality of your programs
  * √ complete instructions on how to run them
  * √ Explain the algorithms, data structures, and optimizations that you used in each of the three steps. 
  * How big was the vocabulary? 
  * Include a sample of 100 tokens from your vocabulary. 
  * Include the first 10 answers to queries 1 and 25. 
  * Discuss your final results.


- √ include the file named Results with the results for all the 49 test queries, in the required format.
- √ make sure all your programs run correctly.
- submit your assignment, including programs, README file, and Results file, as a zip file through Blackboard Learn.
- **don’t include the initial text collection or any external tools.**

