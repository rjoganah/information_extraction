'''
Created on 14 oct. 2016

@author: jogr0001
'''
import pickle
import json
ner_results = pickle.load(open('ner_google.txt','rb'))
ne_final = {}
for result in ner_results:
    for ne in result:
        key_name = ne['name'] + '_' + ne['type']
        if(key_name not in ne_final.keys()):
            ne_final[key_name] = 1
        else:
            ne_final[key_name] += 1
            
print(sorted(ne_final, key=ne_final.__getitem__, reverse=True))
