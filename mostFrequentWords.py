'''
A script to retrieve all reddit top level comments. 
It also follows it up by fitting a CountVectorizer on the text to determine the most frequent words used in nsfw (over_18) posts
'''
import pymongo
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

connection = pymongo.MongoClient("mongodb://localhost")  
db=connection.joke
record1 = db.joke_collection
nsfw_words = [];
sents = []
for x in record1.find({},{ "title": 1, "selftext": 2, "over_18":3 }):
  #print(x)
  if not 'selftext' in x:
  	continue
  if x['over_18'] == True:
  		sent = x['title'] + ' '+x['selftext']
  		stop_words = set(stopwords.words('english')) 
  		word_tokens = word_tokenize(sent) 
  		filtered = [w for w in word_tokens if not w in stop_words]
  		filtered_sentence = ''
  		for w in filtered:
  			filtered_sentence = w + ' '
  		sents.append(filtered_sentence.strip())
  		#print(sent)
print(sents)
vec = CountVectorizer().fit(sents)
bag_of_words = vec.transform(sents)
sum_words = bag_of_words.sum(axis=0) 
words_freq = [(word, sum_words[0, idx]) for word, idx in     vec.vocabulary_.items()]
words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
print(words_freq[:20])