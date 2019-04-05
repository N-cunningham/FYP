from __future__ import division
import nltk
from nltk import FreqDist
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Utilities
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from numpy  import array


stopwords = set(stopwords.words('english'))
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]", "’", "|", "‘", "'", ".", " ", "e", "i", "a", "r", "."]# TODO Come back to investiagte use of punctuation marks
sources = Utilities.get_sources()
reliableSources = ["BBC", "CBS News", "CNBC", "NPR", "PBS", "Salon", "Slate", "The Atlantic", "The Daily Beast", "The Hill", "The Huffington Post", "The New York Times", "USA Today", "Vox", "Washington Examiner", "Media Matters for America", "The Fiscal Times", "AP", "Talking Points Memo"]
quesionable = ["Alternative Media Syndicate", "Bipartisan Report", "Breitbart", "CNS News", "Conservative Tribune", "Daily Mail", "Freedom Daily", "Liberty Writers", "Hang The Bankers", "Infowars", "Intellihub", "FrontPage Magazine", "Occupy Democrats", "Politicus USA", "Prntly","RedState", "The Duran", "The Gateway Pundit", "TruthFeed", "USA Politics Now", "End the Fed", "NODISINFO", "Freedom Outpost", "Waking Times", "NewsBusters", "Activist Post", "Drudge Report", "The D.C. Clothesline", "World News Politics", "Daily Buzz Live", "DC Gazette"]
allsources = reliableSources + quesionable
sourcesHeadings = ["reliable", "quesionable"]
sourceName = []
reliableScores = []
quesionableScores = []
distributions = []
classifications = []
differenceScores = []
months = listdir("F:/FYP/Data/JSON Data/")

#with open ("C:/Users/Niall/Desktop/FYP/Output JSON Data/list_of_sources", 'r') as s:
    #sources = json.load(s)

print(sources)

class Article:
    def __init__(self, month, dates):
        self.month = month
        self.dates = dates

class sourceNeighbourhood:
    def __init__(self, sourceName, neighbourhoods):
        self.sourceName = sourceName
        self.neighbourhoods = neighbourhoods

sourceNeighbourhoods = []

articles = []

for i in months:
    days = listdir("F:/FYP/Data/JSON Data/" + i)
    a1 = Article(i, days)
    articles.append(a1)

#sourceA = input("Type source ")
#sourceB = input("Type source B ")
topic = input("What is your topic to campair? ")
additional_stopords.append(topic)
part = input("What part of the text do you wish to compair (title/content)? ")

stopWord = ""

#while stopWord != "#no":
    #stopWord = input("Do you have any additional stop words to add in this case (type #no if not or to stop)? ")
    #additional_stopords.append(stopWord)

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

targetSourceData = []

for sources in sourceName:


    sourceData = []
    data = []
    for a in articles:
        file_exists = "true"
        for day in a.dates:
            try:
                article_headline = listdir("F:/FYP/Data/JSON Data/" + a.month + "/" + day + "/" + sources)
            except FileNotFoundError:
                #print("No artilces published by "+ s + " on " + day)
                file_exists = "false"

            if file_exists == "true":
                for headline in article_headline:
                    with open ("F:/FYP/Data/JSON Data/"+ a.month + "/" + day + "/" + sources + "/" + headline, 'rb') as f:
                        article_content = json.load(f)
                        if topic in article_content[part]:
                            data.append(article_content[part])


    data = ''.join(data)
    data = nltk.word_tokenize(data)
    neighbourhoods = []
    index = 0

    print(sources)


    for index in range(len(data)):
        #print(data[index] + " & " + topic)
        if data[index] == topic:

        #    try:
        #        if data[index - 4] not in stopwords and data[index - 4] not in additional_stopords:
        #            neighbourhoods.append(data[index - 4])
        #    except IndexError:
        #        print("Neighbourhood smaller than 4")

            try:
                if data[index - 3] not in stopwords and data[index - 3] not in additional_stopords:
                    neighbourhoods.append(data[index - 3])
            except IndexError:
               print("Neighbourhood smaller than 3")

            try:
                if data[index - 2] not in stopwords and data[index - 2] not in additional_stopords:
                    neighbourhoods.append(data[index - 2])
            except IndexError:
                print("Neighbourhood smaller than 2")

            try:
                if data[index - 1] not in stopwords and data[index - 1] not in additional_stopords:
                    neighbourhoods.append(data[index - 1])
            except IndexError:
                print("Neighbourhood smaller than 1")

            try:
                if data[index + 1] not in stopwords and data[index + 1] not in additional_stopords:
                    neighbourhoods.append(data[index + 1])
            except IndexError:
                print("Neighbourhood smaller than 1")

            try:
                if data[index + 2] not in stopwords and data[index + 2] not in additional_stopords:
                    neighbourhoods.append(data[index + 2])
            except IndexError:
                print("Neighbourhood smaller than 2")

            try:
                if data[index + 3] not in stopwords and data[index + 3] not in additional_stopords:
                    neighbourhoods.append(data[index + 3])
            except IndexError:
                print("Neighbourhood smaller than 3")

            #try:
            #    if data[index + 4] not in stopwords and data[index + 4] not in additional_stopords:
            #        neighbourhoods.append(data[index + 4])
            #except IndexError:
            #    print("Neighbourhood smaller than 4")

            index = index + 3

        index = index + 1


    neighbourhoods = ' '.join(neighbourhoods)
    sourceNeighbourhoodA = sourceNeighbourhood(sources, neighbourhoods)
    targetSourceData.append(sourceNeighbourhoodA)

