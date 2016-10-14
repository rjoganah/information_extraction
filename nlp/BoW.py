'''
Created on 11 oct. 2016

@author: jogr0001
'''
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def vectorize(documents):
    
    count_vect = CountVectorizer()
    count_vect = count_vect.fit(documents)
    return count_vect

def bag_of_words(count_vect,document):
    return count_vect.transform(document)

def vectorize_and_transform(documents):
    count_vect = vectorize(documents)
    print(count_vect.vocabulary_)
    return bag_of_words(count_vect,documents).todense()

def measure_similarity_vectors(vectors):
    pair = []
    for i,vector in enumerate(vectors):
        for j,v in enumerate(vectors[i:]):
            sim = cosine_similarity(vector,v)
            if((not np.allclose(sim[0][0],np.float64(1.0)) and (not np.allclose(sim[0][0],np.float64(0.0))))):
                if(sim[0][0] > 0.1):
                    #sim[0][0], vector, v,
                    pair.append((i,i+j,sim[0][0]))
    return pair
                
if __name__ == '__main__':
    vectors = vectorize_and_transform(['hello world','world hello Test', 'hello morld','morld velo'])
    print(vectors)
    measure_similarity_vectors(vectors)
    
        
    