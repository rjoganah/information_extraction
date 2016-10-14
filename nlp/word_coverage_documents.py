'''
Created on 3 oct. 2016

@author: jogr0001
'''
import numpy as np
import csv
import pickle
from utils.utils import lemmatize,stem_and_lemmatize,lemmatize_and_stem
def word_coverage(words,documents):
    with open('unigramme_couverture.csv','w', newline='') as csvfile:
        csvwrter = csv.writer(csvfile,delimiter = ';')
        for word in words:
            words_cover = []
            
            for document in documents:
                if (word in document):
                    words_cover.append(1)       
                else:
                    words_cover.append(0)
            csvwrter.writerow([word,np.sum(np.array(words_cover)) / len(documents)])
        
def recall_keywords(words):
    count = 0
    recall = 22
    keywords_cp1 = ['nutrient','phosphorus','nitrogen','ammonia']
    keywords_cp2 = ['recover', 'reuse', 'concentration', 'valorisation']
    keywords_cp3 = ['wastewater',"waste","water","streams",'effluent', 'leachate', 'supernatant', 'swine', 'manure', 'liquid','fraction', 'treatment', 'digestate' ,'processing', 'sewage' ,'sludge',  'fermentation' ,'residu']
    keywords_cp4 = ['nutrient', 'recovery', 'technology', 'sustainable', 'renewable', 'fertiliser', 'fertilizer']
    keywords = set(keywords_cp1 + keywords_cp2 + keywords_cp3 + keywords_cp4)
    keywords_lem = set([lemmatize(word) for word in keywords])
    keywords_stem_lem = set([stem_and_lemmatize(word) for word in keywords])
    keywords_lem_stem = set([lemmatize_and_stem(word) for word in keywords])
    words = [stem_and_lemmatize(word) for word in words]
    for word in set(words):
        if word in set(keywords_stem_lem):
            print(word)
            count+=1
    print(len(set(keywords_stem_lem)))
    print (count / len(set(keywords_stem_lem)))

if __name__ == '__main__':
    with open('wastewater_nopos_uni_lennoregex' + '.csv', 'r', newline='') as csvfile:
        unigramreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        unigrammes = []
        for row in unigramreader:
            if(len(row) == 0):
                continue
            r = row[0]
            print(r)
            unigrammes.append(r)
    with open('wastewater_nopos_bifreq_lennoregex.csv', 'r', newline='') as csvfile:
        bigramreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        bigrammes = []
        for row in bigramreader:
            if(len(row) == 0):
                continue
            
            r = row[0].split(',')
            for w in r:
                bigrammes.append(w)
    with open('wastewater_nopos_tri_lennoregex.csv', 'r', newline='') as csvfile:
        trigramreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        trigrammes = []
        for row in trigramreader:
            r = row[0].split(',')
            
            for w in r:
                trigrammes.append(w)
        print(trigrammes)
    
    with open('word2vec_expansion.csv', 'r', newline='') as csvfile:
        w2vreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        w2v = []
        for row in w2vreader:
            for c in row[0:10]:
                w2v.append(stem_and_lemmatize(c))
    with open('word2vec_expansion_bigram.csv', 'r', newline='') as csvfile:
        w2vreaderbigram = csv.reader(csvfile, delimiter=';', quotechar='|')
        w2vbigram = []
        for row in w2vreaderbigram:
            for c in row[0:10]:
                w2vbigram.append(stem_and_lemmatize(c))
    with open('NMF_wastewater_18.csv', 'r', newline='') as csvfile:
        readersklearn = csv.reader(csvfile, delimiter=',', quotechar='|')
        sklearn_lda = []
        for row in readersklearn:
            for c in row:
                sklearn_lda.append(stem_and_lemmatize(c))           
    print(word_coverage(unigrammes, pickle.load(open('wastewater_nopos_len_noregex.pkl','rb'))))
    recall_keywords(unigrammes + bigrammes)
    print(len(set(unigrammes +  bigrammes)))