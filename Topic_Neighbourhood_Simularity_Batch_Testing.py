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


stopwords = set(stopwords.words('english'))
additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!', "''", "``", "%", "@", "--", ".", "[", "]", "[]", "[ ]", "’", "|", "‘", "'", ".", " ", "e", "i", "a", "r", "."]# TODO Come back to investiagte use of punctuation marks
sources = Utilities.get_sources()
reliableSources = ["BBC", "CBS News", "CNBC", "NPR", "PBS", "Salon", "Slate", "The Atlantic", "The Daily Beast", "The Hill", "The Huffington Post", "The New York Times", "USA Today", "Vox", "Washington Examiner", "Media Matters for America", "The Fiscal Times", "AP", "Talking Points Memo"]
quesionable = ["Alternative Media Syndicate", "Bipartisan Report", "Breitbart", "CNS News", "Conservative Tribune", "Daily Mail", "Freedom Daily", "Liberty Writers", "Hang The Bankers", "Infowars", "Intellihub", "FrontPage Magazine", "Occupy Democrats", "Politicus USA", "Prntly","RedState", "The Duran", "The Gateway Pundit", "TruthFeed", "USA Politics Now", "End the Fed", "NODISINFO", "Freedom Outpost", "Waking Times", "NewsBusters", "Activist Post", "Drudge Report", "The D.C. Clothesline", "World News Politics", "Daily Buzz Live", "DC Gazette"]
allsources = reliableSources + quesionable
sourcesHeadings = ["reliable", "quesionable"]
distributions = []
classifications = []
months = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/")

#with open ("C:/Users/Niall/Desktop/FYP/Output JSON Data/list_of_sources", 'r') as s:
    #sources = json.load(s)

print(sources)

class Article:
    def __init__(self, month, dates):
        self.month = month
        self.dates = dates

class sourceNeighbourhood:
    def __init__(self, allsources, neighbourhoods):
        self.allsources = allsources
        self.neighbourhoods = neighbourhoods

sourceNeighbourhoods = []

articles = []

for i in months:
    days = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + i)
    a1 = Article(i, days)
    articles.append(a1)

#sourceA = input("Type source ")
#sourceB = input("Type source B ")
#topic = input("What is your topic to campair? ")
#additional_stopords.append(topic)
part = input("What part of the text do you wish to compair (title/content)? ")

topics = ["Trump","CNN", "NYT", "Russia", "Obama", "Election",  "Hillary", "Breitbart", "Comey", "Acosta"]#, "FBI", "Manson", "police", "Vegas", "NFL", "CIA", "Morgue", "WikiLeaks", "Army", "MI5", "Texas Church Shooting", "Sharia", "Kapernick", "ISIS", "Hurricane", "Bitcoin",  "Vegas", "Korea", "Eclipse", "Manchester", "Giraffe"]

stopWord = ""

while stopWord != "#no":
    stopWord = input("Do you have any additional stop words to add in this case (type #no if not or to stop)? ")
    additional_stopords.append(stopWord)

#print(sourceA)
#print(sourceB)

correctPercentages = []
inncorrectPercentages = []
diviations = []
allsources = []

for sourceR in reliableSources:
    allsources.append(sourceR)

for sourceQ in quesionable:
    allsources.append(sourceQ)

