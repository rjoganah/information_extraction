# -*- coding: utf-8 -*-
'''
Created on 14 oct. 2016

@author: jogr0001
'''
import re
import os
from unidecode import unidecode
path = 'C:/Users/cano2247/Downloads/SemEval2010.tar/SemEval2010/SemEval2010/train.tar/train/train/'
for dir in os.listdir(path):
    if dir.startswith(('C','I','H','J')):
        f = open(path + dir,encoding='utf8')
        corpus = f.read()
        for line in corpus:
            corpus += unidecode(line)
        #print(corpus)
        #print(corpus.replace('\\s',' '))
        #print(corpus.split(r'\n'))
        corpus = re.sub(r'\s',' ',corpus)
        print(dir,corpus[0:200])
    elif dir.startswith('train.combined.final'):
        f = open(path + dir,encoding='utf8')
        corpus = f.read()
        for result in (unidecode(corpus).split('\n')):
            print(result[0:5],result[7:].split(','))
        