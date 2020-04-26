#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 07:24:55 2020

@author: dignazio
"""

import tweepy
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
csvFile = open('output100-' + lastweek +'.csv', 'a', encoding='utf8')
fieldnames = ['tweet_id', 'datetime', 'user_id', 'username', 'is_retweet', 'text']
csvWriter = csv.writer(csvFile)
csvWriter.writerow(fieldnames)

search_terms = 'data feminism OR #datafeminism'

for status in tweepy.Cursor(api.search,
                       q=search_terms,
                       since=lastweek, until=today,
                       count=200,
                       result_type='recent',
                       include_entities=True,
                       monitor_rate_limit=True, 
                       wait_on_rate_limit=True,
                       lang="en").items():

    eastern_time = status.created_at - timedelta(5)
    edt_time = eastern_time.strftime('%Y-%m-%d %H:%M')
    isRT = hasattr(status, 'retweeted_status')
    
    csvWriter.writerow([status.id, status.created_at, status.user.id, status.user.screen_name, isRT, status.text.encode('utf-8')])
csvFile.close()