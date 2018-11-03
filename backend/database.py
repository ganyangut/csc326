# lab3
# create database tables

import sqlite3 as lite


class MyDatabase():

    def _init_(self, db_conn):
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

    def add_link(self, from_doc_id, to_doc_id):
        """Add a link into the database, or increase the number of links between
        two pages in the database."""
        sql_get_link = "SELECT occurrence_number from documentIndex where doc_id=%s and link =%s"
        params = []
        params.append(from_doc_id)
        params.append(to_doc_id)

        self._cursor.execute(sqlString, tuple(params))
        row = self._cursor.fetchone()

        if row!='':
            occ_num=int(row)+1
            sql_ocurrence_number_plus_one="UPDATE documentIndex SET ocurrence_number=%s"

        if self.document_index[from_doc_id].links == None:
            self.document_index[from_doc_id].links = {}
        # if the link exists in the db, increase the number
        if to_doc_id in self.document_index[from_doc_id].links:
            self.document_index[from_doc_id].links[to_doc_id] += 1
        else:  # if the link doesn't exist in the db, add it
            self.document_index[from_doc_id].links[to_doc_id] = 1

    def insert_to_db_documentIndex(self, doc_id, url, depth, title, short_description, words, link):
        if self._cursor:
            try:
                self._cursor.execute(
                    "INSERT INTO documentIndex VALUES(?,?,?,?,?,?,?)",
                    doc_id, url, depth, title, short_description, words, link
                )
            except lite.Error as e:
                raise e
    '''
    def insert_to_db_links(self, destination_url_id, occurrence_number):
        if self._cursor:
            try:
                self._cursor.execute(
                    "INSERT INTO documentIndex VALUES(?,?)",
                    destination_url_id, occurrence_number
                )
            except lite.Error as e:
                raise e
    ''''

    def insert_to_db_lexicon(self, word_id, word):
        if self._cursor:
            try:
                self._cursor.execute(
                    "INSERT INTO documentIndex VALUES(?,?)",
                    word_id, word
                )
            except lite.Error as e:
                raise e

    def insert_to_db_InvertedIndex(self, word_id, doc_id):
        if self._cursor:
            try:
                self._cursor.execute(
                    "INSERT INTO documentIndex VALUES(?,?)",
                    word_id, doc_id
                )
            except lite.Error as e:
                raise e

    def insert_to_db_resolvedInvertedIndex(self, word, document_url):
        if self._cursor:
            try:
                self._cursor.execute(
                    "INSERT INTO documentIndex VALUES(?,?)",
                    word, document_url
                )
            except lite.Error as e:
                raise e

    def insert_to_db_pageRank(self, doc_id, rank_score):
        if self._cursor:
        try:
                self._cursor.execute(
                    "INSERT INTO documentIndex VALUES(?,?)",
                    doc_id, rank_score
                )
            except lite.Error as e:
                raise e
    
    def disconnect_db(self):
        self._db_conn.commit()
        self._db_conn.close()
