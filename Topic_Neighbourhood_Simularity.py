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
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]", "’", "|", "‘", "'", ".", " ", "e", "i", "a", "r", "."]# TODO Come back to investiagte use of punctuation marks
sources = Utilities.get_sources()
reliableSources = ["BBC", "CBS News", "CNBC", "CNBC", "NPR", "PBS", "Salon", "Slate", "The Atlantic", "The Daily Beast", "The Hill", "The Huffington Post", "The New York Times", "USA Today", "Vox", "Washington Examiner", "Media Matters for America", "The Fiscal Times", "AP", "Talking Points Memo"]
quesionable = ["Alternative Media Syndicate", "Bipartisan Report", "Breitbart", "CNS News", "Conservative Tribune", "Daily Mail", "Freedom Daily", "Liberty Writers", "Hang The Bankers", "Infowars", "Intellihub", "FrontPage Magazine", "Occupy Democrats", "Politicus USA", "Prntly","RedState", "The Duran", "The Gateway Pundit", "TruthFeed", "USA Politics Now", "End the Fed", "NODISINFO", "Freedom Outpost", "Waking Times", "NewsBusters", "Activist Post", "Drudge Report", "The D.C. Clothesline", "World News Politics", "Daily Buzz Live", "DC Gazette"]
allsources = reliableSources + quesionable
sourcesHeadings = ["reliable", "quesionable"]
sourceName = []
reliableScores = []
quesionableScores = []
distributions = []
classifications = []
targetSourceData = []
months = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/")

#with open ("C:/Users/Niall/Desktop/FYP/Output JSON Data/list_of_sources", 'r') as s:
    #sources = json.load(s)

print(sources)

class Article:
    def __init__(self, month, dates):
        self.month = month
        self.dates = dates

articles = []

for i in months:
    days = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + i)
    a1 = Article(i, days)
    articles.append(a1)

#sourceA = input("Type source ")
#sourceB = input("Type source B ")
topic = input("What is your topic to campair? ")
additional_stopords.append(topic)
part = input("What part of the text do you wish to compair (title/content)? ")

stopWord = ""

while stopWord != "#no":
    stopWord = input("Do you have any additional stop words to add in this case (type #no if not or to stop)? ")
    additional_stopords.append(stopWord)

#print(sourceA)
#print(sourceB)
print(topic)
print(part)
print("Running...")

#sourceName.append(sourceA)
#sourcesHeadings.append(sourceA)
#sourceName.append(sourceB)

#
#SOURCE
#
for sourceR in reliableSources:
    sourceName.append(sourceR)

for sourceQ in quesionable:
    sourceName.append(sourceQ)

