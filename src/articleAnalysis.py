import numpy as np
import pandas as pd
import nltk
import networkx as nx
from nltk.tokenize import sent_tokenize
nltk.download('punkt') # one time execution
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
from sklearn.metrics.pairwise import cosine_similarity
from textExtraction import read_from_website
stop_words = stopwords.words('english')

# function to remove stopwords
def remove_stopwords(sen):
    '''
    Removes stopwords from the passed in sentence.
    Input: 
        sen - string
    Output:
        string
    '''
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

def summarize_text(article):
    '''
    Returns the 10 (or less) most important sentences from the passed in string.
    Input: 
         article - string 
    Output:
         string list
    '''
    # split articles by sentences and tokenize
    sentences = sent_tokenize(article)

    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

    # remove stopwords from the sentences
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

    # Extract word vectors
    word_embeddings = {}
    f = open('data/glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    sentence_vectors = []

    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    # similarity matrix
    sim_mat = np.zeros([len(sentences), len(sentences)])

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    
    # graph for similarity matrix
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    print("length of ranked_sentences = ", len(ranked_sentences))
    if(len(ranked_sentences) < 5):
        # return ranked_sentences[:len(ranked_sentences)][1]
        r_sentences = []
        for i in range(len(ranked_sentences)):
            r_sentences.append(ranked_sentences[i][1])
        return sentences
    else:
        r_sentences = []
        for i in range(5):
            r_sentences.append(ranked_sentences[i][1])
        return r_sentences
        # return ranked_sentences[:5][1]

def summarize_url(url):
    '''
    Input:
        url - string
    Output:
        string
    '''
    article_body = read_from_website(url)
    summarized_body = summarize_text(article_body)
    return summarized_body