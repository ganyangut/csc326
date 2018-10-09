# csc326

a search engine project

* how to run front end:
  * in terminal, under lab1_group_20:
    * ~/lab1_group_20$ python frontend.py
  * in browser:
    * localhost:8081

* how to run tests for backend:
  * in terminal, under lab1_group_20/backend:
    * ~/lab1_group_20/backend$ python test.py

* how to run crawler:
  * in terminal, under lab1_group_20/backend:
    * ~/lab1_group_20/backend$ python crawler.py

* database framework:
  * document index # that keeps information about each document
    * dict {document id: document}
    * document
      * list [url, depth, title, short_description, words, links]
      * words
        * list [word]
        * word
          * tuple (word id, font size)
      * links
        * dict {to_doc_id: number of links}
      * lexicon # keeps a list of words
        * dict {word id: word string}
      * inverted index # that returns a list of document Ids given a word id
        * dict {word id: set([document id0, document id1, document id2, ..., ])}
      * resolved inverted index # that returns a list of document urls given a word string
        * dict {word string: set([document url0, document url1, document url2, ..., ])}
      * _word_id_cache
        * dict {word string: word id}
      * _doc_id_cache
        * dict {document url: document id}

* backup test urls:
  * http://www.eecg.toronto.edu/~csc467/
  * http://www.petergoodman.me/
  * http://dsrg.utoronto.ca/csc467/index.html


http://dsrg.utoronto.ca/csc467/midterm/midterm11.pdf
    
    Traceback (most recent call last):
      File "crawler.py", line 444, in <module>
        bot.crawl(depth=1)
      File "crawler.py", line 384, in crawl
        soup = BeautifulSoup(socket.read())
      File "/usr/lib/python2.7/dist-packages/BeautifulSoup.py", line 1522, in __init__
        BeautifulStoneSoup.__init__(self, *args, **kwargs)
      File "/usr/lib/python2.7/dist-packages/BeautifulSoup.py", line 1147, in __init__
        self._feed(isHTML=isHTML)
      File "/usr/lib/python2.7/dist-packages/BeautifulSoup.py", line 1189, in _feed
        SGMLParser.feed(self, markup)
      File "/usr/lib/python2.7/sgmllib.py", line 104, in feed
        self.goahead(0)
      File "/usr/lib/python2.7/sgmllib.py", line 143, in goahead
        k = self.parse_endtag(i)
      File "/usr/lib/python2.7/sgmllib.py", line 320, in parse_endtag
        self.finish_endtag(tag)
      File "/usr/lib/python2.7/sgmllib.py", line 358, in finish_endtag
        method = getattr(self, 'end_' + tag)
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xed' in position 4: ordinal not in range(128)