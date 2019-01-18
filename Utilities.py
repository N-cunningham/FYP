import nltk
import json
from os import listdir
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

months = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/")

class Article:
    def __init__(self, month, dates):
        self.month = month
        self.dates = dates

days_with_articles = []

for m in months:
    days = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + m)
    a1 = Article(m, days)
    days_with_articles.append(a1)

def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)

def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


def get_nouns(words):

    nouns = []

    for w in words:
        tagged_word = nltk.pos_tag(w)
        if (tagged_word[0][1] == 'NN' or tagged_word[0][1] == 'NNP' or tagged_word[0][1] == 'NNS' or tagged_word[0][1] == 'NNPS'):
                 nouns.append(w)
    return nouns


def save_as_JSON(list, file_end):

    with open('C:/Users/Niall/Desktop/FYP/Output JSON Data/' + file_end, 'w') as outfile:
        json.dump(list, outfile)


def get_sources():
    data = []
    article_sources_all = []
    i = 0

    for days_with_articles[i] in days_with_articles:
        for day in days_with_articles[i].dates:
            try:
                article_sources = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + days_with_articles[i].month + "/" + day + "/")
                for a in article_sources:
                    if a not in article_sources_all:
                        article_sources_all.append(a)
            except FileNotFoundError:
                print("No artilces published by "+ source + " on " + day)
                break
        i += 1

    return article_sources_all


def stem_tokens(tokens):
    stemmer = PorterStemmer()
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed
