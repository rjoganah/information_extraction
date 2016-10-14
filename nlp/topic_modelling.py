'''
Created on 26 sept. 2016

@author: jogr0001
'''
from sklearn.feature_extraction.text import  TfidfVectorizer, CountVectorizer
import lda
import numpy as np
import pickle
from graphic.tagcloud import create_tag_cloud
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import  NMF, LatentDirichletAllocation
import unidecode
#import matplotlib.pyplot as plt
#import math
import csv
import information_retrieval

from utils.utils import stem_and_lemmatize

class TopicModelling(object):
    '''
    classdocs
    '''
    n_features = 1000

    def __init__(self, data,filename):
        '''
        Constructor
        '''
        self.data = data
        self.vectorize(data)
        self.filename = filename
        
    def vectorize(self,corpus):
        self.count_vect = CountVectorizer()
        for i,line in enumerate(corpus):
            new_line = []
            for word in line:
                new_line.append(stem_and_lemmatize(word))
            corpus[i] = ' '.join(new_line)
        self.X_train_counts = self.count_vect.fit_transform(corpus)
        print(self.X_train_counts.shape)
        self.tf_vectorizer = CountVectorizer(max_df=0.99, min_df=2, stop_words='english')
        self.tf = self.tf_vectorizer.fit_transform(corpus)
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.99, min_df=2, max_features = self.n_features, stop_words='english')
        self.tfidf = self.tfidf_vectorizer.fit_transform(corpus)
        
    def print_top_words(self,model, feature_names, n_top_words):
#        count = 0
#        nb_topics = len(model.components_)
        with open(self.filename + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for topic_idx, topic in enumerate(model.components_):
            
#===============================================================================
#             num_top_words = 10
# 
#             fontsize_base =15/np.max(topic)
#             
#             
# 
#             
#             plt.subplot(1,1,1)  # plot numbering starts with 1
#             plt.subplots_adjust(left=0, bottom=0.1, right=8 , top=0.9, wspace=2, hspace=8)
#             plt.xlim(0,40)
#             plt.ylim(0, n_top_words/2 + 0.5)  # stretch the y-axis to accommodate the words
#             plt.xticks([])  # remove x-axis markings ('ticks')
#             plt.yticks([]) # remove y-axis markings ('ticks')
#             #plt.title('Topic #{}'.format(topic_idx))
#             top_words_idx = topic.argsort()[:-n_top_words - 1:-1]  # descending order
#             top_words_idx = top_words_idx[:num_top_words]
#             top_words = [feature_names[i] for i in top_words_idx]
#             top_words_shares = [topic[i] for i in top_words_idx]
#             plt.text(count, num_top_words+2,'Topic ' + str(topic_idx))
#             for i, (word, share) in enumerate(zip(top_words, top_words_shares)):
#                 plt.text(count, num_top_words-i, word, fontsize=fontsize_base*share)
#===============================================================================
         
            #plt.tight_layout()
                print("Topic #%d:" % topic_idx)
                top_words = ['topic_idx ' + str(topic_idx)] + [unidecode.unidecode(feature_names[i])
                                for i in topic.argsort()[:-n_top_words - 1:-1]]
                csvwriter.writerow(top_words)
                print(" ".join(top_words))
            
            #===================================================================
            # if(topic_idx == nb_topics-1):
            #     plt.savefig("Topics " + str(topic_idx-count) + '-' +  str(topic_idx) + self.filename + ".png")
            #     plt.close()
            # count += 1
            # if(count == 5):
            #     plt.savefig("Topics " + str(topic_idx-count+1) + '-' +  str(topic_idx) + self.filename + ".png")
            #     plt.close()
            #     count = 0
            #===================================================================
            
        print()
   
    
    def run_NMF(self,n_topics):
        n_top_words = 25
        nmf = NMF(n_components=n_topics).fit(self.tfidf)
        print("\nTopics in NMF model:")
        tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()
        self.print_top_words(nmf, tfidf_feature_names, n_top_words)
        
    def run_lda_sklearn(self,n_topics):
        n_top_words = 12
        lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        lda.fit(self.tf)
        print("\nTopics in LDA model:")
        tf_feature_names = self.tf_vectorizer.get_feature_names()
        self.print_top_words(lda, tf_feature_names, n_top_words)
        
    def run_lda(self):
        self.model = lda.LDA(n_topics=15, n_iter=500, random_state=1)
        self.model.fit(self.X_train_counts)
        self.topic_word = self.model.topic_word_
        pickle.dump(self.model,open('lda_model_wastewater_test_docsim.pkl','wb'))

        
    def load_lda(self):
        self.model = pickle.load(open('lda_model_NN.pkl','rb'))
        self.topic_word = self.model.topic_word_
        
    def transform_document(self,documents):
        X = self.count_vect.transform(documents)
        return X
        
    def write_topics(self):
        voc = self.count_vect.vocabulary_
        n_top_words = 15
        vocabulary = [(v,k) for k, v in voc.items()]
        sorted_voc = sorted(vocabulary,key=lambda value:value[0],reverse=False)
        vocabulary = [k.encode('utf-8') for v,k in sorted_voc]
        word_list_per_topic = []
        topics_words = []
        for i, topic_dist in enumerate(self.topic_word):
            topic_words = np.array(vocabulary)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
            word_list_per_topic.append(topic_words)
            topics_words.append([])
            for word in topic_words:
                topics_words[i].append(word)
        self.topics = topics_words
        return topics_words


    def cloud_tag_topic(self):
        for topic in self.topics:
            topic_string = b' '.join(list(topic))
            create_tag_cloud(topic_string.decode('utf-8'))
    
    def similarity(self,document):
        for topic_idx, topic in enumerate(self.model.components_):
            print(len(topic),topic)
            print(topic_idx,cosine_similarity(document, topic))
if __name__ == '__main__':
    data_transform = pickle.load(open('../information_retrieval/corpus_html_wastewater.pkl','rb'))
    data = pickle.load(open('wastewater_nopos_len_noregex.pkl','rb'))

    #===========================================================================
    # f = open('corpus_wordcloud_NN.txt','w')
    # for dat in data:
    #     f.write(unidecode.unidecode(dat))
    #===========================================================================
    topic_modelling = TopicModelling(data,'NMF_wastewater_18')
    #===========================================================================
    #LDA package
    # topic_modelling.run_lda()
    # topic_modelling.load_lda()
    # topics = topic_modelling.write_topics()
    # for i,topic in enumerate(topics):
    #     topic_string = b' '.join(list(topic))
    #     create_tag_cloud(topic_string.decode('utf-8'),'topicNN' + str(i))
    #     print('topicNN ' + str(i+1) + ' :', topic_string.decode('utf-8'))
    #===========================================================================
    #Sklearn LDA
    topic_modelling.run_NMF(18)
    #topic_modelling.run_lda_sklearn(10)
#    topic_modelling.load_lda()
    #topic_modelling.run_lda()
    #print(topic_modelling.write_topics()[7])
    #print(data_transform[4][0:100])
    #===========================================================================
    # data_transformed = topic_modelling.transform_document(data_transform)
    # 
    # components = topic_modelling.model.transform(data_transformed)
    # print (len(components))
    # 
    # for i,component in enumerate(components):
    #     print(component)
    #     print(np.sum(component),np.argsort(component))
    #     print(data_transform[i][0:500])
    #     if(i==10):
    #         break
    #===========================================================================
        
    #topic_modelling.similarity(components)
        
    

    