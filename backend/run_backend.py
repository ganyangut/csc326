from data_structures import *
from crawler import *
from pagerank import *
import os
import difflib
import multiprocessing

def run_crawler(database_file, url_file, crawler_id, number_processes):
    bot = crawler(database_file, url_file, crawler_id, number_processes)
    bot.crawl(depth=1)

number_processes = 3
database_file_integrated = "persistent_storage.db"

start = timer()

dbfile_list = []
process_list = []

for crawler_id in range(number_processes):
    database_file = "persistent_storage" + str(crawler_id) + ".db"
    if os.path.isfile(database_file):
        os.remove(database_file)    
    p = multiprocessing.Process(target = run_crawler, args = (database_file, "urls.txt", crawler_id, number_processes))
    dbfile_list.append(database_file)
    process_list.append(p)
    p.start()
    
for p in process_list:   
    p.join()

end1 = timer()
start1 = end1

if os.path.isfile(database_file_integrated):
        os.remove(database_file_integrated)    
# Get connections to the databases
integrated_db_conn = sqlite3.connect(database_file_integrated)
integrated_db_cursor = integrated_db_conn.cursor()
integrated_db_cursor.executescript("""
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

integrated_db_conn.commit()

for database_file in dbfile_list:   
    db_conn = sqlite3.connect(database_file)
    db_cursor = db_conn.cursor()
    
    db_cursor.execute('SELECT * FROM lexicon')
    lexicon = db_cursor.fetchall()    
    integrated_db_cursor.executemany('INSERT INTO lexicon VALUES (?, ?, ?)', lexicon)
    
    db_cursor.execute('SELECT * FROM inverted_index')
    inverted_index = db_cursor.fetchall()    
    integrated_db_cursor.executemany('INSERT INTO inverted_index VALUES (?, ?, ?)', inverted_index)
    
    db_cursor.execute('SELECT * FROM document_index')
    document_index = db_cursor.fetchall()    
    integrated_db_cursor.executemany('INSERT INTO document_index VALUES (?, ?, ?, ?, ?)', document_index)
    
    db_cursor.execute('SELECT * FROM page_rank')
    page_rank = db_cursor.fetchall()    
    integrated_db_cursor.executemany('INSERT INTO page_rank VALUES (?, ?, ?)', page_rank)
    
    # clean up
    db_conn.close()

integrated_db_conn.commit()
integrated_db_conn.close()

end = timer()

print "time used 1: "
print (end1 - start)
print "time used 2: "
print (end - start1)
print "time used: "
print (end - start)

db_conn = sqlite3.connect(database_file_integrated)
db_cursor = db_conn.cursor()

db_cursor.execute("SELECT * FROM page_rank")
page_rank_dict = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM lexicon")
lexicon = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM inverted_index")
inverted_index = db_cursor.fetchall()
db_cursor.execute("SELECT * FROM document_index")
document_index = db_cursor.fetchall()

db_conn.close()
with open("test.out", 'w') as do:    
    
    do.write("document index:")
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
    print "lexicon:"
    for (crawler_id, word_id, word) in lexicon: 
        do.write('(' + str(crawler_id) + ', ' + str(word_id) + ', ' + word + ')' + '\n')
    print "inverted index:"
    for entry in inverted_index: 
        do.write(repr(entry)+'\n')
    
    do.write("page rank:\n")
    for (crawler_id, document_id, rank_value) in page_rank_dict: 
        do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + str(rank_value) + ')' + '\n')
    
    do.write("links:\n")
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
