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
 3. Wait for the indexing to occur
 4. Batch Queries are then performed and results are printed into "results.txt".
 5. Term Stats (number of terms in vocabulary and a sample of 100 terms) is output to "term_stats.txt"
 6. Top Results are output to "topResults.txt"

How to Evaluate
---
 1. Download the tree_eval script from the assignment page.
 2. Point your terminal to the unzipped dir and type 'make'
 3. If `make` doesn't work you might need to install Xcode. 
 4. Test it worked with `make quicktest`
 5. Run `./trec_eval Trec_microblog11-qrels.txt results.txt`

Now when you run run.py it will take the query texts, and batch run them, and just dump in console directly the content of the results file

---

How the work was divided
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
 9. Stats based results
 10. Verification of Report

During the initial stages, Julian started by writing a small preprocessing script. This was developed at first to present a simple word frequency pattern.

After the initial preprocessing of the tweets, Emilienne worked to integrate Whoosh library to perform our indexing and our retrieval/ranking. Whoosh provided a good backbone for both of these features so that they went hand in hand.

Then, the queries to be used in the evaluations were parsed, we used the BeautifulSoup library to parse this html text and retrieve the unique query ids, and query text content.

Emilienne then provided the outputted results from the searcher in the correct format and printed them to file.

Next, several test runs were carried out, to determine weak points in the indexing method. Once these weak points were discovered, optimization stories were further flushed out. This was determined by both team members.

The Report was then started as a way to take note and verify the code structure (as the functionality portion was filled in). This report was fleshed out by Julian.

During the reporting phase, Julian took the time to split up classes that had become too large and cleanup the code. He split the concerns of various sections into their own classes and renamed code where necessary. He removed unused requirements and imports, as well as vestigial methods.

Optimizations were then performed by both team members. These optimizations were determined through analysis, evaluation and discussions.

Discussions were held between the team members throughout the project to determine which sections must be completed and which goals we were to reach. Once initial results came in, brainstorming sessions were held to think of ways to improve them, and implemented by both Julian and Emilienne.

Outputting of stats based results (including the term-based stat numbers (such as vocabulary size), the selections of terms and the selection of query results) was split among both members of the team.

The last run through of the report was performed by both members of the team.

---

Functionality
---
 - Using the `run.py` script, `BatchRunQueries` are setup and performed. 
 - The `BatchRunQueries` script first setups up a `Indexer` object which initially calls the `Preprocessing` script, which removes all invalid information (punctuation etc.).
 - The `Indexer` then creates an index on the resulting text.
 - Next, `BatchRunQueries` extracts all queries from the `topics_MB1-50.txt` and extracts individual queries using the `BeautifulSoup` Library, an information scraping library for Python.
 - After the queries are parsed, the script runs each query against the `Indexer` one by one, and prints the results.

### Preprocessing

**preprocess**
This is the initial call to the Preprocessor. It reads in the data and preprocesses it.
Finally, it returns the processed tweets.

**process_text**
First, all punctuation is removed. 
This is accomplished using a "translate" method in Python and the string.punctuation list.
Finally, an array of text is returned by splitting the text by newline (each tweet is a line). This array of text consists in the unique tweet id, a tab, and the tweet content.

### Indexing
Indexing is accomplished using the `Whoosh` library available for Python. This library allows us to define an index "Schema"
```Schema(title=TEXT(stored=True), content=TEXT(stored=True, analyzer=StemmingAnalyzer(stoplist=stop_words)))```

This schema indicates that for each document/tweet we have a title and content, both text and both stored in the index. An additional argument is also added to indicate that we want to use a stemming analyzer.
The Stemming Analyzer also takes care of removing and ignoring stop words that we manually defined using the file provided by Dr. Inkpen.
The library takes care of the fine grained implementation of building the index from the tweets. The tweets served as the document inputs, and were added to the index in the following manner:

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
Second, with an index searcher that uses one of several kinds of weighting, we search the corpus of documents and extract up to 1000 results. At first the TF-IDF weighting was used, and then BM25 was used as well.
We then print the results to a file using the TrecEval format, in order to evaluate them using the trec_eval script.

Note: The query is also evaluated using a Stemming Analyzer, which will analyze and ignore stop words.

---

Algorithms, Data Structures, and Optimizations
---

### Algorithms

#### Preprocessing
None in use beyond the prior mentioned scripts.

#### Indexing
There is a StemmingAnalyzer being used by the schema.

Stemming is a heuristic process whereby the suffix (and sometimes prefix) of words is removed. For example the word "rendered", would be stemmed to "render", as would "renders", "rendering", "rendered" etc.