for s in sourceName:

    sourceData = []
    data = []
    for a in articles:
        file_exists = "true"
        for day in a.dates:
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                #print("No artilces published by "+ s + " on " + day)
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

            if data[index - 3] not in stopwords and data[index - 3] not in additional_stopords:
                neighbourhoods.append(data[index - 3])

            if data[index - 2] not in stopwords and data[index - 2] not in additional_stopords:
                neighbourhoods.append(data[index - 2])

            if data[index - 1] not in stopwords and data[index - 1] not in additional_stopords:
                neighbourhoods.append(data[index - 1])

            if data[index + 1] not in stopwords and data[index + 1] not in additional_stopords:
                neighbourhoods.append(data[index + 1])

            if data[index + 2] not in stopwords and data[index + 2] not in additional_stopords:
                neighbourhoods.append(data[index + 2])

            if data[index + 3] not in stopwords and data[index + 3] not in additional_stopords:
                neighbourhoods.append(data[index + 3])

            index = index + 3

        index = index + 1

    neighbourhoods = ' '.join(neighbourhoods)
    targetSourceData.append(neighbourhoods)



    #
    #RELIABLE SOURCE
    #


    reliableData = []
    for sr in reliableSources:
        if sr != s:
            for a in articles:
                file_exists = "true"
                for day in a.dates:
                    try:
                        article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + sr)
                    except FileNotFoundError:
                        #print("No artilces published by "+ s + " on " + day)
                        file_exists = "false"

                    if file_exists == "true":
                        for headline in article_headline:
                            with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + sr + "/" + headline, 'rb') as f:
                                article_content = json.load(f)
                                if topic in article_content[part]:
                                    reliableData.append(article_content[part])
            #print(len(reliableData))


    reliableData = ''.join(reliableData)
    reliableData = nltk.word_tokenize(reliableData)
    reliableNeighbourhoods = []
    index = 0


    print("\n\n\nANALYSING NEIGHBOURHOODS\n\n\n")

    for index in range(len(reliableData)):
        #print(data[index] + " & " + topic)
        if reliableData[index] == topic:

            if reliableData[index - 3] not in stopwords and reliableData[index - 3] not in additional_stopords:
                reliableNeighbourhoods.append(reliableData[index - 3])

            if reliableData[index - 2] not in stopwords and reliableData[index - 2] not in additional_stopords:
                reliableNeighbourhoods.append(reliableData[index - 2])

            if reliableData[index - 1] not in stopwords and reliableData[index - 1] not in additional_stopords:
                reliableNeighbourhoods.append(reliableData[index - 1])

            if reliableData[index + 1] not in stopwords and reliableData[index + 1] not in additional_stopords:
                reliableNeighbourhoods.append(reliableData[index + 1])

            if reliableData[index + 2] not in stopwords and reliableData[index + 2] not in additional_stopords:
                reliableNeighbourhoods.append(reliableData[index + 2])

            if reliableData[index + 3] not in stopwords and reliableData[index + 3] not in additional_stopords:
                reliableNeighbourhoods.append(reliableData[index + 3])

            index = index + 3

        index = index + 1

    reliableNeighbourhoods = ' '.join(reliableNeighbourhoods)
    sourceData.append(reliableNeighbourhoods)



    #
    #QUESTIONABLE SOURCE
    #


    quesionabledata = []
    for sq in quesionable:
        if sq != s:
            for a in articles:
                file_exists = "true"
                for day in a.dates:
                    try:
                        article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + sq)
                    except FileNotFoundError:
                        #print("No artilces published by "+ s + " on " + day)
                        file_exists = "false"

                    if file_exists == "true":
                        for headline in article_headline:
                            with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + sq + "/" + headline, 'rb') as f:
                                article_content = json.load(f)
                                if topic in article_content[part]:
                                    quesionabledata.append(article_content[part])
            #print(len(quesionabledata))


    quesionabledata = ''.join(quesionabledata)
    quesionabledata = nltk.word_tokenize(quesionabledata)
    quesionableNeighbourhoods = []
    index = 0


    print("\n\n\nANALYSING NEIGHBOURHOODS\n\n\n")

    for index in range(len(quesionabledata)):
            #print(data[index] + " & " + topic)
        if quesionabledata[index] == topic:

            if quesionabledata[index - 3] not in stopwords and quesionabledata[index - 3] not in additional_stopords:
                quesionableNeighbourhoods.append(quesionabledata[index - 3])

            if quesionabledata[index - 2] not in stopwords and quesionabledata[index - 2] not in additional_stopords:
                quesionableNeighbourhoods.append(quesionabledata[index - 2])

            if quesionabledata[index - 1] not in stopwords and quesionabledata[index - 1] not in additional_stopords:
                quesionableNeighbourhoods.append(quesionabledata[index - 1])

            if quesionabledata[index + 1] not in stopwords and quesionabledata[index + 1] not in additional_stopords:
                quesionableNeighbourhoods.append(quesionabledata[index + 1])

            if quesionabledata[index + 2] not in stopwords and quesionabledata[index + 2] not in additional_stopords:
                quesionableNeighbourhoods.append(quesionabledata[index + 2])

            if quesionabledata[index + 3] not in stopwords and quesionabledata[index + 3] not in additional_stopords:
                quesionableNeighbourhoods.append(quesionabledata[index + 3])

            index = index + 3

        index = index + 1

    quesionableNeighbourhoods = ' '.join(quesionableNeighbourhoods)
    sourceData.append(quesionableNeighbourhoods)


    index3 = 0;
    print(s)
    for s in sourceData:
        print('\n' + sourcesHeadings[index3])
        word_tokens = word_tokenize(s)
        freq_dist = FreqDist(word_tokens)
        freq_dist_top_25 = freq_dist.most_common(25)
        distributions.append(freq_dist_top_25)
        print(freq_dist_top_25)
        index3 = index3 + 1
        print("\n")


    print("\nTotal Reliable Simularity")
    scoreR = Utilities.get_cosine_sim(targetSourceData[0], sourceData[0])
    reliableScores.append(scoreR)
    print(scoreR);

    print("\nTotal Quesionable Simularity")
    scoreQ = Utilities.get_cosine_sim(targetSourceData[0], sourceData[1])
    reliableScores.append(scoreQ)
    print(scoreQ);

    #print(sourceData[0])
    print(len(targetSourceData[0]))
    print("\n")

    #print(sourceData[1])
    print(str(len(sourceData[0])) + " reliable neighbourhoods")
    print("\n")

    #print(sourceData[2])
    print(str(len(sourceData[1])) + " unreliable neighbourhoods")
    print("\n")


index = 0

for index in range(len(reliableScores)):

    print(allsources[index] + "s Results:")
    print("reliable:" + str(reliableScores[index]))
    print("quesionable:" + str(quesionableScores[index]))

    if allsources[index] in reliableSources:
        print("Original clasification: reliable" )

    if allsources[index] in quesionable:
        print("Original clasification: quesionable" )

    print(distributions[index])

    index = index + 1

    print("\n")