docLen = 0
docCount = 0

for tsd in targetSourceData:
    docLen = docLen + len(tsd.neighbourhoods)
    docCount = docCount + 1


for s in sourceName:

    #for sNeigh in targetSourceData:
    for name in targetSourceData:
        if name.sourceName == s:
            targetSourceIndex = targetSourceData.index(name)

    #
    #RELIABLE SOURCE
    #

    reliableData = []
    for sNeigh in targetSourceData:
        if sNeigh.sourceName != s and sNeigh.sourceName in reliableSources:
            reliableData.append(sNeigh.neighbourhoods)


    reliableData = ''.join(reliableData)


    #
    #QUESTIONABLE SOURCE
    #


    quesionabledata = []
    for sNeigh in targetSourceData:
        if sNeigh.sourceName != s and sNeigh.sourceName in quesionable:
            quesionabledata.append(sNeigh.neighbourhoods)

    quesionabledata = ''.join(quesionabledata)

    index3 = 0;

    avgDocLen = ((len(reliableData) + len(quesionabledata))) / 2

    for s in sourceData:
        print('\n' + sourcesHeadings[index3])
        word_tokens = word_tokenize(s)
        freq_dist = FreqDist(word_tokens)
        freq_dist_top_25 = freq_dist.most_common(25)
        distributions.append(freq_dist_top_25)
        print(freq_dist_top_25)
        index3 = index3 + 1
        print("\n")

    print(s)
    print("\nTotal Reliable Simularity")
    scoreR = (Utilities.get_cosine_sim(targetSourceData[targetSourceIndex].neighbourhoods, reliableData)) #* (len(reliableData) / avgDocLen)
    reliableScores.append(scoreR)
    print(scoreR);

    print("\nTotal Quesionable Simularity")
    scoreQ = Utilities.get_cosine_sim(targetSourceData[targetSourceIndex].neighbourhoods, quesionabledata) #* (len(quesionabledata) / avgDocLen)
    quesionableScores.append(scoreQ)
    print(scoreQ);

    #print(sourceData[0])
    print("\n")
    print(str(len(targetSourceData[targetSourceIndex].neighbourhoods)) + " current source neighbourhoods")

    #print(sourceData[1])
    print(str(len(reliableData)) + " reliable neighbourhoods")

    #print(sourceData[2])
    print(str(len(quesionabledata)) + " unreliable neighbourhoods")
    print("\n")


index = len(reliableSources)

correct = 0
inncorrect = 0
reliableReliableScores = []
reliableQuesionableScores=[]
quesionableReliableScores=[]
quesionableQuesionableScores=[]

