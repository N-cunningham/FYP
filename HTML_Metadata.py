import sklearn
import nltk
from nltk import FreqDist
#from nltk.book import *
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords = set(stopwords.words('english'))
source = "The New York Times"
date = "2017-04-19"
month = "April"
files = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + month + "/" + date + "/" + source)

NYT_APR_19 = []
data = []
i = 0
#print(files)
for files[i] in files:
    i += 1
    with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + month + "/" + date + "/" + source + "/" + files[0], 'rb') as f:
        NYT =json.load(f)
        data.append(NYT['html'])

all_NYT_data = ' '.join(data)
#print(all_NYT_data)
word_tokens = word_tokenize(all_NYT_data)

#print(word_tokens[52][1])

tags = []

for w in word_tokens:
    if len(w) > 1 and w[0] == "/" and w[1] != "/":
        tags.append(w)

#print (tags)
freq_dist = FreqDist(tags)
print(freq_dist.most_common(25))
print(freq_dist)

#filtered_sentence = []

#for w in word_tokens:
#    if w not in stopwords:
#        filtered_sentence.append(w)

#print(word_tokens)

#print(filtered_sentence)
