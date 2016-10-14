'''
Created on 26 sept. 2016

@author: jogr0001
'''
import gensim
import pickle
import unidecode
import nltk
import csv

class Word2Vec():
    def __init__(self,corpus_name,model_fname):
        self.model = None
        self.model_fname = model_fname
        self.corpus_name = corpus_name
    
    def create_model(self):
        f = open(self.corpus_name,'rb')
        sentences = pickle.load(f)
        sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        #print(sentences[0][:50])
        model = gensim.models.Word2Vec(sentences, min_count=5,size=200)
        f.close()
        f = open(self.model_fname ,'wb')
        pickle.dump(model,f)
        f.close()
        
    def load_model(self):
        f = open(self.model_fname,'rb')
        self.model = pickle.load(f)
        
        
    def print_vocab_model(self):
        for word, _vocab_obj in self.model.vocab.items():
            print(unidecode.unidecode(word))

    def words_similarity(self,w1,w2):
        return self.model.similarity(w1, w2)
    
    def get_context_words(self, pos=[], neg=[]):
        print(pos)
        return pos + [tup[0]for tup in self.model.most_similar(positive=pos,negative=neg)]
    
    
if __name__ == '__main__':
   # w2v = Word2Vec('../information_retrieval/corpus_html_pos_wastewater.pkl','model_w2v_html_wastewater.pkl')
    #w2v = Word2Vec('captation_nopos_len_noregex.pkl','captation_model_w2v_nopos_len_noregex.pkl')
    w2v = Word2Vec('garnissage__lem_en.pkl','model_w2v_garnissage_lem.pkl')
    w2v.create_model()
    w2v.load_model()
    
    with open('garnissage__lem_nopos_bilik.csv','r',newline='') as csvfile:
        with open('Garnissage_word2vec_expansion.csv','w',newline='') as csvfile2:
            csvwriter = csv.writer(csvfile2, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvreader = csv.reader(csvfile,delimiter = ';')
            for line in csvreader:
                if len(line) > 0:
                    try:
                        csvwriter.writerow((w2v.get_context_words(pos = [unidecode.unidecode(line[0]),unidecode.unidecode(line[1])])))
                    except KeyError:
                        csvwriter.writerow([])
        
#    print(w2v.get_context_words(pos = ['sewage', 'sludge']))