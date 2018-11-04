import nltk
from nltk import FreqDist
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import xlsxwriter

stopwords = set(stopwords.words('english'))
source = "RT"
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
                data.append(NYT['title'])
    i += 1

all_news_source_data = ' '.join(data)
word_tokens = word_tokenize(all_news_source_data)

filtered_titles = []
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ]# TODO Come back to investiagte use of punctuation marks

for w in word_tokens:
    if w not in stopwords and w not in additional_stopords:
       filtered_titles.append(w)

freq_dist = FreqDist(filtered_titles)
freq_dist_top_40 = freq_dist.most_common(40)
print(freq_dist_top_40)
print(freq_dist)

freq_dist.plot(20, title = source + " Distribution of top 20 title words across all data")
