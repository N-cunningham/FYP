import sys
import sklearn
import nltk
from nltk import FreqDist
import json
import time
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Utilities import get_sources
from Utilities import save_as_JSON
import Utilities
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

stopwords = set(stopwords.words('english'))
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]", "’", "|", "‘", "'", ".", " ", "e", "i", "a", "r", "."]# TODO Come back to investiagte use of punctuation marks
source = "CNBC"
sources = []
freqDists = []
freqDistsNames = []
sourcesAlreadyDone = ["CNBC", "BBC"]
#sources = get_sources()


reliableSources = ["BBC", "CBS News", "CNBC", "NPR", "PBS", "Slate"]#, "The Atlantic"]#, "The Daily Beast", "The Hill", "Salon", "The Huffington Post", "The New York Times", "USA Today", "Vox", "Washington Examiner", "Media Matters for America", "The Fiscal Times", "AP", "Talking Points Memo"]
for rs in reliableSources:
    sources.append(rs)
reliableTags = []

quesionableSources = ["Alternative Media Syndicate", "Bipartisan Report", "Breitbart", "CNS News", "Conservative Tribune", "Freedom Daily", "Liberty Writers", "Hang The Bankers", "Infowars"]#, "Intellihub", "FrontPage Magazine"]#, "Occupy Democrats", "Politicus USA", "Prntly","RedState", "The Duran", "TruthFeed", "USA Politics Now", "End the Fed", "NODISINFO", "Freedom Outpost", "Waking Times", "NewsBusters", "Activist Post", "The D.C. Clothesline","World News Politics", "Daily Buzz Live", "DC Gazette"]
for qs in quesionableSources:
    sources.append(qs)
quesionableTags = []

satireSources = satireSources = ["The Beaverton" , "The Chaser", "The Shovel", "The Spoof" , "Glossy News", "Newslo", "Humor Times", "The Burrard Street Journal", "The Borowitz Report", "The Huffington Post Political Satire", "National Report"]
for ss in satireSources:
    sources.append(ss)
satireTags = []

sourcesTags = []

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
    filename = "C:/Users/Niall/Desktop/FYP/Output JSON Data/HTML/Pickle/"+ s + ".pickle"
    if os.path.isfile(filename) == False:
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


        if warning != "INCOMPLETE":
            time2 = time.localtime()
            print(str(time2.tm_hour) + ":" + str(time2.tm_min) + ":" + str(time2.tm_sec) + ": Tokenizing article HTML tags in " + s + "...")
            try:
                data = ' '.join(map(str, data))
                data = word_tokenize(data)

            except MemoryError:
                print(' \n ***Too many aticles from ' + s + ' to batch process*** \n')
                warning = "INCOMPLETE"
                save_as_JSON( [], 'HTML/'+ 'INCOMPLETE_' + s + '_top_100_.json')
                save_as_JSON( [], 'HTML/'+ 'INCOMPLETE_' + s + '_Frequency_Distribution.json')

    #print(all_NYT_data)
        if warning != "INCOMPLETE":
            #print (tags)
            freq_dist = FreqDist(data)
            freq_dist_top_100 = freq_dist.most_common(100)

            print(s)
            freqDistsNames.append(s)
            print(freq_dist_top_100)

            pickle_out = open("C:/Users/Niall/Desktop/FYP/Output JSON Data/HTML/Pickle/"+ s + ".pickle","wb")
            pickle.dump(data, pickle_out)
            del pickle_out
            pickle_out.close()
            sourcesTags.append(data)

            print("\n")
            save_as_JSON(freq_dist_top_100, 'HTML/' + s +'_top_100.json')
            save_as_JSON(freq_dist,  'HTML/' + s + '_Frequency_Distribution.json')
            del pickle_out
            del test_deSer
    else:
        pickle_in = open(filename,"rb")
        word_tokens_pickle = pickle.load(pickle_in)

        freq_dist = FreqDist(word_tokens_pickle)
        freq_dist_top_100 = freq_dist.most_common(100)

        print(s + " Already processed")
        freqDistsNames.append(s)
        print(freq_dist_top_100)
        sourcesTags.append(word_tokens_pickle)

        print("\n")
        save_as_JSON(freq_dist_top_100, 'HTML/' + s +'_top_100.json')
        save_as_JSON(freq_dist,  'HTML/' + s + '_Frequency_Distribution.json')

        del pickle_in
        del word_tokens_pickle





SatireCorrect = 0
QuesionableCorrect = 0
ReliableCorrect = 0
index = 0
for st in sources:

    reliableTags = []
    quesionableTags = []
    satireTags = []

    index2 = 0
    for sss in sources:
        if sss in reliableSources and st != sss:
            reliableTags.append(sourcesTags[index2])
        elif sss in quesionableSources and st != sss:
            quesionableTags.append(sourcesTags[index2])
        elif sss in satireSources and st != sss:
            satireTags.append(sourcesTags[index2])
        index2 = index2 + 1

    overallSize = 0

    for size in reliableTags:
        overallSize = overallSize + sys.getsizeof(size)

    print(overallSize)
    reliableTags = ' '.join(map(str, reliableTags))
    quesionableTags = ' '.join(map(str, quesionableTags))
    satireTags = ' '.join(map(str, satireTags))

    print("\n" + sources[index])

    #st = ' '.join(map(str, st))

    thisSource = ' '.join(map(str, sourcesTags[index]))
    ReliableScore = Utilities.get_cosine_sim(reliableTags, thisSource)[1][0]
    QuesionableScore = Utilities.get_cosine_sim(quesionableTags, thisSource)[1][0]
    SatireScore = Utilities.get_cosine_sim(satireTags, thisSource)[1][0]

    print("Reliable:\t" + str(ReliableScore))

    print("Quesionable:\t"+ str(QuesionableScore))

    print("Satire:\t\t"+ str(SatireScore))

    if st in reliableSources and ReliableScore > QuesionableScore and ReliableScore > SatireScore:
        ReliableCorrect = ReliableCorrect + 1

    if st in quesionableSources and QuesionableScore > ReliableScore and QuesionableScore > SatireScore:
        QuesionableCorrect = QuesionableCorrect + 1

    if st in satireSources and SatireScore > QuesionableScore and SatireScore > ReliableScore:
        SatireCorrect = SatireCorrect + 1

    index = index + 1

    del thisSource
    del reliableTags
    del quesionableTags
    del satireTags


print("\nReliable score: " + str((ReliableCorrect / len(reliableSources))   *   100) + "%")
print("Quesionable score: " + str((QuesionableCorrect / len(quesionableSources))     *   100) + "%")
print("Satire score: " + str((SatireCorrect / len(satireSources))   *   100) + "%")
print("\nOverall score: " + str(((ReliableCorrect + QuesionableCorrect + SatireCorrect) / (len(sources)))   *   100) + "%")


print("\nFinito")
#filtered_sentence = []

#for w in word_tokens:
#    if w not in stopwords:
#        filtered_sentence.append(w)

#print(word_tokens)
#print(filtered_sentence)
