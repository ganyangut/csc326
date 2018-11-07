# lab3
# create database tables

import sqlite3 as lite
from static_variables import StaticVar

class MyDatabase:

    def __init__(self,db_conn):
        self._db_conn = db_conn
        self._cursor = db_conn.cursor()

    def init_db_tables(self):
        if self._cursor:
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS documentIndex(doc_id integer, url text, depth integer, title text, short_description text,words text, link text, occurrence_number integer, PRIMARY KEY(doc_id));"
            )
            '''
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS links(destination_url_id integer,occurrence_number integer,PRIMARY KEY(destination_url_id))"
            )
            '''
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS lexicon(word_id integer, words text, PRIMARY KEY(word_id))"
            )
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS invertedIndex(word_id integer,doc_id integer,PRIMARY KEY(word_id))"
            )
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS resolvedInvertedIndex(words text, document_url text)"
            )
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS pageRank(doc_id integer,rank_score real, PRIMARY KEY(doc_id))"
            )

    def select_word_id_from_lexicon(self, word_string):
        if self._cursor:
            try:
                #word_id = []
                #for word in word_string:
                #print "word: "+repr(word)
                self._cursor.execute( "SELECT word_id FROM lexicon where word_string = ?", (word_string,))
                word_id = self._cursor.fetchall()
                #print "word_id: "+repr(word_id)
                return word_id
            except lite.Error as e:
                raise e

    def select_document_id_from_InvertedIndex(self, word_id):
        if self._cursor:
            try:
                document_id = []
                for id in word_id:
                    #print "id: "+repr(id)
                    self._cursor.execute("SELECT document_id FROM inverted_index where word_id = ?", id)
                    document_id = self._cursor.fetchall()
                    #print "doc_id: "+repr(document_id)
                return document_id
            except lite.Error as e:
                raise e

    def select_document_id_from_PageRank(self, document_id):
        if self._cursor:
            try:
                page_rank={}
                sorted_document_id = []
                for id in document_id:
                    print "page_rank ----- id: "+repr(id)
                    self._cursor.execute( "SELECT rank_value, document_id FROM page_rank where document_id = ?", id)
                    temp_page_rank = self._cursor.fetchall()
                    page_rank[temp_page_rank[0][0]]=temp_page_rank[0][1]
                    print "temp_page_rank: "+repr(temp_page_rank)
                keys=page_rank.keys()
                keys.sort(reverse=True)
                sorted_document_id = map(page_rank.get,keys)
                return sorted_document_id
            except lite.Error as e:
                raise e

    def select_document_from_DocumentIndex(self, document_id):
        if self._cursor:
            try:
                document = []
                for id in document_id:
                    print "document index ------- id: "+repr(id)
                    self._cursor.execute("SELECT url, title, short_description FROM document_index where document_id = ?", (id,))
                    document = document + self._cursor.fetchall()
                    print "document index ----- document: "+repr(document)
                return document
            except lite.Error as e:
                raise e

    def select_doc_id_with_links_from_Link(self,document_id):
        if self._cursor:
            try:
                self._cursor.execute("SELECT from_document_id FROM links")
                from_document_id=self._cursor.fetchall()
                for id in document_id:
                    if id not in from_document_id:
                        document_id.remove(id)
                return document_id
            except lite.Error as e:
                raise e
                    
    def disconnect_db(self):
        self._db_conn.commit()
        self._db_conn.close()
