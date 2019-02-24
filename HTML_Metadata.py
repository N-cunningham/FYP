import sklearn
import nltk
from nltk import FreqDist
#from nltk.book import *
import json
import time
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from enum import Enum
from Utilities import get_sources
from Utilities import save_as_JSON


stopwords = set(stopwords.words('english'))
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]", "’", "|", "‘", "'", ".", " ", "e", "i", "a", "r", "."]# TODO Come back to investiagte use of punctuation marks
source = "AP"
sources = []
sources = get_sources()
#sources.append(source)
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
    tags = []
    words = ""
    article_data = ""
    time1 = time.localtime()
    print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": Processing articles in " + s + "...")

    for a in articles:
        for day in a.dates:
            article_data = []
            file_exists = "true"
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                #print("No artilces published by "+ s + " on " + day)
                file_exists = "false"

            if file_exists != "false":
                article_data = []
                for headline in article_headline:
                    with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s + "/" + headline, 'rb') as f:
                        try:
                            del article_data
                            article_data = json.load(f)
                            del words
                            words = word_tokenize(article_data['html'])
                            last = " "
                            for w in words:
                                if len(w) > 1 and w[0] == "/" and w[1] != "/" and last == "<":
                                    data.append(w)
                                last = w
                        except MemoryError:
                            print(' \n ***Too many aticles from ' + s + ' to batch process*** \n')
                            warning = "INCOMPLETE"
                            break
                        except ValueError:
                            print(' \n ***Decoding failed for '+ a.month + "/" + day + "/" + s + "/" + headline  + ' *** \n')


    all_news_source_data = []
    word_tokens = []
    if warning != "INCOMPLETE":
        time2 = time.localtime()
        print(str(time2.tm_hour) + ":" + str(time2.tm_min) + ":" + str(time2.tm_sec) + ": Tokenizing article HTML tags in " + s + "...")
        try:
            all_news_source_data = ' '.join(map(str, data))
            word_tokens = word_tokenize(all_news_source_data)
        except MemoryError:
            print(' \n ***Too many aticles from ' + s + ' to batch process*** \n')
            warning = "INCOMPLETE"
            save_as_JSON( [], 'HTML/'+ 'INCOMPLETE_' + s + '_top_100_.json')
            save_as_JSON( [], 'HTML/'+ 'INCOMPLETE_' + s + '_Frequency_Distribution.json')

#print(all_NYT_data)
    if warning != "INCOMPLETE":


        #print (tags)
        freq_dist = FreqDist(word_tokens)
        freq_dist_top_100 = freq_dist.most_common(100)

        print(s)
        print(freq_dist_top_100)
        print("\n")
        save_as_JSON(freq_dist_top_100, 'HTML/' + s +'_top_100.json')
        save_as_JSON(freq_dist,  'HTML/' + s + '_Frequency_Distribution.json')

print("Finito")
#filtered_sentence = []

#for w in word_tokens:
#    if w not in stopwords:
#        filtered_sentence.append(w)

#print(word_tokens)
#print(filtered_sentence)
