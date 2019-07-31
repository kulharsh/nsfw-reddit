'''
A script to download content from a specific subreddit. 
Loops multiple times to get older and older content with the before option in the pushshift api. Sleep is added so as
not to overwhelm the pushshift servers. 
Saves the downloaded json in mongo for further use. 
'''
import requests 
import json
import pymongo
from datetime import datetime
import time
#now = time.time()

connection = pymongo.MongoClient("mongodb://localhost")  
db=connection.joke
record1 = db.joke_collection

# api-endpoint 
#print(type(now))
#print(now)
#last = int(now - 100);
last = '1549537111'
i = 0
URL = "https://api.pushshift.io/reddit/search/submission/"
while i < 1000 :  
	print(last)
	# defining a params dict for the parameters to be sent to the API 
	PARAMS = {'subreddit':'jokes', 'sort':'desc', 'sort_type':'created_utc', 'size':'1000', 'before':last} 
	  
	# sending get request and saving the response as response object 
	r = requests.get(url = URL, params = PARAMS) 
	  
	# extracting data in json format 
	your_data = r.json()

	jokes = your_data['data']
	for joke in jokes:
		print("Adding...")
		last = joke["created_utc"]
		record1.insert(joke)
	i = i + 1
	time.sleep(10)
