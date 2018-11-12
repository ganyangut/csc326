# lab3
# create database tables

import sqlite3 as lite
from static_variables import StaticVar

class MyDatabase:

    def __init__(self,db_conn):
        self._db_conn = db_conn
        self._cursor = db_conn.cursor()

    def select_word_id_from_lexicon(self, word_string):
        if self._cursor:
            try:
                print "word_string: "+repr(word_string)
                self._cursor.execute( "SELECT crawler_id, word_id FROM lexicon where word_string = ?", (word_string,))
                word_id = self._cursor.fetchall()
                print "word_id: "+repr(word_id)
                return word_id
            except lite.Error as e:
                raise e

    def select_document_id_from_InvertedIndex(self, word_id):
        if self._cursor:
            try:
                document_id = []
                for id in word_id:
                    print "id: "+repr(id)
                    self._cursor.execute("SELECT crawler_id, document_id FROM inverted_index where crawler_id = ? and word_id = ?", id)
                    document_id = document_id + self._cursor.fetchall()
                    print "doc_id: "+repr(document_id)
                return document_id
            except lite.Error as e:
                raise e

    def select_document_id_from_PageRank(self, document_id):
        if self._cursor:
            try:
                page_rank={}
                #page_rank_list=[]
                sorted_document_id = ()
                for id in document_id:
                    print "page_rank ----- id: "+repr(id)
                    self._cursor.execute( "SELECT rank_value, crawler_id, document_id FROM page_rank where crawler_id= ? and document_id = ?", id)
                    temp_page_rank = self._cursor.fetchall()
                    page_rank[temp_page_rank[0][1],temp_page_rank[0][2]]=(temp_page_rank[0][0])
                    #page_rank[temp_page_rank[0][0]]=(temp_page_rank[0][1],temp_page_rank[0][2])
                    #page_rank_list.append({temp_page_rank[0][0]:(temp_page_rank[0][1],temp_page_rank[0][2])})
                    print "temp_page_rank: "+repr(temp_page_rank)
                    print "page_rank: "+repr(page_rank)
                
                sorted_page_rank  = sorted(page_rank.items(), key=lambda d: d[1], reverse=True)

                print "final_page_rank: "
                print sorted_page_rank
                
                for rank in sorted_page_rank:
                    i = 0
                    for r in rank:
                        i = i+1 
                        if i % 2 !=0:
                            sorted_document_id = sorted_document_id+ (r,)
                
                
                return sorted_document_id
            except lite.Error as e:
                raise e

    def select_document_from_DocumentIndex(self, document_id):
        if self._cursor:
            try:
                document = []
                for id in document_id:                  
                    print "document index ------- id: "+repr(id)
                    self._cursor.execute("SELECT url, title, short_description FROM document_index where crawler_id =? and document_id = ?", id)
                    document = document + self._cursor.fetchall()
                    print "document index ----- document: "+repr(document)
                return document
            except lite.Error as e:
                raise e


    '''    
    def select_word_id_from_lexicon(self, word_string):
        if self._cursor:
            try:
                print "word_string: "+repr(word_string)
                self._cursor.execute( "SELECT word_id FROM lexicon where word_string = ?", (word_string,))
                word_id = self._cursor.fetchall()
                print "word_id: "+repr(word_id)
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
                doc_id = [i[0] for i in document_id]
                print doc_id
                doc_id = tuple(doc_id)
                print doc_id
                self._cursor.execute( "SELECT document_id FROM page_rank where document_id in {} order by rank_value desc".format(doc_id))
                sorted_document_id=self._cursor.fetchall()
                return sorted_document_id
            except lite.Error as e:
                raise e

    def select_document_from_DocumentIndex(self, document_id):
        if self._cursor:
            try:
                document = []
                for id in document_id:                  
                    print "document index ------- id: "+repr(id)
                    self._cursor.execute("SELECT url, title, short_description FROM document_index where document_id = ?", id)
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
    '''               
    def disconnect_db(self):
        self._db_conn.commit()
        self._db_conn.close()
