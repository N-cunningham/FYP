import sklearn
import nltk
from nltk import FreqDist
import json
import time
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from enum import Enum
from Utilities import get_sources
from Utilities import save_as_JSON
import Utilities
from sklearn.metrics.pairwise import cosine_similarity


stopwords = set(stopwords.words('english'))
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]", "’", "|", "‘", "'", ".", " ", "e", "i", "a", "r", "."]# TODO Come back to investiagte use of punctuation marks
source = "CNBC"
sources = []
freqDists = []
freqDistsNames = []
sourcesAlreadyDone = ["CNBC", "BBC"]
#sources = get_sources()


reliableSources = ["AP", "The Daily Beast", "Media Matters for America", "The Fiscal Times", "CNBC", "Talking Points Memo"]
for rs in reliableSources:
    sources.append(rs)
reliableTags = []

quesionableSources = ["Alternative Media Syndicate", "Breitbart", "Freedom Daily", "Liberty Writers", "Infowars", "Intellihub", "FrontPage Magazine"]
for qs in quesionableSources:
    sources.append(qs)
quesionableTags = []

satireSources = ["The Beaverton" , "The Chaser", "The Shovel", "The Spoof" , "Glossy News", "Newslo", "Humor Times", "The Burrard Street Journal", "The Borowitz Report", "The Huffington Post Political Satire", "National Report"]
for ss in satireSources:
    sources.append(ss)
satireTags = []


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

data = []
for s in sources:
    del data[:]
    warning = ""
    tags = []
    words = " "
    article_data = " "
    time1 = time.localtime()
    print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": Processing articles in " + s + "...")
    aCounter = 0
    for a in articles:
        time1 = time.localtime()
        if aCounter == 1:
            print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": 14% done")

        if aCounter == 2:
            print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": 29% done")

        if aCounter == 4:
            print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": 57% done")

        if aCounter == 5:
            print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": 71% done")

        if aCounter == 6:
            print(str(time1.tm_hour) + ":" + str(time1.tm_min) + ":" + str(time1.tm_sec) + ": 86% done")

        aCounter = aCounter + 1

        for day in a.dates:

            file_exists = "true"
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                #print("No artilces published by "+ s + " on " + day)
                file_exists = "false"

            if file_exists != "false":

                for headline in article_headline:
                    article_data = []
                    with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s + "/" + headline, 'rb') as f:
                        try:
                            del article_data
                            article_data = json.load(f)
                            del words
                            words = word_tokenize(article_data['html'])
                            last = " "
                            for w in words:
                                if len(w) > 1 and w[0] == "/" and w[1] != "/" and last == "<":#THis line detects HTML tags
                                    data.append(w)
                                last = w
                        except MemoryError:
                            print(' \n ***Too many aticles from ' + s + ' to batch process*** \n')
                            warning = "INCOMPLETE"
                            break
                        except ValueError:
                            print(' \n ***Decoding failed for '+ a.month + "/" + day + "/" + s + "/" + headline  + ' *** \n')


    all_news_source_data = []
    del all_news_source_data[:]
    word_tokens = []
    del word_tokens[:]

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
        freqDistsNames.append(s)
        print(freq_dist_top_100)

        if s in reliableSources:
            reliableTags.append(word_tokens)
        elif s in quesionableSources:
            quesionableTags.append(word_tokens)
        elif s in satireSources:
            satireTags.append(word_tokens)


        print("\n")
        save_as_JSON(freq_dist_top_100, 'HTML/' + s +'_top_100.json')
        save_as_JSON(freq_dist,  'HTML/' + s + '_Frequency_Distribution.json')


reliableTagsAll = ' '.join(map(str, reliableTags))
quesionableTagsAll = ' '.join(map(str, quesionableTags))
satireTagsAll = ' '.join(map(str, satireTags))

print("Reliable")
print(Utilities.get_cosine_sim(reliableTagsAll, satireTagsAll))

print("\nQuesionable")
print(Utilities.get_cosine_sim(quesionableTagsAll, satireTagsAll))

print("Finito")
#filtered_sentence = []

#for w in word_tokens:
#    if w not in stopwords:
#        filtered_sentence.append(w)

#print(word_tokens)
#print(filtered_sentence)
