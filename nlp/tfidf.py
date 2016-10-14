'''
Created on 30 sept. 2016

@author: jogr0001
'''

import sklearn
from sklearn.feature_extraction.text import  TfidfVectorizer, CountVectorizer
import pickle
from unidecode import unidecode
import numpy as np


f = open('wastewater_nopos_len.pkl','rb')
corpus = pickle.load(f)

tfidf_vectorizer = TfidfVectorizer(min_df=2, stop_words='english')
tfidf_vectorizer.fit_transform(corpus)
response = tfidf_vectorizer.transform(corpus)
feature_names = tfidf_vectorizer.get_feature_names()
print(len(feature_names))
#for value in np.argsort(response.nonzero()[1]):
#    print(value)
#    print(feature_names[value])

list_tuples = []
for col in response.nonzero()[1]:
    list_tuples.append((feature_names[col], response[0, col]))

print(sorted(set(list_tuples), key=lambda tup:tup[1], reverse = True)[0:50])
