import nltk
from nltk import FreqDist
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import xlsxwriter
import Utilities
from Utilities import get_sources
from Utilities import get_nouns

stopwords = set(stopwords.words('english'))
source = "RT"
sources = get_sources()
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

data = []
i = 0
#print(files)
for s in sources:
    i = 0
    for a in articles:
        for day in articles[i].dates:
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                print("No artilces published by "+ s + " on " + day)
                break
            for headline in article_headline:
                with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s + "/" + headline, 'rb') as f:
                    NYT =json.load(f)
                    data.append(NYT['title'])
        i += 1

all_news_source_data = ' '.join(data)
word_tokens = word_tokenize(all_news_source_data)

filtered_titles = []
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!']# TODO Come back to investiagte use of punctuation marks

nouns = get_nouns(word_tokens)

for w in nouns:
    if w not in stopwords and w not in additional_stopords:
       filtered_titles.append(w)

freq_dist = FreqDist(filtered_titles)
freq_dist_top_100= freq_dist.most_common(100)
print(freq_dist_top_100)
print(freq_dist)

freq_dist.plot(20, title = source + " Distribution of top 20 title words across all data")
