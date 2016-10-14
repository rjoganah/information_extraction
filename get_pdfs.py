# -*- coding: utf-8 -*-
'''
Created on 26 sept. 2016

@author: jogr0001
'''
from tika import parser
import os
import pickle
from langdetect import detect

# -*- coding: utf-8 -*-
class PDFExtraction():
    def __init__(self):
        self.path = "F:\documents pour analyse\captation composés souffrés"
        #self.path = "F:\documents pour analyse\watewater nutrient recovery"
        self.path = "G:/CRIQ/Jean-Luc Morin/documents pour analyse/garnissage biofiltre/articles PDF"
        self.files = os.listdir(self.path)
        
        
    
    def print_pdfs(self):
        corpus_en = []
        corpus_fr = []
        scanned_docs = []
        for file in self.files:
            if file.endswith('.pdf'):
                print(file)
                self.text = parser.from_file(self.path + '\\' + file)
                if(self.text['content'] != None):
                    if(detect(self.text['content'])=='en'):
                        corpus_en.append(self.text['content'])
                    elif(detect(self.text['content'])=='fr'):
                        corpus_fr.append(self.text['content'])
                else:
                    scanned_docs.append(file)
        f = open('garnissage_pdfs_en.pkl','wb')
        pickle.dump(corpus_en,f)
        f.close()
        f = open('garnissage_pdfs_fr.pkl','wb')
        pickle.dump(corpus_fr,f)
        f.close()
        print('####scanned docs')
        print(scanned_docs)
        
if __name__ == '__main__':
    extraction_pdf = PDFExtraction()
    extraction_pdf.print_pdfs()
    