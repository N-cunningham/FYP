import sklearn
import nltk
from nltk import FreqDist
#from nltk.book import *
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from enum import Enum
from Utilities import get_sources
from Utilities import save_as_JSON


stopwords = set(stopwords.words('english'))
source = "AP"
sources = get_sources()
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


for s in sources:
    data = []
    warning = ""
#print(files)
    for a in articles:
        article_data = []
        for day in a.dates:
            file_exists = "true"
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                print("No artilces published by "+ s + " on " + day)
                file_exists = "false"

            if file_exists != "false":
                article_data = []
                for headline in article_headline:
                    with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s + "/" + headline, 'rb') as f:
                        try:
                            article_data = json.load(f)
                            data.append(article_data['html'])
                        except MemoryError:
                            print(' \n ***Too many aticles from ' + s + ' to batch process*** \n')
                            warning = "INCOMPLETE"
                            break
                        except ValueError:
                            print(' \n ***Decoding failed for '+ a.month + "/" + day + "/" + s + "/" + headline  + ' *** \n')




    all_news_source_data = []
    word_tokens = []
    if warning != "INCOMPLETE":
        try:
            all_news_source_data = ' '.join(data)
            word_tokens = word_tokenize(all_news_source_data)
        except MemoryError:
            print(' \n ***Too many aticles from ' + s + ' to batch process*** \n')
            warning = "INCOMPLETE"
            save_as_JSON( [], 'HTML/'+ 'INCOMPLETE_' + s + '_top_100_.json')
            save_as_JSON( [], 'HTML/'+ 'INCOMPLETE_' + s + '_Frequency_Distribution.json')

#print(all_NYT_data)
    if warning != "INCOMPLETE":

        #print(word_tokens[52][1])

        tags = []
        last = " "
        for w in word_tokens:
            #print("Last: "+ last)
            #print("this:" + w)
            if len(w) > 1 and w[0] == "/" and w[1] != "/" and last == "<":
                tags.append(w)
            last = w


        #print (tags)
        freq_dist = FreqDist(tags)
        freq_dist_top_100 = freq_dist.most_common(100)

        print(freq_dist_top_100)
        save_as_JSON(freq_dist_top_100, 'HTML/' + s +'_top_100.json')
        save_as_JSON(freq_dist,  'HTML/' + s + '_Frequency_Distribution.json')

print("Finito")
#filtered_sentence = []

#for w in word_tokens:
#    if w not in stopwords:
#        filtered_sentence.append(w)

#print(word_tokens)
#print(filtered_sentence)
