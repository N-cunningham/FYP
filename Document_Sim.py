import nltk
from nltk import FreqDist
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Utilities
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

stopwords = set(stopwords.words('english'))
#sources = get_sources()
sourceName = []
sourceData = []
months = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/")

class Article:
    def __init__(self, month, dates):
        self.month = month
        self.dates = dates

articles = []

for i in months:
    days = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + i)
    a1 = Article(i, days)
    articles.append(a1)

sourceA = input("Type source A ")
sourceB = input("Type source B ")
topic = input("What is your topic to campair? ")

print(sourceA)
print(sourceB)
print(topic)
print("Fin")

sourceName.append(sourceA)
sourceName.append(sourceB)

for s in sourceName:
    data = []
    for a in articles:
        file_exists = "true"
        for day in a.dates:
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                print("No artilces published by "+ s + " on " + day)
                file_exists = "false"

            if file_exists == "true":
                for headline in article_headline:
                    with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s + "/" + headline, 'rb') as f:
                        article_content = json.load(f)
                        if topic in article_content['title']:
                            data.append(article_content['title'])

    #for ds in data:
        #word_tokenize(ds)
        #ds = Utilities.stem_tokens(ds)
    data = ' '.join(data)
    sourceData.append(data)

for sd in sourceData:
    print(sd)
    print('\n' +"NEW" + '\n')

print(Utilities.get_cosine_sim(sourceData[0], sourceData[1]));
