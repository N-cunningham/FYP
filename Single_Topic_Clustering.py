import nltk
from nltk import FreqDist
import json
from os import listdir
from Utilities import save_as_JSON#
from sklearn.cluster import KMeans
import numpy as np
from Utilities import get_sources
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

sources = get_sources()
topic = "Trump"
topics = []
labels = np.array(sources)

for source in sources:

    with open ("C:/Users/Niall/Desktop/FYP/Output JSON Data/Linguistic/" + source + "_Frequency_Distribution.json", 'rb') as file:

        JSON_Data = json.load(file)

        try:
            Topic_freq = []
            #Topic_freq.append(source)
            Topic_freq.append(JSON_Data[topic])


        except KeyError:
            print("y0 n0 "+ topic +" reported by " + source)
            Topic_freq = []
            #Topic_freq.append(source)
            Topic_freq.append(0)

    topics.append(Topic_freq)

#for t in trumps:
#    print(t)


X = np.array(topics)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
i = 0
while i in range(len(sources)):
    print(str(kmeans.labels_[i]) + " " + str(sources[i]))
    i += 1

print(kmeans.cluster_centers_)
