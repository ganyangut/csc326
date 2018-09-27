from collections import OrderedDict

class history(OrderedDict):
    
    def __init__(self):
        OrderedDict.__init__(self)
    
    # the format of each entry is 
    # keyword : (number of times searched, how recent the keyword is saerched)
    # "how recent the keyword is saerched" is recorded in an integer, 1 means most recent, larger number means the keyword is older
    def add_new_keyword(self, keyword):
        
        self.make_keywords_old()
        
        # the keyword has been searched before
        if keyword in self:
            self[keyword] = (self[keyword][0]+1,1)
        # the keyword has not been searched before
        # the history is full
        elif len(self) == 20:
            self.popitem()
            self[keyword] = (1,1)
        # the keyword has not been searched before
        # the history is not full
        else:
            self[keyword] = (1,1)
        
        self.sort()
        
    def sort(self):
        self = OrderedDict(sorted(self.items(), key = lambda entry : entry[1][1]))
        self = OrderedDict(sorted(self.items(), key = lambda entry : entry[1][0], reverse=True))
        
        

        #print "sorted: " 
        #print (sorted(self.items(), key = lambda entry : entry[1][1]))
        print "sorted self: " 
        print self.items()

        #self = OrderedDict(sorted(self.items(), key = lambda entry : entry[0],reverse=True))


    def make_keywords_old(self):
        for keyword in self:
            self[keyword] = (self[keyword][0],self[keyword][1]+1)


        


    

    def get_last(self):
        last = next(reversed(self))
        return (last,self[last])


history= history()
history.add_new_keyword("a")

print history.items()

history.add_new_keyword("b")

print history.items()

history.add_new_keyword("b")

print history.items()

history.add_new_keyword("b")

print history.items()

history.add_new_keyword("a")

print history.items()

history.add_new_keyword("a")

print history.items()

history.add_new_keyword("a")

print history.items()

history.add_new_keyword("b")

print history.items()