'''
Created on 28 sept. 2016

@author: jogr0001
'''
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import time
import pickle
import re
from unidecode import unidecode
import nltk

class Extraction():
    """Extraction class from the url."""
    def __init__(self):
        self.test = ""
        #self.url = url
        #print(self.url)
        #self.get_html()
    
    def search_on_google(self,query):
        encoded_query =  urlencode({'q':query})
        new_links = []
        
        for nb_page in range(0,100):
            if(nb_page == 0):
                page = requests.get("https://www.google.ca/search?" + encoded_query)
            else:
                page = requests.get("https://www.google.ca/search?" + encoded_query + "&start=" + str(nb_page*10))
            soup = BeautifulSoup(page.content)
        
            #links = soup.findAll("a")

            for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
                l = re.split(":(?=http)",link["href"].replace("/url?q=",""))
                if len(l)==1:
                    n_substr=l[0].find('&sa')
                    new_links.append(l[0][:n_substr])
            time.sleep(5)
        self.new_links = new_links
        f = open('linkswastewater_google1000.pkl','wb')
        pickle.dump(new_links,f)
    def get_html(self,url):
        
        headers = {
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                     }
        self.html = requests.get(url, headers=headers).content
        
    def url_scrapping(self):
        corpus_dict = {}
        for i,l in enumerate(self.new_links):
            print(l)
            corpus = ""
            if(l.endswith('.pdf')):
                continue
            try:
                headers = {
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
                     }
                html = requests.get(l, timeout=10, headers=headers)
                bs = BeautifulSoup(html.content)
                paragraphs = bs.find_all("p")
                for p in paragraphs:
                    text = p.get_text()
                    if len(text) > 50:
                        corpus += text
            except requests.exceptions.Timeout as _e:
                print("TIMEOUT")
            except requests.exceptions.ConnectionError as _e:
                print("Connection error")
            corpus_dict[l] = corpus
        f = open('corpus_html_wastewater.pkl','wb')
        pickle.dump(corpus_dict,f)
    
    def corpus_extraction(self):
        new_links = self.new_links
        corpus_dict_pfile = open('corpus_html_wastewater.pkl','rb')
        corpus_dict = pickle.load(corpus_dict_pfile)
        corpus_dict_pfile.close()
        corpus_NN_JJ = []
        stopwords = nltk.corpus.stopwords.words('english')
        for i,l in enumerate(new_links):
            if(not l.endswith('pdf')):
                print(i,l)
                
                    
                text = corpus_dict[l].encode('utf-8')
                text = unidecode(text.decode('utf-8'))
                
                if(i==11 or i==141 or i==244):
                    print(l)
                    continue
                    print(text)
                sentences = nltk.sent_tokenize(text)
                tokens = [nltk.word_tokenize(sent) for sent in sentences]
                pos = [nltk.pos_tag(tok) for tok in tokens]
                tuple_to_keep = []
                for _j,sent in enumerate(pos):
                    for _k,tup in enumerate(sent):
                        
                        if(tup[0] not in stopwords):
                            
                            tuple_to_keep.append(tup[0])
        
                corpus_NN_JJ.append(' '.join(tuple_to_keep))
        f = open('corpus_html_wastewater.pkl','wb')
        pickle.dump(corpus_NN_JJ,f)
        print(corpus_NN_JJ[0:10])
    def load_links(self):
        self.new_links = pickle.load(open('linkswastewater_google1000.pkl','rb'))
        
    def read_links(self):
        print(len(set(self.new_links)))
        print(self.new_links)


if __name__ == '__main__':
    #query = '"maple sugar" OR "maple syrup" OR "maple sirup" OR "maple sap" or "maple water" -festival -meteo -spring -harvest -production -police -cartel -court -battle -"nyse" -"tsx" -"nasdaq" -dizzle'
    query = '"nutrient recovery" technologies OR technology OR sustainable OR renewable OR fertilizer "waste water" OR wastewater OR "liquid fraction" OR leachate OR supernatant OR effluent'
    ext = Extraction()
   # ext.search_on_google(query)
    ext.load_links()
    #ext.url_scrapping()

    ext.corpus_extraction()