for topic in topics:

    noTopicSources = 0
    reliableScores = []
    quesionableScores = []

    print("\n\nNew Topic " + topic)
    print(part)
    print("\nRunning...")

    #allsources.append(sourceA)
    #sourcesHeadings.append(sourceA)
    #allsources.append(sourceB)

    #
    #SOURCE
    #


    targetSourceData = []

    for sources in allsources:

        reliableScores = []
        quesionableScores = []
        sourceData = []
        data = []
        for a in articles:
            file_exists = "true"
            for day in a.dates:
                try:
                    article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + sources)
                except FileNotFoundError:
                    #print("No artilces published by "+ s + " on " + day)
                    file_exists = "false"

                if file_exists == "true":
                    for headline in article_headline:
                        with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + sources + "/" + headline, 'rb') as f:
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


    for s in allsources:

        #for sNeigh in targetSourceData:
        for name in targetSourceData:
            if name.allsources == s:
                targetSourceIndex = targetSourceData.index(name)

        #
        #RELIABLE SOURCE
        #

        reliableData = []
        for sNeigh in targetSourceData:
            if sNeigh.allsources != s and sNeigh.allsources in reliableSources:
                reliableData.append(sNeigh.neighbourhoods)


        reliableData = ' '.join(reliableData)


        #
        #QUESTIONABLE SOURCE
        #


        quesionabledata = []
        for sNeigh in targetSourceData:
            if sNeigh.allsources != s and sNeigh.allsources in quesionable:
                quesionabledata.append(sNeigh.neighbourhoods)

        quesionabledata = ' '.join(quesionabledata)

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

        #print(s)
        #print("\nTotal Reliable Simularity")
        try:
            scoreR = (Utilities.get_cosine_sim(targetSourceData[targetSourceIndex].neighbourhoods, reliableData)) #* (len(reliableData) / avgDocLen)
            reliableScores.append(scoreR)
        except ValueError:
            print("No occurences of " + topic + " in "+ s )
            noTopicSources = noTopicSources + 1

        #print(scoreR);
        #print("\nTotal Quesionable Simularity")

        try:
            scoreQ = Utilities.get_cosine_sim(targetSourceData[targetSourceIndex].neighbourhoods, quesionabledata) #* (len(quesionabledata) / avgDocLen)
            quesionableScores.append(scoreQ)
        except ValueError:
            print("No occurences of " + topic + " in "+ s )

        #print(scoreQ);

        #print(sourceData[0])
        #print("\n")
        #print(str(len(targetSourceData[targetSourceIndex].neighbourhoods)) + " current source neighbourhoods")

        #print(sourceData[1])
        #print(str(len(reliableData)) + " reliable neighbourhoods")

        #print(sourceData[2])
        #print(str(len(quesionabledata)) + " unreliable neighbourhoods")
        #print("\n")


    index = len(reliableSources)

    correct = 0
    inncorrect = 0
    reliableReliableScores = []
    reliableQuesionableScores=[]
    quesionableReliableScores=[]
    quesionableQuesionableScores=[]
    differneces = []


    for index in range(len(reliableScores)):

        #print("\n" + allsources[index])
        #print("Reliable:"+ "\t" + str(reliableScores[index][1][0]))
        #print("Quesionable:"+ "\t" + str(quesionableScores[index][1][0]))

        differnece = abs(reliableScores[index][1][0] - quesionableScores[index][1][0])
        differneces.append(differnece)

        if allsources[index] in reliableSources:
        #    print("Original:"+ "\t" + "Reliable" )
            if reliableScores[index][1][0] > quesionableScores[index][1][0]:
                correct = correct + 1
            elif  reliableScores[index][1][0] != 0 and 0 != quesionableScores[index][1][0]:
                inncorrect = inncorrect + 1
            reliableReliableScores.append(reliableScores[index][1][0])
            reliableQuesionableScores.append(quesionableScores[index][1][0])

        if allsources[index] in quesionable:
        #    print("Original:"+ "\t" + "Quesionable")
            if reliableScores[index][1][0] < quesionableScores[index][1][0]:
                correct = correct + 1
            elif  reliableScores[index][1][0] != 0 and 0 != quesionableScores[index][1][0]:
                inncorrect = inncorrect + 1
            quesionableReliableScores.append(reliableScores[index][1][0])
            quesionableQuesionableScores.append(quesionableScores[index][1][0])

        index = index + 1


    total = correct + inncorrect
    print("\n" + "Reliable News Sources")
    print("Reliable Score:"+ "\t\t" + str(reliableReliableScores))
    print("Quesionable Score:"+ "\t" + str(reliableQuesionableScores)+"\n")
    print("Quesionable News Sources")
    print("Reliable Score:"+ "\t\t" + str(quesionableReliableScores))
    print("Quesionable Score:"+ "\t" + str(quesionableQuesionableScores))

    total_differnces = 0;
    for diff in differneces:
        total_differnces = total_differnces + diff

    correctPercentage = (correct/total) *100
    correctPercentages.append(correctPercentage)

    inncorrectPercentage = (inncorrect/total) *100
    inncorrectPercentages.append(inncorrectPercentage)

    diviation = total_differnces/total
    diviations.append(diviation)

    correctString = ("\n" + "CORRECT:"+"\t"+str(correct) + "\t" + str(correctPercentage) + "%")
    inncorrectString = ("\n" + "INNCORRECT:"+"\t"+str(inncorrect) + "\t" + str(inncorrectPercentage) + "%")
    diviationString = ("\n" + "Average Diviation: " + str(diviation))

    print(correctString)
    print(inncorrectString)
    print(diviationString)

    outputString = correctString + " " + inncorrectString + " " + diviationString

    Utilities.save_as_JSON( outputString , 'Results/'+ topic +'_Results.txt')


correctPercentagesTotal = 0
inncorrectPercentagesTotal = 0
diviationsTotal = 0

for cp in correctPercentages:
    correctPercentagesTotal = correctPercentagesTotal + cp

for ip in inncorrectPercentages:
    inncorrectPercentagesTotal = inncorrectPercentagesTotal + ip

for dt in diviations:
    diviationsTotal = diviationsTotal + dt

print("Correct Average: " + str(correctPercentagesTotal / len(topics)) )
print(correctPercentages)

print("\nInncorrect Average: " + str(inncorrectPercentagesTotal / len(topics)))
print(inncorrectPercentages)

print("\nDiviation Average: " + str(diviationsTotal / len(topics)))
print(diviations)


    #print(distributions[index])