The Stemming algorithm also removes stop words specified by a list of common words in the English language.

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
Another scoring analysis we used to generate results is TF_IDF.

TF-IDF is the product of 2 statistics, the "term frequency" (TF) and the "inverse document frequency" (IDF). The term frequency can be determined by any number of methods including the "raw frequency" and an "augmented frequency" which weights the frequency based on the length of the document.

This algorithm bases the relevance of a document on the term frequency and the inverse term frequency so that common words, such as "the" does not impact the results, as it will irrelevantly be more common in many documents, and therefore a poor matching predictor.

These algorithms are similar and were both used in the generation of results and compared.

### Data Structures
The majority of the preprocessing, indexing and retrieval is abstracted and performed using libraries.

#### Preprocessing
 - General tweet content is initially held in a python list (essentially an array) prior to indexing. The BeautifulSoup library allows the text document in which the queries are stored with html markup to be parsed into a soup object. This object's attributes are the various tag labels from the query file (num, title, querytime, etc.). 

#### Indexing
 - The index is held in a combination of an "index" and a "schema" object, the schema is only used in the initial creation, to define the fields required for each value of the index.
 - The "schema" object stores information about the type of data and which data should be stored. In our case, we have the "content" which is the main tweet text, and the "title" which is the unique tweet id.
 - The "index" consumes the "schema" and creates a "FileStorage" object which is stored in the "tweetsearch/indexdir" directory.

#### Scoring and Retrieval
 - The "searcher" object that is used forms a sort of buffer that must closed once its purpose is fulfilled.
 - The "searcher" object consumes a "query" object that is constructed from the content of the query text, as provided.
 - The execution of a search returns a "result" object, which is essentially just a list of hashes. Each represents a document/tweet in the corpus.

### Optimizations for all sections
Initial optimizations included adding stop words. Initially, no stop words were being removed. Our first step was to manually remove the stop words on preprocessing, but this proved to be a difficult task as the preprocessor did not differentiate between the tweet id and the content. We later moved this task to the time of indexing, but this proved to be a huge slow down on indexing (increasing the indexing time a few times over). Finally, it was determined that the Whoosh library supports a StemmingAnalyzer that will remove words from a provided stop list, and so the stop words removal process was moved there with great success.

With regards to the StemmingAnalyzer, we switched the type of cache from "least recently used" (LRU) to an unbounded cache to decrease batch query time, but this reduced memory performance. As a number of queries are being performed in quick succession, it may be necessary to use a number of cached stemming words. Since it can be assumed that the index is relatively small, and the memory capacity large, this unbounded cache may give a performance boost with no detriment due to the larger memory footprint.

For query text, the words in each query could be joined with a multitude of keywords. We switched to using "OR" grouping instead of "AND" grouping, which means that any of terms could, but do not have to, exist in any order, instead of requiring all words be present at the same time in the same document. This allowed more results to be returned in a query, and therefore more relevant results to be matched to any given query.

Stepping Stone to Results
---

In the initial run, we ran with BM25F Weighting. We decided to test against TF-IDF weighting to compare the differences. Below we list the results after running the queries against trec_eval.


|                       |  BM25F Weighting     |  TF-IDF Weighting   |
|-----------------------|----------------------|---------------------|
| runid                 |  all awesomenessRun  |  all awesomenessRun |
| num_q                 |  all 49              |  all 49             |
| num_ret               |  all 40773           |  all 40773          |
| num_rel               |  all 2640            |  all 2640           |
| num_rel_ret           |  all 2203            |  all 2207           |
| map                   |  all 0.2560          |  all 0.1918         |
| gm_map                |  all 0.1954          |  all 0.1294         |
| Rprec                 |  all 0.3018          |  all 0.2100         |
| bpref                 |  all 0.2747          |  all 0.1825         |
| recip_rank            |  all 0.5820          |  all 0.4555         |
| iprec_at_recall_0.00  |  all 0.6527          |  all 0.5121         |
| iprec_at_recall_0.10  |  all 0.5221          |  all 0.3512         |
| iprec_at_recall_0.20  |  all 0.4313          |  all 0.2996         |
| iprec_at_recall_0.30  |  all 0.3600          |  all 0.2783         |
| iprec_at_recall_0.40  |  all 0.3265          |  all 0.2504         |
| iprec_at_recall_0.50  |  all 0.2724          |  all 0.2297         |
| iprec_at_recall_0.60  |  all 0.1993          |  all 0.1898         |
| iprec_at_recall_0.70  |  all 0.1533          |  all 0.1489         |
| iprec_at_recall_0.80  |  all 0.1093          |  all 0.1172         |
| iprec_at_recall_0.90  |  all 0.0716          |  all 0.0608         |
| iprec_at_recall_1.00  |  all 0.0135          |  all 0.0100         |
| P_5                   |  all 0.3510          |  all 0.2490         |
| P_10                  |  all 0.3388          |  all 0.2571         |
| P_15                  |  all 0.3252          |  all 0.2653         |
| P_20                  |  all 0.3020          |  all 0.2592         |
| P_30                  |  all 0.2714          |  all 0.2395         |
| P_100                 |  all 0.1906          |  all 0.1531         |
| P_200                 |  all 0.1347          |  all 0.1288         |
| P_500                 |  all 0.0771          |  all 0.0778         |
| P_1000                |  all 0.0450          |  all 0.0450         |

