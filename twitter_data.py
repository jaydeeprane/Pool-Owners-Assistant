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

location_longitude = location['longitude']
location_latitude = location['latitude']


consumer_key = 'X8JfHtFAy47DD1cYWBbtCawZm'
consumer_secret = 'LgA9cIhl6apmcs0XieqUkAk4uYOzSaNoqFxDli1edo9jC56zRS'
access_token = '578485087-7RLurdjG7Kx4BpsTJZ1hCAgewvKxZQipuolGaxJq'
access_secret = 'SvW0LmgIqesjMiQwFkca6ds2XR3gKnn1G1pHjM6HFpfKJ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
# geocode=str(location_latitude)+","+str(location_longitude)+",10000mi"

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)


# api = tweepy.API(auth,wait_on_rate_limit=True)
l = MyStreamListener()
stream = tweepy.Stream(auth, l)


stream.filter(track=['swimming pool','pool party'])


  