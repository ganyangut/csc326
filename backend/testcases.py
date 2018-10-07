import unittest
from crawler import crawler

'''lexicon
    93: 'aided'
'''

'''document_id
    1, http://www.eecg.toronto.edu/
'''

'''inverted_index
    93: set([1])
'''

'''resolved_inverted_index
    'aided': set(['http://www.eecg.toronto.edu/']), 
    'limited': set(['http://www.eecg.toronto.edu/~enright', 'http://www.eecg.utoronto.ca/~ashvin']), 
    'extrapolated': set(['http://www.eecg.toronto.edu/~enright'])
'''

class testCrawler(unittest.TestCase):
    def setUp(self):
        self.bot = crawler(None, "urls.txt")
        self.bot.crawl(depth=1)
        '''
        fo=open("lexicon.txt","wb")
        fo.write(repr(self.bot.lexicon))      
        fo.close()

        fo2=open("document_index.txt","wb")
        fo2.write(repr(self.bot.document_index))
        fo2.close()
        '''

    def test_inverted_index(self): 
        '''
        self.inverted_index=self.bot.get_inverted_index()

        fo=open("inverted_index.txt","wb")
        fo.write(repr(self.inverted_index))
        fo.close()
        '''

        #test url:http://www.eecg.toronto.edu/
        print ("test inverted_index \n")
        print self.bot.get_inverted_index()[93]
        key=self.bot.get_inverted_index()[93]
        value= set([1])
        self.assertEqual(key,value)
        

        


    def test_resolved_inverted_index(self):
        '''
        self.resolved_inverted_index=self.bot.get_resolved_inverted_index()
        fo=open("resolved_inverted_index.txt","wb")
        fo.write(repr(self.resolved_inverted_index))
        fo.close()
        '''

        #test url:http://www.eecg.toronto.edu/
        print ("test resolved_inverted_index \n")
        print self.bot.get_resolved_inverted_index()['aided']
        
        self.assertEqual(self.bot.get_resolved_inverted_index()['aided'],set(['http://www.eecg.toronto.edu/']))
        self.assertEqual(self.bot.get_resolved_inverted_index()['limited'],set(['http://www.eecg.toronto.edu/~enright', 'http://www.eecg.utoronto.ca/~ashvin']))


if __name__ == "__main__":
    unittest.main()