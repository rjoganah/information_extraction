# -*- coding: utf-8 -*-
'''
Created on 3 oct. 2016

@author: jogr0001
'''
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import csv
import pickle
import re
from unidecode import unidecode
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from gensim.matutils import corpus2csc

wordnet_lemmatizer = WordNetLemmatizer()



def lemmatize(word):
    return wordnet_lemmatizer.lemmatize(word)

def stem_and_lemmatize(word):
    stemmer = PorterStemmer()
    return lemmatize(stemmer.stem(word))

def lemmatize_and_stem(word):
    stemmer = PorterStemmer()
    return stemmer.stem(lemmatize(word))

def stopwords_french():
    stoplist = stopwords.words('french') 
    stoplist_ranks_nl = [word[:-2].decode('unicode_escape') for word in open('../utils/stopwords_french.txt','rb')]
    stoplist += stoplist_ranks_nl
    print(stoplist_ranks_nl)
    for word in stoplist:
        print(word)
        if 'é' in word:
            stoplist.append(word.replace('é','e'))
        if 'à' in word:
            stoplist.append(word.replace('à','a'))
        if 'è' in word:
            stoplist.append(word.replace('è','e'))
        if 'ô' in word:
            stoplist.append(word.replace('ô','o'))
        if 'ê' in word:
            stoplist.append(word.replace('ê','e'))
        if 'û' in word:
            stoplist.append(word.replace('û','u'))
        if 'î' in word:
            stoplist.append(word.replace('î','i'))
    
    return set(stoplist)

def read_csv(filename,delim=','):
    if filename.endswith('.csv'):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delim, quotechar='|')
            return [elem for elem in reader]
    else:
        with open(filename + '.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delim, quotechar='|')
            return [elem for elem in reader]
        

def load_pickle(filename):
    return pickle.load(open(filename,'rb'))



def pre_process_corpus_pos(corpus):
    tok,tags = [],[]
    uniform_space = [re.sub('\s+',' ',doc) for doc in corpus]
    corpus_of_tokens = [word_tokenize(unidecode(doc)) for doc in uniform_space]
    corpus_tagged = [nltk.pos_tag(tokens) for tokens in corpus_of_tokens]
    for elements in corpus_tagged:
        for element in elements:
            if(element[0].lower() not in stopwords.words('english') and len(element[0]) > 3 ):
                tok.append(element[0])
                tags.append(element[1])
    return tok,tags
    

def alpha_punct(text):
    return ' '.join([word for word in nltk.wordpunct_tokenize(text) if (word.isalnum() or word in punctuation)])
            
if __name__ == '__main__':
    print(stopwords_french())
    print (pre_process_corpus_pos(['Treatment of ozonated, water in b!otilters contain.','test here if it works not sure\n', 'why not']))