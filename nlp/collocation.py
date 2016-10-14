# -*- coding: utf-8 -*-
'''
Created on 26 sept. 2016

@author: jogr0001
'''
import nltk
import pickle
from nltk.collocations import BigramCollocationFinder,TrigramCollocationFinder
from string import digits
from string import punctuation
from nltk.corpus import stopwords
import unidecode
#import time
import re
import csv
from utils.utils import stopwords_french,stem_and_lemmatize,lemmatize

corpus = pickle.load(open('../captation_pdfs_en.pkl','rb'))
corpus_fname = "captation_lem"

def print_n_gram_csv(n,data,filename):
    with open(filename + '.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            if(n==1):
                csvwriter.writerow([unidecode.unidecode(line)])
            elif(n==2):
                line = (unidecode.unidecode(line[0]),unidecode.unidecode(line[1]))
                csvwriter.writerow(line)
            elif(n==3):
                line = (unidecode.unidecode(line[0]),unidecode.unidecode(line[1]),unidecode.unidecode(line[2]))
                csvwriter.writerow(line)
    
       
        
corpus = [re.sub('\\W+',' ',doc) for doc in corpus]
list_sentences = [nltk.sent_tokenize(doc) for doc in corpus]
remove_digits = str.maketrans('', '', digits)
remove_punct = str.maketrans('', '', punctuation)
tokens_unique = []
list_tokens = []
stoplist = stopwords.words('english') 
#stoplist = stopwords_french()
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
docs_pos = []



print(stoplist)
for sentences in list_sentences:
    
    clean_sentences = [' '.join(sentence.split()) for sentence in sentences]
   
    tokens = [nltk.wordpunct_tokenize(sentence.translate(remove_digits)) for sentence in clean_sentences]
    
    #corpus_pos = nltk.pos_tag_sents(tokens)
    
    #'JJ','JJR','JJS','NNP','NN','NNS'
    #tokens = [tup[0].lower() for sentence in corpus_pos for tup in sentence if tup[1] in ['NN'] and tup[0].lower() not in stoplist ]
    tokens = [lemmatize(tup.lower()) for sentence in tokens for tup in sentence if tup.lower() not in stoplist and len(tup) > 3 ]
    tokens_unique += tokens
    docs_pos.append(' '.join(tokens))
    

    #===========================================================================
    # tokens_for_listokens = []
    # for token in tokens:
    #     token =  [t.lower() for t in token if t not in stoplist ]
    #         
    #     tokens_unique += token
    #     tokens_for_listokens += token
    # list_tokens.append(tokens_for_listokens)
    #===========================================================================
tokens_unique_final = tokens_unique

finder = BigramCollocationFinder.from_words(tokens_unique_final)
finder_tri = TrigramCollocationFinder.from_words(tokens_unique_final)

finder.apply_freq_filter(25)
finder_tri.apply_freq_filter(10)
#===============================================================================
# print("============================PMI==============================")
# print(finder.nbest(bigram_measures.pmi, 20))
# print (finder_tri.nbest(trigram_measures.pmi, 20))
# print("============================CHI_SQ==============================")
# print(finder.nbest(bigram_measures.chi_sq, 20))
# print (finder_tri.nbest(trigram_measures.chi_sq, 20))
#===============================================================================
print_n_gram_csv(2,finder.nbest(bigram_measures.chi_sq, 200),corpus_fname + "_nopos_bichi_sq")
print_n_gram_csv(3,finder_tri.nbest(trigram_measures.chi_sq, 200),corpus_fname + "_nopos_trischi_sq")

print_n_gram_csv(2,finder.nbest(bigram_measures.poisson_stirling, 200),corpus_fname + "_nopos_bipoisson_stirling")
print_n_gram_csv(3,finder_tri.nbest(trigram_measures.poisson_stirling, 200),corpus_fname + "_nopos_tripoisson_stirling")

print("============================PMI==============================")
print_n_gram_csv(2,finder.nbest(bigram_measures.pmi, 200),corpus_fname + "_nopos_bipmi")
print_n_gram_csv(3,finder_tri.nbest(trigram_measures.pmi, 200),corpus_fname + "_nopospmi_tri")
print("============================LIKELIHOOD==============================")
print_n_gram_csv(2,finder.nbest(bigram_measures.likelihood_ratio, 200),corpus_fname +"_nopos_bilik")
print_n_gram_csv(3,finder_tri.nbest(trigram_measures.likelihood_ratio, 200),corpus_fname +"_noposlki_tri")

fdist = nltk.FreqDist(tokens_unique_final)
print_n_gram_csv(1,sorted(fdist, key=fdist.__getitem__, reverse=True)[0:200],corpus_fname + "_nopos_uni")
fdist = nltk.FreqDist(nltk.bigrams(tokens_unique_final))
print_n_gram_csv(2,sorted(fdist, key=fdist.__getitem__, reverse=True)[0:200],corpus_fname  + "_nopos_bifreq")
fdist = nltk.FreqDist(nltk.trigrams(tokens_unique_final))
print_n_gram_csv(3,sorted(fdist, key=fdist.__getitem__, reverse=True)[0:200],corpus_fname  + "_nopos_trifreq")


f = open(corpus_fname + '_en.pkl','wb')
pickle.dump(docs_pos,f)
