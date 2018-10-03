# csc326
a search engine project


database framework:

    document index # that keeps information about each document
        dict {document id: document}

        document
            list [url, depth, title, short_description, words, links]

            words
                list [word]
    
                word
                    tuple (word id, font size)

            links
                dict {to_doc_id: number of links}                

    lexicon # keeps a list of words
        dict {word id: word string}

    inverted index # that returns a list of document Ids given a word id
        dict {word id: set([document id0, document id1, document id2, ..., ])}

    resolved inverted index # that returns a list of document urls given a word string
        dict {word string: set([document url0, document url1, document url2, ..., ])}

    _word_id_cache
        dict {word string: word id}

    _doc_id_cache
        dict {document url: document id}


Questions:
    ASCII/Unicode
    inverted index key: 1 or '1'
    how to submit test cases

TODO: 
    frontend fix
    some unicode remaining
    self.depth necessary or not
    document repr method

test:
    csc326/backend$ python crawler.py

backup test urls:
    http://www.eecg.toronto.edu/~csc467/
    http://www.petergoodman.me/
    http://dsrg.utoronto.ca/csc467/index.html