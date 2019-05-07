from InstagramAPI import InstagramAPI
import praw
import requests
import urllib.request
import time
import keyboard
from PIL import Image
import math

#put it IG username/password
api = InstagramAPI("username", "password")
api.login()


#make a reddit acount and look up how to find this stuff. its called PRAW
reddit = praw.Reddit(client_id='', 
	client_secret='', 
	username='', 
	password='', 
	user_agent='chrome')


def DLimage(url, filePath, fileName):
	fullPath = filePath + fileName + '.jpg'
	urllib.request.urlretrieve(url, fullPath)


#folder path to store downloaded images
filePath = ""

subreddit = reddit.subreddit('dankmemes') #subreddit to take images from

#tags for IG post
captionTags = ""

#caption text for IG
captionText = "These images are from reddit."

waitTime = 2 #to prevent reddit badgateway error. DONt change

numRounds = 100 #how many posts

postFrequency = 4000 # how often to post in seconds. 

numPics = 10 #how many pics per post. 2-10

for x in range(numRounds):
	new_memes = subreddit.rising(limit=numPics) #.hot/.rising/.new   reddit sorting algorithm
	authors = []
	photoAlbum = []
	print("Round/post number:", x)
	for subbmission in new_memes:
		if subbmission.is_self == True: #checking if post is only text.
			print("Post was text, skipping to next post.")
			continue
		else:
			pass
		url = subbmission.url
		time.sleep(waitTime)
		fileName = str(subbmission)
		fullPath = filePath + fileName + '.jpg'
		#print(fullPath)
		time.sleep(waitTime)
		#print(url)
		try:
			DLimage(url, filePath, fileName)
		except:
			print("scratch that, next post.")
			continue
		time.sleep(waitTime)
		author = str(subbmission.author)
		authors.append(author)
		time.sleep(waitTime)
		img = Image.open(fullPath)
		width, height = img.size
		img = img.resize((1000, 1020), Image.NEAREST) #image resize. width/height
		img = img.convert("RGB")
		img.save(fullPath)
		photoAlbum.append({ 
				'type': 'photo', 
				'file': fullPath,
			})

	authors = ''.join(str(e + ', ') for e in authors)
	print(photoAlbum)
	api.uploadAlbum(photoAlbum, caption=(captionText + '\n' + 'Created by redditors: ' + authors[0:(len(authors)-2)] + '.' + '\n' + captionTags))
	time.sleep(postFrequency)
