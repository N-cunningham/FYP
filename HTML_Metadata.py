import sklearn
import nltk
from nltk import FreqDist
#from nltk.book import *
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from enum import Enum

stopwords = set(stopwords.words('english'))
source = "FrontPage Magazine"
#date = "2017-04-19"
#start_month = "April"

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

NYT_APR_19 = []
data = []
i = 0
#print(files)
for articles[i] in articles:
    for day in articles[i].dates:
        try:
            article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + articles[i].month + "/" + day + "/" + source)
        except FileNotFoundError:
            print("No artilces published by "+ source + " on " + day)
            break
        for headline in article_headline:
            with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + articles[i].month + "/" + day + "/" + source + "/" + headline, 'rb') as f:
                NYT =json.load(f)
                data.append(NYT['html'])
    i += 1

all_news_source_data = ' '.join(data)
#print(all_NYT_data)
word_tokens = word_tokenize(all_news_source_data)

#print(word_tokens[52][1])

tags = []

for w in word_tokens:
    if len(w) > 1 and w[0] == "/" and w[1] != "/":
        tags.append(w)

#print (tags)
freq_dist = FreqDist(tags)

print(freq_dist.most_common(20))

print(freq_dist)

freq_dist.plot(20, title = source + " Distribution of top 20 HTML tags across all data")

#filtered_sentence = []

#for w in word_tokens:
#    if w not in stopwords:
#        filtered_sentence.append(w)

#print(word_tokens)

#print(filtered_sentence)
