import urllib2
import urlparse
from BeautifulSoup import *

class MyDictionary:
    def translateWords(self,word):
        url='https://en.oxforddictionaries.com/definition/{}'.format(word)
        socket = urllib2.urlopen(url, timeout=3)
        soup = BeautifulSoup(socket.read())
        tranlation_semb = soup.find("ul", attrs= {"class":"semb"})

        if not tranlation_semb:
            return None
        translation_li = tranlation_semb.find('li')

        res = ''
        for li in translation_li:
            a=li.text.strip()
            b=a.replace("&lsquo;","")
            c=b.replace("&rsquo;","\n")
            d=c.replace("1","",1)
            res=d

        return res









  

    
    