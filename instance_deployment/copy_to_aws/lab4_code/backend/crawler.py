# Copyright (C) 2011 by Peter Goodman
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import urllib2
import urlparse
from BeautifulSoup import *
from collections import defaultdict
from data_structures import *
from pagerank import *
import re
import unicodedata
import sqlite3

from timeit import default_timer as timer

def attr(elem, attr):
    """An html attribute from an html element. E.g. <a href="">, then
    attr(elem, "href") will get the href or an empty string."""
    try:
        return elem[attr]
    except:
        return ""

WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')

class crawler(object):
    """Represents 'Googlebot'. Populates a database by crawling and indexing
    a subset of the Internet.
    This crawler keeps track of font sizes and makes it simpler to manage word
    ids and document ids."""

    def __init__(self, database_file, url_file, crawler_id, number_processes):
        """Initialize the crawler with a connection to the database to populate
        and with the file containing the list of seed URLs to begin indexing."""
        
        self.crawler_id = crawler_id
        
        self.db_conn = sqlite3.connect(database_file)
        self.db_cursor = self.db_conn.cursor()
        # Create table
        self.db_cursor.executescript("""
                CREATE TABLE IF NOT EXISTS lexicon(
                    crawler_id INTEGER,
                    word_id INTEGER,
                    word_string TEXT
                );
                CREATE TABLE IF NOT EXISTS inverted_index(
                    crawler_id INTEGER,
                    word_id INTEGER,
                    document_id INTEGER,
                    rank_value REAL,
                    UNIQUE (crawler_id, word_id, document_id)
                );
                CREATE TABLE IF NOT EXISTS document_index(
                    crawler_id INTEGER,
                    document_id INTEGER,
                    url TEXT, 
                    title TEXT, 
                    short_description TEXT
                );                 
                """) 

        self.db_conn.commit()

        self._url_queue = [ ]
        self._doc_id_cache = { }
        self._word_id_cache = { }

        self.document_index = DocumentIndex()
        self.inverted_index = InvertedIndex()
        self.resolved_inverted_index = ResolvedInvertedIndex()
        self.lexicon = { }
        self.links = set()

        # functions to call when entering and exiting specific tags
        self._enter = defaultdict(lambda *a, **ka: self._visit_ignore)
        self._exit = defaultdict(lambda *a, **ka: self._visit_ignore)

        # add a link to our graph, and indexing info to the related page
        self._enter['a'] = self._visit_a

        # record the currently indexed document's title an increase
        # the font size
        def visit_title(*args, **kargs):
            self._visit_title(*args, **kargs)
            self._increase_font_factor(10)(*args, **kargs)

        # increase the font size when we enter these tags
        self._enter['b'] = self._increase_font_factor(2)
        self._enter['strong'] = self._increase_font_factor(2)
        self._enter['i'] = self._increase_font_factor(1)
        self._enter['em'] = self._increase_font_factor(1)
        self._enter['h1'] = self._increase_font_factor(7)
        self._enter['h2'] = self._increase_font_factor(6)
        self._enter['h3'] = self._increase_font_factor(5)
        self._enter['h4'] = self._increase_font_factor(4)
        self._enter['h5'] = self._increase_font_factor(3)
        self._enter['title'] = visit_title

        # decrease the font size when we exit these tags
        self._exit['b'] = self._increase_font_factor(-2)
        self._exit['strong'] = self._increase_font_factor(-2)
        self._exit['i'] = self._increase_font_factor(-1)
        self._exit['em'] = self._increase_font_factor(-1)
        self._exit['h1'] = self._increase_font_factor(-7)
        self._exit['h2'] = self._increase_font_factor(-6)
        self._exit['h3'] = self._increase_font_factor(-5)
        self._exit['h4'] = self._increase_font_factor(-4)
        self._exit['h5'] = self._increase_font_factor(-3)
        self._exit['title'] = self._increase_font_factor(-10)

        # never go in and parse these tags
        self._ignored_tags = set([
            'meta', 'script', 'link', 'meta', 'embed', 'iframe', 'frame', 
            'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset', 
            'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
        ])

        # set of words to ignore
        self._ignored_words = set([
            '', 'the', 'of', 'at', 'oamazon', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

        # initialize ids
        self._next_doc_id = 1
        self._next_word_id = 1

        # keep track of some info about the page we are currently parsing
        self._curr_depth = 0
        self._curr_url = ""
        self._curr_doc_id = 0
        self._font_size = 1
        self._curr_words = None

        # get all urls into the queue
        line_counter = 0        
        try:
            with open(url_file, 'r') as f:
                for line in f:
                    if line_counter % number_processes == crawler_id:
                        self._url_queue.append((self._fix_url(line.strip(), ""), 0))                        
                    line_counter += 1
        except IOError:
            pass
    
    def _insert_document(self, url):
        """A function that inserts a url into a document db table
        and then returns that newly inserted document's id."""
                
        ret_id = self._next_doc_id
        self._next_doc_id += 1

        new_document = Document(url=url)
        self.document_index[ret_id] = new_document

        return ret_id
    
    def _insert_word(self, word):
        """A function that inserts a word into the lexicon db table
        and then returns that newly inserted word's id."""
        ret_id = self._next_word_id
        self._next_word_id += 1

        # add word to lexicon        
        self.lexicon[ret_id] = word

        # insert into database
        self.db_cursor.execute("INSERT INTO lexicon VALUES (?,?,?)", (self.crawler_id, ret_id, word))

        return ret_id
    
    def word_id(self, word):
        """Get the word id of some specific word."""
        if word in self._word_id_cache:
            word_id = self._word_id_cache[word]
        else:
            # 1) add the word to the lexicon, if that fails, then the
            #    word is in the lexicon
            # 2) query the lexicon for the id assigned to this word, 
            #    store it in the word id cache, and return the id.
            word_id = self._insert_word(word)
            self._word_id_cache[word] = word_id            
        
        # add the word to inverted index and resolved inverted index
        self.inverted_index.add(word_id, self._curr_doc_id, self._font_size)
        self.resolved_inverted_index.add(word, self._curr_url)   
        
        return word_id
    
    def document_id(self, url):
        """Get the document id for some url."""
        if url in self._doc_id_cache:
            return self._doc_id_cache[url]
        
        # if the document doesn't exist in the db
        # then only insert the url and leave
        # the rest to their defaults        
        doc_id = self._insert_document(url)
        self._doc_id_cache[url] = doc_id

        # insert into database
        self.db_cursor.execute('''INSERT INTO document_index (crawler_id, document_id, url) 
                                VALUES (?,?,?)''', (self.crawler_id, doc_id, url))

        return doc_id
    
    def _fix_url(self, curr_url, rel):
        """Given a url and either something relative to that url or another url,
        get a properly parsed url."""

        rel_l = rel.lower()
        if rel_l.startswith("http://") or rel_l.startswith("https://"):
            curr_url, rel = rel, ""
            
        # compute the new url based on import 
        curr_url = urlparse.urldefrag(curr_url)[0]
        parsed_url = urlparse.urlparse(curr_url)
        fixed_url = urlparse.urljoin(parsed_url.geturl(), rel)
        try:
            if isinstance(fixed_url, unicode):
                fixed_url = unicodedata.normalize('NFKD', fixed_url).encode('ascii','ignore')
        finally:
            return fixed_url

    def add_link(self, from_doc_id, to_doc_id):
        """Add a link into the database. 
        When a page contains multiple links to a document, 
        only the first link should be counted. """
        
        self.links.add((from_doc_id, to_doc_id))

    def _visit_title(self, elem):
        """Called when visiting the <title> tag."""
        title_text = self._text_of(elem).strip()
        if title_text:        
            # change unicode string to ascii string
            if isinstance(title_text, unicode):
                title_text = unicodedata.normalize('NFKD', title_text).encode('ascii','ignore')

            # update document title for document id self._curr_doc_id
            self.document_index[self._curr_doc_id].title = title_text

            # insert into database
            self.db_cursor.execute('''UPDATE document_index SET title = ? WHERE crawler_id = ? AND document_id = ? ''', 
                                    (title_text, self.crawler_id, self._curr_doc_id))
    
    def _visit_a(self, elem):
        """Called when visiting <a> tags."""

        dest_url = self._fix_url(self._curr_url, attr(elem,"href"))

        skip = False
        # if dest_url has been visited, no need to add title again
        if dest_url in self._doc_id_cache:
            skip = True

        # add the just found URL to the url queue
        self._url_queue.append((dest_url, self._curr_depth))
        
        # add a link entry into the database from the current document to the
        # other document
        self.add_link(self._curr_doc_id, self.document_id(dest_url))        
        
        # add depth and title/alt/text to index for destination url
        if not skip:
            self.document_index[self.document_id(dest_url)].depth = self._curr_depth            
            
    def _add_words_to_document(self):
        # knowing self._curr_doc_id and the list of all words and their
        # font sizes (in self._curr_words), add all the words into the
        # database for this document
        self.document_index[self._curr_doc_id].words = self._curr_words

    def _increase_font_factor(self, factor):
        """Increade/decrease the current font size."""
        def increase_it(elem):
            self._font_size += factor
        
        return increase_it
    
    def _visit_ignore(self, elem):
        """Ignore visiting this type of tag"""
        pass

    def _add_text(self, elem):
        """Add some text to the document. This records word ids and word font sizes
        into the self._curr_words list for later processing."""
        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue
            # change unicode string to ascii string
            if isinstance(word, unicode):
                word = unicodedata.normalize('NFKD', word).encode('ascii','ignore')
            self._curr_words.append((self.word_id(word), self._font_size))
        
    def _text_of(self, elem):
        """Get the text inside some element without any tags."""
        if isinstance(elem, Tag):
            text = [ ]
            for sub_elem in elem:
                text.append(self._text_of(sub_elem))            
            return " ".join(text)
        else:
            return elem.string

    def _index_document(self, soup):
        """Traverse the document in depth-first order and call functions when entering
        and leaving tags. When we come accross some text, add it into the index. This
        handles ignoring tags that we have no business looking at."""
        class DummyTag(object):
            next = False
            name = ''
        
        class NextTag(object):
            def __init__(self, obj):
                self.next = obj
        
        tag = soup.html
        stack = [DummyTag(), soup.html]

        while tag and tag.next:
            tag = tag.next

            # html tag
            if isinstance(tag, Tag):

                if tag.parent != stack[-1]:
                    self._exit[stack[-1].name.lower()](stack[-1])
                    stack.pop()

                tag_name = tag.name.lower()

                # ignore this tag and everything in it
                if tag_name in self._ignored_tags:
                    if tag.nextSibling:
                        tag = NextTag(tag.nextSibling)
                    else:
                        self._exit[stack[-1].name.lower()](stack[-1])
                        stack.pop()
                        tag = NextTag(tag.parent.nextSibling)
                    
                    continue                
                
                # enter the tag
                self._enter[tag_name](tag)
                stack.append(tag)

                # if no title tag, use h1 as title
                if tag_name == "h1":

                    h1_text = self._text_of(tag).strip()
                    
                    if h1_text:
                        # change unicode string to ascii string
                        if isinstance(h1_text, unicode):
                            h1_text = unicodedata.normalize('NFKD', h1_text).encode('ascii','ignore')
                        if not self.document_index[self._curr_doc_id].title:                    
                            # update document title for document id self._curr_doc_id_font_size
                            self.document_index[self._curr_doc_id].title = h1_text
                            # insert into database
                            self.db_cursor.execute('''UPDATE document_index SET title = ? WHERE crawler_id = ? AND document_id = ? ''', 
                                                    (h1_text, self.crawler_id, self._curr_doc_id))
                        elif not self.document_index[self._curr_doc_id].short_description:
                            self.document_index[self._curr_doc_id].short_description = h1_text
                
                # if no short_description, use h2 h3 h4 as short_description
                if (tag_name == "h2" or tag_name == "h3" or tag_name == "h4") and not self.document_index[self._curr_doc_id].short_description:
                    h234_text = self._text_of(tag).strip()
                    if h234_text:
                        # change unicode string to ascii string
                        if isinstance(h234_text, unicode):
                            h234_text = unicodedata.normalize('NFKD', h234_text).encode('ascii','ignore')
                        self.document_index[self._curr_doc_id].short_description = h234_text
            
            # text (text, cdata, comments, etc.)
            #else:
            try:
                self._add_text(tag)
            except:
                pass

    def crawl(self, depth=2, timeout=3):
        """Crawl the web!"""
        seen = set()
        
        while len(self._url_queue):

            url, depth_ = self._url_queue.pop()            

            # skip this url; it's too deep
            if depth_ > depth:
                continue

            doc_id = self.document_id(url)

            # we've already seen this document
            if doc_id in seen:
                continue

            seen.add(doc_id) # mark this document as haven't been visited
            
            # record the depth of current document
            self.document_index[doc_id].depth = depth_

            socket = None
            try:
                socket = urllib2.urlopen(url, timeout=timeout)
                soup = BeautifulSoup(socket.read())

                self._curr_depth = depth_ + 1
                self._curr_url = url
                self._curr_doc_id = doc_id
                self._font_size = 1
                self._curr_words = [ ]
                self._index_document(soup)
                self._add_words_to_document()
                
                # extract short description form meta description field
                short_description = soup.find("meta", attrs= {'name': 'description'})
                if short_description:
                    short_description = short_description["content"]
                    if short_description:
                        if isinstance(short_description, unicode):
                            short_description = unicodedata.normalize('NFKD', short_description).encode('ascii','ignore')
                        self.document_index[self._curr_doc_id].short_description = short_description                 
            
            except Exception as e:
                print "Exception as e:"
                print "url: " + url
                print "depth: " + str(depth_)
                print e                
                pass
            finally:
                if socket:
                    socket.close()
  
        # insert into database
        for document_id in self.document_index:          
            self.db_cursor.execute('''UPDATE document_index SET short_description = ? WHERE crawler_id = ? AND document_id = ? ''', 
                                    (self.document_index[document_id].short_description, self.crawler_id, document_id))       

        page_rank_dict = page_rank(self.links)
        
        for word_id in self.inverted_index:             
            for document_id in self.inverted_index[word_id]: 
                if document_id in page_rank_dict and self.inverted_index[word_id][document_id]:
                    self.inverted_index[word_id][document_id] = self.inverted_index[word_id][document_id] * 0.0001 + page_rank_dict[document_id] * 100
            self.inverted_index[word_id] = sorted(self.inverted_index[word_id].items(), key = lambda x: -x[1])
            for (document_id, rank_value) in self.inverted_index[word_id]:
                self.db_cursor.execute("INSERT INTO inverted_index VALUES (?,?,?,?)", (self.crawler_id, word_id, document_id, rank_value))

        # commit changes
        self.db_conn.commit()
        self.db_conn.close()
            
    def get_inverted_index(self):
        return self.inverted_index

    def get_resolved_inverted_index(self):
        return self.resolved_inverted_index

    def get_title(self, doc_id):
        if doc_id not in self.document_index:
            raise KeyError("doc_id not valid")
        return self.document_index[doc_id].title
    
    def get_short_description(self, doc_id):
        if doc_id not in self.document_index:
            raise KeyError("doc_id not valid")
        return self.document_index[doc_id].short_description

if __name__ == "__main__":    
    
    start = timer()
    
    db_conn = sqlite3.connect('example.db')
    bot = crawler(db_conn, "urls.txt", 0, 4)
    bot.crawl(depth=0)

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    db_conn.close()

    end = timer()

    print "time used: "
    print (end - start)