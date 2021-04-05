#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 07:24:55 2020

@author: dignazio
"""

import tweepy
import json
import csv
import os
from datetime import datetime,timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "apikeys.env"))


# Enter Twitter API Keys
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Set up search dates btw now and a week ago
now = datetime.today()
today = now.strftime('%Y-%m-%d')

weekago= now - timedelta(days=7)
lastweek = weekago.strftime('%Y-%m-%d')

# Set up CSV file
fname = 'output-' + lastweek +'.csv'
csvFile = open(fname, 'w', encoding="utf-8")

fieldnames = ['tweet_id', 'datetime', 'user_id', 'username', 'is_retweet', 'text', 'is_quoted_tweet', 'favorite_count', 'retweet_count', 'replying_to_username', 'tweet_url']
csvWriter = csv.writer(csvFile)
csvWriter.writerow(fieldnames)

# Set up search terms
search_terms = 'data feminism OR #datafeminism'

# Search API and write results to csv file
# This way of searching can only go back 1 week
for status in tweepy.Cursor(api.search,
                       q=search_terms,
                       since=lastweek, until=today,
                       count=200,
                       result_type='recent',
                       include_entities=True,
                       monitor_rate_limit=True, 
                       wait_on_rate_limit=True,
                       lang="en", tweet_mode='extended').items():

    #Put creation date in Eastern time zone 
    eastern_time = status.created_at - timedelta(5)
    edt_time = eastern_time.strftime('%Y-%m-%d %H:%M')
    
    isRT = hasattr(status, 'retweeted_status')
    
    is_quoted_tweet = False
    if hasattr(status, 'is_quote_status'):
        is_quoted_tweet = status.is_quote_status
        
    tweet_url = 'https://twitter.com/' + status.user.screen_name + '/status/' + str(status.id)

    tweet_text = str(json.loads(json.dumps(status.full_text)))
    
    csvWriter.writerow([status.id, status.created_at, status.user.id, status.user.screen_name, isRT, tweet_text, is_quoted_tweet, status.favorite_count, status.retweet_count, status.in_reply_to_screen_name, tweet_url])

csvFile.close()
print("Success! Created file " + fname)