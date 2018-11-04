from data_structures import *
from crawler import *
from pagerank import *
import os
import difflib

num_threads = 1

database_file = 'persistent_storage.db'
if os.path.isfile(database_file):
    os.remove(database_file)

start = timer()

db_conn = sqlite3.connect(database_file)
db_cursor = db_conn.cursor()
# Create table
db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS lexicon(
            crawler_id INTEGER,
            word_id INTEGER,
            word_string TEXT
        );
        CREATE TABLE IF NOT EXISTS inverted_index(
            crawler_id INTEGER,
            word_id INTEGER,
            document_id INTEGER,
            UNIQUE (crawler_id, word_id, document_id)
        );
        CREATE TABLE IF NOT EXISTS links(
            crawler_id INTEGER,
            from_document_id INTEGER,
            to_document_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS document_index(
            crawler_id INTEGER,
            document_id INTEGER,
            url TEXT, 
            title TEXT, 
            short_description TEXT
        );     
        CREATE TABLE IF NOT EXISTS page_rank(
            crawler_id INTEGER,
            document_id INTEGER,
            rank_value REAL
        );    
        """) 
db_conn.commit()

for crawler_id in range(num_threads):
    
    bot = crawler(db_conn, "urls.txt", crawler_id, num_threads)
    bot.crawl(depth=1)
    
    db_cursor.execute("SELECT from_document_id, to_document_id FROM links WHERE crawler_id = ?", (crawler_id, ))
    links = db_cursor.fetchall()
    page_rank_dict = page_rank(links)
    for document_id in page_rank_dict:
        db_cursor.execute('''INSERT INTO page_rank VALUES (?,?,?)''', (crawler_id, document_id, page_rank_dict[document_id]))
    db_conn.commit()

db_conn.close()

end = timer()
print "time used: "
print (end - start)



db_conn = sqlite3.connect(database_file)
db_cursor = db_conn.cursor()

db_cursor.execute("SELECT * FROM page_rank")
page_rank_dict = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM lexicon")
lexicon = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM inverted_index")
inverted_index = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM links")
links = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM document_index")
document_index = db_cursor.fetchall()

db_conn.close()
with open("test.out", 'w') as do:
    do.write("page rank:\n")
    for (crawler_id, document_id, rank_value) in page_rank_dict: 
        do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + str(rank_value) + ')' + '\n')
    
    do.write("links:\n")
    for link in links: 
        do.write(repr(link)+'\n')

    '''
    print "lexicon:"
    for (crawler_id, word_id, word) in lexicon: 
        do.write('(' + str(crawler_id) + ', ' + str(word_id) + ', ' + word + ')' + '\n')
    print "inverted index:"
    for entry in inverted_index: 
        do.write(repr(entry)+'\n')
    
    
    
    print "links:"
    for link in links: 
        do.write(repr(link)+'\n')
    print "document index:"
    for (crawler_id, document_id, url, title, short_description) in document_index: 
        if title and short_description:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + title + ', ' + short_description + ')' + '\n')
        elif title:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + title + ', ' + ')' + '\n')
        elif short_description:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + ', ' + short_description + ')' + '\n')
        else:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + ', '  + ')' + '\n')

    '''
