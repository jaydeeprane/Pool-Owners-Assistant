import tweepy
import re
import nltk
from time import sleep
import datetime
from tweepy.streaming import StreamListener
from collections import Counter
from tweepy import OAuthHandler, Stream
import urllib2
import json
import csv


# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)

# Verifyng the current location of the device
# print(location)

# Output:
# {u'city': u'Raleigh', u'region_code': u'NC', u'region_name': u'North Carolina', u'ip': u'152.7.224.5', 
# u'time_zone': u'America/New_York', u'longitude': -78.7239, u'metro_code': 560, u'latitude': 35.7463, u'country_code': u'US', 
# u'country_name': u'United States', u'zip_code': u'27606'}

# location_longitude = location['longitude']
# location_latitude = location['latitude']



# Uncomment this and refer to access_tokens file for these tokens
# consumer_key = 
# consumer_secret = 
# access_token = 
# access_secret = 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

# Open/Create a file to append data
csvFile = open('tweets1.csv', 'a')
# Use csv Writer
csvWriter = csv.writer(csvFile)
s = set()




for tweet in tweepy.Cursor(api.search, 
                    q=('swimming pool OR swimming pool party OR swimming pool tips OR swimming fun'), 
                    Since="2016-08-09", 
                    until="2014-02-15", 
                    lang="en",tweet_mode='extended').items():

	t = re.sub(r"http\S+", "", tweet.full_text.encode('utf-8'))
	if (not tweet.retweeted) and ('RT @' not in t) and t not in s:
		print t
		print '\n'
		s.add(t)
		csvWriter.writerow(t)

csvFile.close()


# Approach 2
# results = api.search(q=('swimming pool OR swimming pool party OR swimming pool tips OR swimming fun'),lang="en", tweet_mode='extended')

# for tweet in results:
# 	t = re.sub(r"http\S+", "", tweet.full_text.encode('utf-8'))
# 	if (not tweet.retweeted) and ('RT @' not in t) and t not in s:
# 		print t
# 		print '\n'
# 		s.add(t)




# Approach 3

# geocode=str(location_latitude)+","+str(location_longitude)+",10000mi"

# class MyStreamListener(tweepy.StreamListener):
#     def on_status(self, status):
#     	t = re.sub(r"http\S+", "", status.full_text.encode('utf-8'))

#     	if (not tweet.retweeted) and ('RT @' not in t) and t not in s:
# 			print t
# 			print '\n'
# 			s.add(t)

# 		# print(status.text)


# # api = tweepy.API(auth,wait_on_rate_limit=True)
# l = MyStreamListener()
# stream = tweepy.Stream(auth, l)


# stream.filter(track=['swimming pool','pool party'],tweet_mode='extended')


  
