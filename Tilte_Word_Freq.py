import nltk
from nltk import FreqDist
import json
from os import listdir
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Utilities import get_sources
from Utilities import get_nouns
from Utilities import save_as_JSON

stopwords = set(stopwords.words('english'))
#raw_sources = get_sources()
sources = get_sources()
#offset = 11

#while offset < len(raw_sources):
    #sources.append(raw_sources[offset])
    #offset += 1

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


#print(files)
for s in sources:
    data = []
    for a in articles:
        file_exists = "true"
        for day in a.dates:
            try:
                article_headline = listdir("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s)
            except FileNotFoundError:
                print("No artilces published by "+ s + " on " + day)
                file_exists = "false"

            if file_exists == "true":
                for headline in article_headline:
                    with open ("C:/Users/Niall/Desktop/FYP/JSON Data/" + a.month + "/" + day + "/" + s + "/" + headline, 'rb') as f:
                        article_content = json.load(f)
                        data.append(article_content['title'])


    all_news_source_data = ' '.join(data)
    word_tokens = word_tokenize(all_news_source_data)

    filtered_titles = []
    additional_stopords = [":", "'", "'s", "The", "-", "?", ",", '"', '”', '“', "'", "'", "'", "'", "$", ")", "(", "_", "&", '...', '.', '�', ';', '!']# TODO Come back to investiagte use of punctuation marks

    nouns = get_nouns(word_tokens)

    for w in nouns:
        if w not in stopwords and w not in additional_stopords:
            filtered_titles.append(w)

    freq_dist = FreqDist(filtered_titles)
    freq_dist_top_100 = freq_dist.most_common(100)

    #print(freq_dist_top_100)
    #print(freq_dist)

    save_as_JSON(freq_dist_top_100,  s + 'Linguistic/_top_100.json')
    save_as_JSON(freq_dist,  s + 'Linguistic/_Frequency_Distribution.json')


    #freq_dist.plot(20, title = s + " Distribution of top 20 title words across all data")

print("Fin")