Discussion of Results
---

It is clear that BM25F yielded better results, which is why we reverted to using that weighting algorithm. This is probably due to the BM25F algorithm using a probablistic weighting scheme. 

Our mean average precision stood at about 25-26% throughout all queries. Using BM25F our general precision is quite a bit higher in most areas with about 6-13% higher precision than the respective score for TF-IDF. TF-IDF did retrieve slightly more relevant results (4 more to be exact), however the precision was, as previously mentioned, lower.

With regards to the number of relevant documents versus those retrieved, we have 83.44% for BMF25 and 83.59% for TF-IDF. Both of these values seem to represent a large portion of the relevant documents available.

In the end, with about 83-84% of the relvant documents retrieved and about a 26% precision, the indexing and retrieval performed by this project presents a fairly good representation of the relevant documents. 

Statistics
---

The corpus size of the index was 45,899 documents/tweets, and 88,095 unique terms composed it. For 100 sample terms contained in the index, see the term_stats.txt document.

Sample Results
---

#### Results for query 1:
Query text: BBC World Service staff cuts 

First 10 results:
 - BBC News Major cuts to BBC World Service BBC World Service is to close five of its language services with th httpbbcine2vlpX
 - Major cuts to BBC World Service BBC World Service is to close five of its language services with the likely lo httpbbcineftjNe
 - BBC World Service axes five language services AFP  AFP  The BBC World Service has said it will close five o httpowly1b23Gf
 - BBC News  BBC World Service cuts to be outlined to staff httpwwwbbccouknewsentertainmentarts12283356
 - BBC Caribbean to be shut down  Stabroek News  Guyana BBC BBC World Service today announced cuts which will  httpbitlyh9huts
 - BBC World Service plans 650 job cuts AP  AP  The BBC said Wednesday that it plans to cut 650 jobs more tha httpowly1b2u20
 - One understands that the BBC World Service is to be renamed BBC Almost the Entire World Service
 - RT QueenUK One understands that the BBC World Service is to be renamed BBC Almost the Entire World Service
 - BBC World Service axes five languages 650 jobs AFP AFP  The BBC World Service said Wednesday it would  httpbitlyf1uNCb
 - BBC World to slash five foreign services THE BBC World Service will shed around 500 jobs after announcing plans httpbitlyfR3vd8

#### Results for query 25:

Query text: TSA airport screening 

First 10 results:
 - The TSAs New Scanners Spot Bombs Not Dongs Tsa httpdlvritFZn1C Tsa ãGIZMODEã
 - TSA to vote on unionizing in March Great So when TSA employee gropes you youll have 5 other TSA guys standing around supervising tcot
 - TSA to Test New Screening at HartsfieldJackson The TSA in coming days at HartsfieldJackson Atlanta Internatio httpbitlye8NW0S
 - Background Screening  Top 5 Reasons to Organize Background Screening Background screening is becoming more pre httpbitlyiktHdI
 - The TSA has a unique ability to make an airport seem busy even when it isnt tsa
 - Power grab TSA fights to stop private screeners at airports despite new Congress and flyers wanting them httpbitlyfX0Qyd tsa
 - New post Seattle man acquitted in TSA airport case See arrest video  Seattle Po httpbitlye1W2Wo TSABlogTeam BigSis Fascism TSA
 - TF  Travel RT BitterAmerican TSA shuts door on private airport screening program  httpbitlyfx6Dgw cnn httpbitlyeADg2G
 - TSA Shuts Down Private Airport Screen Program is headline now on wwwfedsmithcom
 - TSA Shuts Door on Private Airport Screening Program â Patriot Update httppatriotupdatecom2451tsashutsdooronprivateairportscreeningprogramsmssstwitteratxt4d45868911137f910Â â¦ via AddThis





