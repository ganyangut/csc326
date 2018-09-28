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