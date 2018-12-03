# lab3
# create database tables

import sqlite3 as lite
from static_variables import StaticVar
import unicodedata

class MyDatabase:
    def __init__(self,db_conn):
        self._db_conn = db_conn
        self._cursor = db_conn.cursor()

    def get_all_words_from_lexicon(self):
        if self._cursor:
            try:
                self._cursor.execute("SELECT DISTINCT word_string FROM lexicon")
                words_from_db = self._cursor.fetchall()
                word_list = []
                count = 0
                for (word_string, ) in words_from_db:
                    if isinstance(word_string, unicode):
                        word_string = unicodedata.normalize('NFKD', word_string).encode('ascii','ignore')
                    word_list.append(word_string)
                    count += 1
                    if count == 10:
                        break
                return word_list
            except lite.Error as e:
                raise e

    def select_word_id_from_lexicon(self, keyword_list):
        if self._cursor:
            try:
                word_id_list = []
                for word_string in keyword_list:
                    word_string = word_string.lower()
                    self._cursor.execute("SELECT crawler_id, word_id FROM lexicon WHERE word_string = ?", (word_string,))
                    word_id_list += self._cursor.fetchall()
                return word_id_list
            except lite.Error as e:
                raise e

    def select_document_id_from_InvertedIndex(self, word_id_list):
        if self._cursor:
            try:
                cid_docid_rankv = []
                for word_id in word_id_list:
                    self._cursor.execute("SELECT crawler_id, document_id, rank_value FROM inverted_index where crawler_id = ? and word_id = ?", word_id)
                    cid_docid_rankv += self._cursor.fetchall()

                cid_docid_rankv_dict = {}
                for (crawler_id, document_id, rank_value) in cid_docid_rankv:
                    if (crawler_id, document_id) not in cid_docid_rankv_dict:
                        cid_docid_rankv_dict[(crawler_id, document_id)] = rank_value
                    else:
                        cid_docid_rankv_dict[(crawler_id, document_id)] += rank_value

                sorted_cid_docid_rankv = sorted(cid_docid_rankv_dict.items(), key=lambda d: -d[1])
                
                sorted_cid_docid = []
                for ((crawler_id, document_id), rank_value) in sorted_cid_docid_rankv:
                    sorted_cid_docid.append((crawler_id, document_id))

                return sorted_cid_docid
            except lite.Error as e:
                raise e

    def select_document_id_from_PageRank(self, document_id):
        if self._cursor:
            try:
                page_rank={}
                sorted_document_id = ()
                for id in document_id:
                    self._cursor.execute("SELECT rank_value, crawler_id, document_id FROM page_rank WHERE crawler_id= ? and document_id = ?", id)
                    temp_page_rank = self._cursor.fetchall()
                    if temp_page_rank:
                        page_rank[temp_page_rank[0][1],temp_page_rank[0][2]]=(temp_page_rank[0][0])
                    else:
                        page_rank[id] = 0
                
                sorted_page_rank  = sorted(page_rank.items(), key=lambda d: d[1], reverse=True)
                
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
                    self._cursor.execute("SELECT url, title, short_description FROM document_index where crawler_id =? and document_id = ?", id)
                    document = document + self._cursor.fetchall()
                return document
            except lite.Error as e:
                raise e
         
    def disconnect_db(self):
        self._db_conn.commit()
        self._db_conn.close()
