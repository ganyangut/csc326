# lab3
# create database tables

import sqlite3 as lite
from static_variables import StaticVar
import unicodedata

class MyDatabase:
    def __init__(self,db_conn):
        self._db_conn = db_conn
        self._cursor = db_conn.cursor()

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
