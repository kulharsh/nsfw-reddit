'''
A script to retrieve all reddit top level comments from db. 
Follows up by splitting randomly into training and validation set.
'''
import pymongo
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

break_at = 1000000
def getRedditData():
  connection = pymongo.MongoClient("mongodb://localhost")  
  db=connection.joke
  record1 = db.joke_collection
  sents = []
  nsfws = []
  count = 0;
  countnsfw = 0
  countsfw = -1
  for x in record1.find({},{ "title": 1, "selftext": 2, "over_18":3 }):
    if not 'selftext' in x:
      continue
    sent = x['title'] + ' '+x['selftext']
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(sent)
    filtered_sentence = ''
    for w in word_tokens:
      if not w in stop_words:
        filtered_sentence = filtered_sentence + ' ' + w
    count = count + 1;
    if count > break_at :
      break
    if count % 10000 == 0:
      print('Processed : '+str(count))
    
    if x['over_18'] == True:
        nsfw = 1
        countnsfw = countnsfw + 1
        nsfws.append(nsfw)
        sents.append(filtered_sentence.strip())
    else:
        nsfw = 0
        if countsfw < countnsfw : 
          countsfw = countsfw + 1
          nsfws.append(nsfw)
          sents.append(filtered_sentence.strip())    
  return train_test_split(sents, nsfws, test_size=0.33, random_state=42)

if __name__=="__main__":
  X_train, X_test, y_train, y_test = getRedditData()
  print(len(X_train))
  print(len(y_train))
