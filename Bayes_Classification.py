import numpy as np
import csv

attribute = []
targetAttribute = []
#y = np.array([1, 2, 3, 4, 5, 6])
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
#clf = MultinomialNB()
#clf.fit(X, y)
#print(X)
#print(clf.predict(X[2:3]))



with open('C:/Users/Niall_cunningham/Desktop/train.tsv', encoding="utf8") as tsvIn:#, open('new.csv', 'wb') as csvout:

    tsvIn = csv.reader(tsvIn, delimiter='\t')
    falsetext = "FALSE"
    truetext = "TRUE"
    index = 0

    for row in tsvIn:

        if index == 0:
            falsetext = row[1]

        if index == 5:
            truetext = row[1]

        if row[1] == falsetext or row[1] ==  "pants-fire" or row[1] == truetext or row[1] == "mostly-true":
            attribute.append(row[2])
            targetAttribute.append(row[1])
            print(row[1] + ":   " + row[2])

        index = index + 1


clf = MultinomialNB()

vectorizer = CountVectorizer(attribute)
attributeVectorizer = vectorizer.fit(attribute)

columnNames = ["label", "text"]
arra = np.asarray(targetAttribute)
np.reshape(arra, (1, -1))
clf.fit(attribute, targetAttribute)

testAttribute = []
testTargetAttribute = []

with open('C:/Users/Niall_cunningham/Desktop/test.tsv', encoding="utf8") as tsvTestIn:#, open('new.csv', 'wb') as csvout:

    tsvTestIn = csv.reader(tsvTestIn, delimiter='\t')

    print("\n\nTEST DATA\n\n")
    for row in tsvTestIn:
        if row[1] == falsetext or row[1] ==  "pants-fire" or row[1] == truetext or row[1] == "mostly-true":
            testAttribute.append(row[2])
            testTargetAttribute.append(row[1])
            print(row[1] + ":   " + row[2])

print("\n" + str(len(targetAttribute)) + " Training cases")
print(str(len(testTargetAttribute)) + " Test cases")
