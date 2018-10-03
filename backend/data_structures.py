from collections import OrderedDict


class history(OrderedDict):    
    
    def __init__(self):
        OrderedDict.__init__(self)    
    
    # the format of each entry is 
    # keyword : (number of times searched, how recent the keyword is saerched)
    # "how recent the keyword is saerched" is recorded in an integer, 1 means most recent, larger number means the keyword is older
    def add_new_keyword(self, keyword):        
        # make exsiting keywords old before adding new keyword
        self.make_keywords_old()        
        
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
        # if "number of times searched" is the same, rank depends on "how recent the keyword is saerched"
        temp = OrderedDict(sorted(self.items(), key = lambda entry : (-entry[1][0], entry[1][1])))
        
        # assignment to self is not allowed, so we need to clear and add entries one by one 
        self.clear()        
        for entry in temp:
            self[entry] = temp[entry]

    # add 1 to "how recent the keyword is saerched" for every existing  
    def make_keywords_old(self):        
        for keyword in self:
            self[keyword] = (self[keyword][0],self[keyword][1]+1)
    
    def get_last(self):
        last = next(reversed(self))
        return (last,self[last])
    
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


class document_index(OrderedDict):    
    
    def __init__(self):
        OrderedDict.__init__(self)

    def __setitem__(self, key, val):
        if not isinstance(key, int):
            raise ValueError("document_index key must be an int")
        if not isinstance(val, document):
            raise ValueError("document_index value must be a document")
        return OrderedDict.__setitem__(self, key, val)

class document():    
    
    def __init__(self, url="", depth=0, title="", short_description="", words=None, links=None):
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
        self.links = links

    # TODO improve this
    def __repr__(self):
        if self.words and self.links:
            return ", ".join([self.url, str(self.depth), self.title, self.short_description, str(len(self.words)), str(len(self.links))])
        else:
            return ", ".join([self.url, str(self.depth), self.title, self.short_description, "", ""])
'''
class words(list):    
    
    def __init__(self):
        list.__init__(self)

    def __setitem__(self, val):
        if not isinstance(val, word):
            raise ValueError("words value must be a word")
        return list.__setitem__(self, val)

class word(tuple):    
    
    def __init__(self, word_id, font_size):
        tuple.__init__(self)

    def __setitem__(self, val):
        if not isinstance(val, word):
            raise ValueError("words value must be a word")
        return list.__setitem__(self, val)
'''
class links_(dict):    
    
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, key, val):
        if not isinstance(key, int):
            raise ValueError("links_ key must be an int")
        if not isinstance(val, int):
            raise ValueError("links_ value must be an int")
        return dict.__setitem__(self, key, val)

class lexicon(dict):    
    
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, key, val):
        if not isinstance(key, int):
            raise ValueError("lexicon key must be an int")
        if not isinstance(val, basestring):
            raise ValueError("lexicon value must be a basestring")
        return dict.__setitem__(self, key, val)

class inverted_index(dict):    
    
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

class resolved_inverted_index(dict):    
    
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