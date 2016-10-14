'''
Created on 30 sept. 2016

@author: jogr0001
'''
import nltk
import pickle
from unidecode import unidecode
import re
import nltk.tag.stanford as st
import os
import time
from information_retrieval.wikipedia_data import has_wikipedia_page

java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path
tagger = st.StanfordNERTagger("C:/Users/cano2247/Downloads/stanford-ner-2015-12-09/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz","C:/Users/cano2247/Downloads/stanford-ner-2015-12-09/stanford-ner-2015-12-09/stanford-ner.jar")
sents = pickle.load(open('../garnissage_pdfs_en.pkl','rb'))
    
def ner_recognition(): 
    sent = [nltk.sent_tokenize(sent) for sent in sents]
    tags = {}
    list_ner = []
    for s in sent:
        s = [nltk.word_tokenize(phrase) for phrase in s]
        ner_tags_stanford = tagger.tag_sents(s)
        list_ner += ner_tags_stanford
    print(len(list_ner))
    for ner_tags in list_ner:
        #print(unidecode(str(ner_tags)))
        grouped_tag = []
        prec_tag = 'O'
        for tag in ner_tags:
            if(prec_tag == 'O' and tag[1] != 'O'):
                grouped_tag.append(tag[0])
            elif(prec_tag == tag[1] and prec_tag != 'O'):
                grouped_tag.append(tag[0])
            if(tag[1] == 'O' and prec_tag != 'O' ):
                tag_key = ' '.join(grouped_tag)
                if tag_key not in tags.keys():
                    tags[tag_key] = (1,tag[1])
                else:
                    tags[tag_key] = (tags[tag_key][0] + 1,prec_tag)
                     
                grouped_tag = []
            prec_tag = tag[1]
    pickle.dump(tags,open('dict_tags_ner.pkl','wb'))
    return tags


    
#tags = pickle.load(open('dict_tags_ner.pkl','rb'))
tags = ner_recognition()
print(unidecode(str(tags)))
print(unidecode(str(sorted(tags, key=tags.__getitem__, reverse=True))))
for elem in sorted(tags, key=tags.__getitem__, reverse=True)[0:100]:
    if tags[elem][1] != 'LOCATION':
        print(elem,tags[elem])



def get_entities(chunks,listNE = ['GPE','ORGANIZATION','PERSON','LOC'],return_type = 'entities'):
    namedEnt = chunks
    entityList=[]
    for i in range(len(namedEnt)):
        #print(unidecode(str(namedEnt)))
        if  not isinstance(namedEnt[i][0], str):
                #print 'print named entity : ' + str(namedEnt[i])
            entity = ""
            for j in range(len(namedEnt[i])):
                if j==0:
                    entity = namedEnt[i][j][0]
                else:
                    entity = entity + " " + namedEnt[i][j][0]
            reNE = ""
            for NE in range(len(listNE)):
                if(NE==0):
                    reNE = listNE[NE]
                else:
                    reNE = reNE + "|" + listNE[NE]
     
            m = re.search('\(('+ reNE +')(\s)',str(namedEnt[i]))
            if m:
                typeEntity =  m.group(1)
                entityList.append((entity,typeEntity))
    return [(elem[0],elem[1]) for elem in entityList]
 
 
### GET TOP N NAMED ENTITIES 
all_entities = [get_entities(nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(s.encode('utf-8').decode('unicode_escape'))))) for s in sents]
token_left = [entity[0]  for entities in all_entities for entity in entities]
print(token_left[0:100])
fdist = nltk.FreqDist(token_left)
for k in (sorted(fdist, key=fdist.__getitem__, reverse=True)[0:30]):
    if(has_wikipedia_page(k)):
        print(k,fdist[k])
    
#===============================================================================
# IN = re.compile(r'.*\bin\b(?!\b.+ing)')
# for doc in [nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(s.encode('utf-8').decode('unicode_escape')))) for s in sents]:
#     for rel in nltk.sem.extract_rels('PERSON', 'LOC', doc, pattern = IN):
#         print(nltk.sem.rtuple(rel))
#===============================================================================
