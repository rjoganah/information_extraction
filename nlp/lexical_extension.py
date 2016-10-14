'''
Created on 27 sept. 2016

@author: jogr0001
'''
from nltk.corpus import wordnet as wn
import csv
from _sqlite3 import Row

def lemmas(topics_words):
    lexical_expansion = []
    for word in topics_words:
        synsets = wn.synsets(word)
            #print synsets
        print('================' + word +  '=================')
        for synset in synsets:
            #===================================================================
            # print(synset.definition())
            # print("Lemmas",synset.lemma_names())
            # print("Hyponyms",synset.hyponyms())
            # print("holonymes", synset.member_holonyms())
            # print("Hypernymes",synset.hypernyms())
            #===================================================================
            lexical_expansion.append((word,synset.definition().replace(';',','),synset.lemma_names(),[hypo.name() for hypo in synset.hyponyms()],[hyper.name() for hyper in synset.hypernyms()],[holo.name()for holo in synset.member_holonyms()]))
    return lexical_expansion


def print_lexical_csv(data,filename):
    with open(filename + '.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['WORD','DEFINITION','LEMMAS','HYPONYMS','HYPERNYMS','HOLONYMS'])
        for line in data:
            csvwriter.writerow(line)

def common_hypern():
    with open('unigrammes_lexical.csv', 'r', newline='') as csvfile:
        w2vreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        hypernyms_common = {}
        for row in w2vreader:
            hypernym_name = row[4][2:-2].split('.')[0]
            print(hypernym_name)
            if(hypernym_name in hypernyms_common.keys()):
                hypernyms_common[hypernym_name].append(row[0])
            else:
                hypernyms_common[hypernym_name] = [row[0]]
    for k,v in hypernyms_common.items():
        if len(v)>1:
            print(k,v)
    
if __name__ == '__main__':
    with open('captation_nopos_uni_lennoregex' + '.csv', 'r', newline='') as csvfile:
        unigramreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        unigrammes = []
        for row in unigramreader:
            r = row[0]
            print(r)
            unigrammes.append(r)
         
        print_lexical_csv(lemmas(unigrammes),'unigrammes_captation_lexical')
    #common_hypern()