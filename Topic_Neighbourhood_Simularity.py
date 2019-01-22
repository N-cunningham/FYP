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
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]"]# TODO Come back to investiagte use of punctuation marks
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
part = input("What part of the text do you wish to compair (title/content)? ")

print(sourceA)
print(sourceB)
print(topic)
print(part)
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
                        if topic in article_content[part]:
                            data.append(article_content[part])


    data = ''.join(data)
    data = nltk.word_tokenize(data)
    neighbourhoods = []
    index = 0


    print("\n\n\nANALYSING NEIGHBOURHOODS\n\n\n")

    for index in range(len(data)):
        #print(data[index] + " & " + topic)
        if data[index] == topic:

            if data[index - 2] not in stopwords and data[index - 2] not in additional_stopords:
                neighbourhoods.append(data[index - 2])

            if data[index - 1] not in stopwords and data[index - 1] not in additional_stopords:
                neighbourhoods.append(data[index - 1])

            if data[index + 1] not in stopwords and data[index + 1] not in additional_stopords:
                neighbourhoods.append(data[index + 1])

            if data[index + 2] not in stopwords and data[index + 2] not in additional_stopords:
                neighbourhoods.append(data[index + 2])

            index = index + 2

        index = index + 1

    neighbourhoods = ' '.join(neighbourhoods)
    sourceData.append(neighbourhoods)

index2 = 0;
for sd in sourceData:
    print('\n' + sourceName[index2] + '\n')
    print(sd)
    index2 = index2 + 1


print(Utilities.get_cosine_sim(sourceData[0], sourceData[1]));
