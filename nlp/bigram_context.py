'''
Created on 7 oct. 2016

@author: jogr0001
'''
from utils.utils import read_csv,load_pickle,lemmatize,pre_process_corpus_pos
from unidecode import unidecode
import pickle
from nlp.BoW import vectorize_and_transform,measure_similarity_vectors
class BigramContext(object):
    '''
    classdocs
    '''


    def __init__(self, corpus_fname, bigrams_fname):
        '''
        Constructor
        '''
        self.corpus,self.tags = pre_process_corpus_pos(load_pickle('../captation_pdfs_en.pkl'))
        #self.corpus = pickle.load(open('tok_garnissage_pos.pkl','rb'))
        #self.tags = pickle.load(open('tags_garnissage_pos.pkl','rb'))
        
        self.bigrams = read_csv(bigrams_fname,';')
#        self.corpus = load_pickle(corpus_fname)
    
    
    def collect_context(self):
        bigrams_context = {}

        self.bigrams = self.bigrams[0:10]
        for bigram in self.bigrams:
            print(bigram)
            bigram_name = bigram[0] + '_' + bigram[1]
            bigrams_context[bigram_name] = {}

        tokens_document = self.corpus
        for bigram in self.bigrams:
            
            if(bigram[0] in tokens_document):
                #limit = 0
                bigram_name = bigram[0] + '_' + bigram[1]
                indexes = [i for i,token in enumerate(tokens_document) if bigram[0] == token]
                for i in indexes:
                    if (tokens_document[i+1] == bigram[1]):
                        tokens = tokens_document[i-2:i] + tokens_document[i+2:i+4]
                        t = self.tags[i-4:i] + self.tags[i+2:i+6]
                        for j,token in enumerate(tokens):
                            #+ '_' + t[j]
                            if token not in bigrams_context[bigram_name].keys():
                                #+ '_' + t[j][0:2]
                                bigrams_context[bigram_name][token] = 1
                            else:
                                bigrams_context[bigram_name][token] += 1
                        
                #===============================================================
                # while (bigram[1] in tokens_document[limit:] and bigram[0] in tokens_document[limit:]):
                #     id_bigram_left = tokens_document[limit:].index(bigram[0])
                #     id_bigram_rigt = tokens_document[limit:].index(bigram[1])
                #     if (id_bigram_rigt - id_bigram_left == 1 and id_bigram_rigt != len(tokens_document[limit:]) - 1):
                #             
                #         token_after = lemmatize(tokens_document[limit:][id_bigram_rigt + 1])
                #         token_before = lemmatize(tokens_document[limit:][id_bigram_left - 1])
                #         if token_after not in bigrams_context[bigram_name].keys():
                #             bigrams_context[bigram_name][token_after] = 1
                #         else:
                #             bigrams_context[bigram_name][token_after] += 1
                #                 
                #         if token_before not in bigrams_context[bigram_name].keys():
                #                 bigrams_context[bigram_name][token_before] = 1
                #         else:
                #             bigrams_context[bigram_name][token_before] += 1
                #                 
                #     limit = limit + id_bigram_left + 1
                #===============================================================
        bigrams_vectors = []
        bigram_index = []
        for k in bigrams_context.keys():
            bigrams_vectors.append(' '.join(sorted(bigrams_context[k], key=bigrams_context[k].__getitem__, reverse=True)))
            bigram_index.append(k)
            print(k, sorted(bigrams_context[k], key=bigrams_context[k].__getitem__, reverse=True))
            print ([bigrams_context[k][i] for i in sorted(bigrams_context[k], key=bigrams_context[k].__getitem__, reverse=True)])
            if 'bark_NN' in bigrams_context[k]:
                print(bigrams_context[k]['bark_NN'])
        print(bigrams_vectors)
        pairs = measure_similarity_vectors(vectorize_and_transform(bigrams_vectors))
        f = open('strong_pairs_captation.txt','w')
        pairs_sorted = sorted(pairs, key=lambda p:p[2], reverse=True)
        strong_pairs = []
        index_strong = []
        weak_pair = []
        for pair in pairs_sorted:
            if(pair[0] not in index_strong and pair[1] not in index_strong):
                strong_pairs.append(pair)
                index_strong.append(pair[0])
                index_strong.append(pair[1])
            else:
                weak_pair.append(pair)

        for pair in strong_pairs:
            f.write(str(pair) + '\n')
            f.write(str(bigram_index[pair[0]])+ '\n')
            f.write(str(bigram_index[pair[1]])+ '\n'+ '\n')
        
                        
                        
                    
            




if __name__ == '__main__':
    #getBigramContext = BigramContext('garnissage__lem_en.pkl','garnissage__lem_nopos_bilik.csv')
    getBigramContext = BigramContext('captation_nopos_len_noregex.pkl','captation_lem_nopos_bipoisson_stirling.csv')
    getBigramContext.collect_context()
