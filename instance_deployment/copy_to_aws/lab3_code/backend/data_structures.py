from collections import OrderedDict


# each user has a own history
# each History stores up to 20 popular keywords
# key: user_email or "anonymous"
# value: History

    

class UserHistoryIndex(dict):
    def __init__(self):
        dict.__init__(self)

    # get user's history, if user history does not exist, create a new user history
    def get_history(self, _email):
        if _email in self.keys():
            return self[_email]
        # if user history does not exist, create a new user history
        self[_email] = History()
        return self[_email]

class History(OrderedDict):    
    
    def __init__(self):
        OrderedDict.__init__(self)    
    
    # the format of each entry is 
    # keyword : (number of times searched, how recent the keyword is searched)
    # "how recent the keyword is searched" is recorded in an integer, 1 means most recent, larger number means the keyword is older
    def add_new_keywords(self, words_list):        
        # make exsiting keywords old before adding new keyword
        self.make_keywords_old()        
        
        for keyword in words_list:
            # the keyword has been searched before
            if keyword in self:
                self[keyword] = (self[keyword][0]+1,1)
            # the keyword has not been searched before        
            else:
                self[keyword] = (1,1)        
        
        # sort the history after adding new keyword
        self.sort()        
    
    def sort(self):
        # sort key word by "number of times searched" first
        # if "number of times searched" is the same, rank depends on "how recent the keyword is searched"
        temp = OrderedDict(sorted(self.items(), key = lambda entry: (-entry[1][0], entry[1][1])))
        
        # assignment to self is not allowed, so we need to clear and add entries one by one 
        self.clear()        
        for entry in temp:
            self[entry] = temp[entry]

    # add 1 to "how recent the keyword is searched" for every existing  
    def make_keywords_old(self):        
        for keyword in self:
            self[keyword] = (self[keyword][0],self[keyword][1]+1)
    
    # get up to 20 popular keywords in history
    def get_popular(self):        
        popular = OrderedDict()
        counter = 0
        for entry in self:
            popular[entry] = self[entry]
            counter += 1
            if counter >= 20:
                break
        return popular.items()

# each user has a own RecentWords
# each RecentWords stores up to 10 recent keywords
# key: user_email
# value: RecentWords
class UserRecentWordsIndex(dict):
    def __init__(self):
        dict.__init__(self)

    # get user's recent words list, if recent words list does not exist, create a new recent words list
    def get_recent_words(self, _email):
        if _email in self.keys():
            return self[_email]
        # if user does not exist, create a new recent words list
        self[_email] = RecentWords()
        return self[_email]

class RecentWords(list):    
    
    def __init__(self):
        list.__init__(self)    
    
    def add_new_keywords(self, words_list):
        for keyword in words_list:
            # if the recent words list reached max size
            if len(self) == 10:
                self.pop()
            # insert at the head of the list
            self.insert(0, keyword)


# key is document id
# value is document
class DocumentIndex(OrderedDict):    
    
    def __init__(self):
        OrderedDict.__init__(self)

    def __setitem__(self, key, val):
        if not isinstance(key, int):
            raise ValueError("document_index key must be an int")
        if not isinstance(val, Document):
            raise ValueError("document_index value must be a document")
        return OrderedDict.__setitem__(self, key, val)

# a data structure for each entry in the document index
class Document():    
    
    def __init__(self, url="", depth=0, title="", short_description="", words=None):
        if not isinstance(url, basestring):
            raise ValueError("document url must be a basestring")
        if not isinstance(depth, int):
            raise ValueError("document depth must be an int")
        if not isinstance(title, basestring):
            raise ValueError("document title must be a basestring")
        if not isinstance(short_description, basestring):
            raise ValueError("document short_description must be a basestring")
        self.url = url
        self.depth = depth
        self.title = title
        self.short_description = short_description        
        self.words = words        

    def __repr__(self):
        if self.words:
            return ", ".join([self.url, str(self.depth), self.title, self.short_description, str(len(self.words))])
        else:
            return ", ".join([self.url, str(self.depth), self.title, self.short_description, "", ""])

# key is word id
# value is as set of document ids
class InvertedIndex(dict):    
    
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, key, val):
        if not isinstance(key, int):
            raise ValueError("inverted_index key must be an int")
        if not isinstance(val, set):
            raise ValueError("inverted_index value must be a set")
        return dict.__setitem__(self, key, val)

    def add(self, word_id, document_id):
        if not isinstance(word_id, int):
            raise ValueError("word_id must be an int")
        if not isinstance(document_id, int):
            raise ValueError("document_id must be an int")

        if word_id in self:
            self[word_id].add(document_id)
        else:
            self[word_id] = set([document_id])

# key is word string
# value is as set of document urls
class ResolvedInvertedIndex(dict):    
    
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, key, val):
        if not isinstance(key, basestring):
            raise ValueError("resolved_inverted_index key must be a basestring")
        if not isinstance(val, set):
            raise ValueError("resolved_inverted_index value must be a set")
        return dict.__setitem__(self, key, val)

    def add(self, word_str, document_url):
        if not isinstance(word_str, basestring):
            raise ValueError("word_str must be a basestring")
        if not isinstance(document_url, basestring):
            raise ValueError("document_url must be a basestring")

        if word_str in self:
            self[word_str].add(document_url)
        else:
            self[word_str] = set([document_url])