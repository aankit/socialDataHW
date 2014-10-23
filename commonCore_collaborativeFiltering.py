#!/usr/bin/env python
import nltk 
nltk.data.path.append('./nltk_data/') #this may need to change depending on when
from nltk.corpus import stopwords
import queryTwitter, tweetEasy, re, string
import numpy as np
import numpy.linalg as LA


#twitter query search parameters
q = '"common core"'
c = 100
num_iterations = 1
#list of words to scrub
scrubList = stopwords.words('english')
scrubList.append('rt')

#functions, they do work for us :-<
def scrub(word):
	word = word.strip()
	linkPattern = re.compile('http')
	if len(word)>0:
		if word not in scrubList and word[0] != '@' and word[0] != '#' and not linkPattern.match(word):
			return True
		else:
			return False
	else:
		return False

def dictofwords(d):
	newDict = {}
	for user, tweets in d.items():
		for tweet in tweets:
			tweet = tweet.strip()
			words = tweet.split(" ")
			for word in words:
				word = word.encode('ascii', 'ignore')
				word = word.lower()
				word = word.translate(string.maketrans("",""), string.punctuation)
				if scrub(word):
					if user not in newDict:
						newDict[user] = [word]
					else:
						newDict[user].append(word)
	return newDict

def addToSet(d, s):
	for l in d.values():
		for i in l:
			if type(i) is not list:
				s.add(i)

def addToDict(d1, d2):
	for k, v in d1.items():
		if type(v) is list:
			for i in v:
				curr_index = allWords.index(i)
				d2[k][curr_index] += 1
		else:
			curr_index = allWords.index(v)
			d2[k][curr_index] += 1


#run search/tweets request
commonCore = queryTwitter.SearchTwitter(q, c, num_iterations)
statuses = commonCore.runQuery()
#put the results from the query into a parser object
search = tweetEasy.ParseSearch(statuses)

#get info about users usage of hashtags, words in tweets, and words for their description
hashtags = search.getDict('screen_name', 'hashtags')
tweets = search.getDict('screen_name', 'tweetText')
descriptions = search.getDict('screen_name', 'description')
user_mentions = search.getDict('screen_name', 'user_mentions')

#make a list of all the words that the user uses, scrubbing out the stopwords, links, hashtags, and user mentions
tweetWords = dictofwords(tweets)
descriptionWords = dictofwords(descriptions)

#create a set of all words
allWords = set()
addToSet(tweetWords, allWords)
addToSet(descriptionWords, allWords)
addToSet(hashtags, allWords)
allWords = list(allWords)
#create a set of all users
allUsers = list(set(tweets.keys()))

users_to_words = {}
for u in allUsers:
    users_to_words[u]=[0]*len(allWords)

addToDict(tweetWords, users_to_words)
addToDict(descriptionWords, users_to_words)
addToDict(hashtags, users_to_words)

def cx(a, b):
	try:
		divisor = LA.norm(a)*LA.norm(b)
		print divisor
	except:
		return 0
	return round(np.inner(a, b)/(divisor), 3)

scoreDict={}
for user in allUsers:
	scores=[]
	for k, v, in users_to_words.items():
		if k!=user:
			scores.append((cx(users_to_words[user], v), k))
	scoreDict[user] = scores


for k, v in scoreDict.items():
	print k , max(v)