for index in range(len(reliableScores)):

    print("\n" + allsources[index])
    print("Reliable:"+ "\t" + str(reliableScores[index][1][0]))
    print("Quesionable:"+ "\t" + str(quesionableScores[index][1][0]))
    differenceScores.append( round((quesionableScores[index][1][0] - reliableScores[index][1][0]),5)   )

    if allsources[index] in reliableSources:
        print("Original:"+ "\t" + "Reliable" )
        if reliableScores[index][1][0] > quesionableScores[index][1][0]:
            correct = correct + 1
        elif  reliableScores[index][1][0] != 0 and 0 != quesionableScores[index][1][0]:
            inncorrect = inncorrect + 1
        reliableReliableScores.append(reliableScores[index][1][0])
        reliableQuesionableScores.append(quesionableScores[index][1][0])

    if allsources[index] in quesionable:
        print("Original:"+ "\t" + "Quesionable")
        if reliableScores[index][1][0] < quesionableScores[index][1][0]:
            correct = correct + 1
        elif  reliableScores[index][1][0] != 0 and 0 != quesionableScores[index][1][0]:
            inncorrect = inncorrect + 1
        quesionableReliableScores.append(reliableScores[index][1][0])
        quesionableQuesionableScores.append(quesionableScores[index][1][0])

    index = index + 1



total = correct  +inncorrect
print("\n" + "Reliable News Sources")
print("Reliable Score:"+ "\t\t" + str(reliableReliableScores))
print("Quesionable Score:"+ "\t" + str(reliableQuesionableScores)+"\n")
print("Quesionable News Sources")
print("Reliable Score:"+ "\t\t" + str(quesionableReliableScores))
print("Quesionable Score:"+ "\t" + str(quesionableQuesionableScores))


totalDiff = 0

for dev in differenceScores:
    totalDiff = totalDiff + abs(dev)

avgDiff = totalDiff / len(differenceScores)

print("\n")

if(avgDiff > .08):
    resp = (topic +" is a very high target of fake news\n")
    print(resp)

if(avgDiff < .08 and avgDiff > .0715):
    resp = (topic +" is a High target of fake news\n")
    print(resp)

if(avgDiff < .0715 and avgDiff > .054):
    resp = (topic +" is a Mid-range target of fake news\n")
    print(resp)

if(avgDiff < .054 and avgDiff > .046):
    resp = (topic +" is a Low target of fake news\n")
    print(resp)

if(avgDiff < .046):
    resp = (topic +" is a Very Low target of fake news\n")
    print(resp)

print("Average Neighbourhoods Cosine Simularity Deviation for " + topic + ": " + str(avgDiff) + "\n")

FNPER = round(  (((avgDiff-.08)/.08) *100),        2)
RNPER = round(  (((avgDiff-.046)/.046) *100),        2)

resp = ""

if(FNPER == abs(FNPER)):
    print("Increase from the topics that are the biggest targets of fake news:\t+" + str(FNPER)+"%")
else:
    print("Decrease from the topics that are the biggest targets of fake news:\t" + str(FNPER))


if(RNPER == abs(RNPER)):
    print("Increase from the topics that are the not targeted:\t\t\t+" + str(RNPER) +"%")
else:
    print("Decrease from the topics that are the not targeted:\t\t\t" + str(RNPER))




print("\n" + "CORRECT:"+"\t"+str(correct) + "\t" + str((correct/total) *100) + "%")
print("\n" + "INNCORRECT:"+"\t"+str(inncorrect) + "\t" + str((inncorrect/total) *100) + "%")
    #print(distributions[index])


plt.figure(1, figsize=(9, 3))

scoresToProcess = []
sourcesToProcess = []
finalIndex = 0


for z in differenceScores:

    if z != 0:

        sourcesToProcess.append(allsources[finalIndex])
        scoresToProcess.append(differenceScores[finalIndex])

    finalIndex = finalIndex + 1


x = sourcesToProcess
y = scoresToProcess

graph_data = pd.DataFrame(
    {'name': x,
     'scores': y
    })

graph_data.sort_values(by=['scores'], inplace=True)

plt.barh(range(len(graph_data['name'])), graph_data['scores'], color="blue")
plt.yticks(range(len(graph_data['name'])), graph_data['name'])
plt.title(resp)
plt.xlabel('Cosine Deviations')
plt.ylabel('')
#plt.show()
#plt.savefig(os.path.join('test.png'), dpi=300, format='png', bbox_inches='tight')

i = 0

plt.show()
