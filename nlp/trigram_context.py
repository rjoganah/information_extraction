'''
Created on 11 oct. 2016

@author: jogr0001
'''
from utils.utils import read_csv,load_pickle,lemmatize,pre_process_corpus_pos
import itertools



tri_fname = 'garnissage__lem_noposlki_tri.csv'
tri = read_csv(tri_fname,';')
words = {}
for t in tri:
    for perm in (itertools.permutations(t)):
        print(perm)
    for word in t:
        if word in words.keys():
            words[word] += 1
        else:
            words[word] = 1
print(sorted(words,key=words.__getitem__,reverse=True))
