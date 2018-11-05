from data_structures import *
from crawler import *
from pagerank import *
import os
import difflib

os.remove('example.db')

start = timer()
    
db_conn = sqlite3.connect('example.db')
bot = crawler(db_conn, "urls.txt", 0, 4)
bot.crawl(depth=0)
db_conn.close()

end = timer()

print "time used: "
print (end - start)

with open("raw.out", 'w') as ro:
    
    for word_id in bot.lexicon: 
        ro.write('(' + str(bot.crawler_id) + ', ' + str(word_id) + ', ' + bot.lexicon[word_id] + ')' + '\n')
    for word_id in bot.inverted_index: 
        for document_id in bot.inverted_index[word_id]: 
            ro.write('(' + str(bot.crawler_id) + ', ' + str(word_id) + ', ' + str(document_id) + ')' + '\n')
    for link in bot.links: 
        ro.write(repr(link)+'\n')
    for document_id in bot.document_index: 
        ro.write('(' + str(bot.crawler_id) + ', ' + str(document_id) + ', ' + bot.document_index[document_id].url
                + ', ' + bot.document_index[document_id].title + ', ' + bot.document_index[document_id].short_description + ')' + '\n')

with open("db.out", 'w') as do:
    db_conn = sqlite3.connect('example.db')
    db_cursor = db_conn.cursor()

    db_cursor.execute("SELECT * FROM lexicon")
    lexicon = db_cursor.fetchall()
    db_cursor.execute("SELECT * FROM inverted_index")
    inverted_index = db_cursor.fetchall()
    db_cursor.execute("SELECT * FROM links")
    links = db_cursor.fetchall()
    db_cursor.execute("SELECT * FROM document_index")
    document_index = db_cursor.fetchall()
    
    db_conn.close()

    for (crawler_id, word_id, word) in lexicon: 
        do.write('(' + str(crawler_id) + ', ' + str(word_id) + ', ' + word + ')' + '\n')
    for entry in inverted_index: 
        do.write(repr(entry)+'\n')
    for link in links: 
        do.write(repr(link)+'\n')
    for (crawler_id, document_id, url, title, short_description) in document_index: 
        if title and short_description:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + title + ', ' + short_description + ')' + '\n')
        elif title:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + title + ', ' + ')' + '\n')
        elif short_description:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + ', ' + short_description + ')' + '\n')
        else:
            do.write('(' + str(crawler_id) + ', ' + str(document_id) + ', ' + url + ', ' + ', '  + ')' + '\n')\

# compare raw data in crawler and data in database
with open('raw.out', 'r') as rr:
    with open('db.out', 'r') as dr:
        diff = difflib.unified_diff(rr.readlines(), dr.readlines(), fromfile='raw.out', tofile='db.out', lineterm='', n=0)
        lines = list(diff)[2:]
        added = [line[1:] for line in lines if line[0] == '+']
        removed = [line[1:] for line in lines if line[0] == '-']
        if not added:
            print "identical"
        else:
            print 'additions:'
            for line in added:
                print line
            print
            print 'additions, ignoring position:'
            for line in added:
                if line not in removed:
                    print line




"""
CREATE TABLE IF NOT EXISTS lexicon(
    crawler_id INTEGER,
    word_id INTEGER,
    word_string TEXT
);
CREATE TABLE IF NOT EXISTS inverted_index(
    crawler_id INTEGER,
    word_id INTEGER,
    document_id INTEGER
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
"""