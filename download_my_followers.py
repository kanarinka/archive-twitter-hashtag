#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 07:24:55 2020

@author: dignazio
"""

import tweepy
import csv
import os
import json
import time


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

# Helper function to save data into a JSON file
# file_name: the file name of the data on Google Drive
# file_content: the data you want to save
def save_json(file_name, file_content):
  with open(BASE_DIR + file_name, 'w', encoding='utf-8') as f:
    json.dump(file_content, f, ensure_ascii=False, indent=4)
    
# Helper function to handle twitter API rate limit
def limit_handled(cursor, list_name):
  while True:
    try:
      yield cursor.next()    # Catch Twitter API rate limit exception and wait for 15 minutes
    except tweepy.RateLimitError:
      print("\nData points in list = {}") #.format(len(list_name))))
      print('Hit Twitter API rate limit.')
      for i in range(3, 0, -1):
        print("Wait for {} mins.".format(i * 5))
        time.sleep(5 * 60)    # Catch any other Twitter API exceptions
    except tweepy.error.TweepError:
      print('\nCaught TweepError exception' )



# MAIN GUY
fname = 'all-my-followers.csv'
csvFile = open(fname, 'a', encoding='utf8')
fieldnames = ['userid', 'username', 'screenname', 'location', 'friendscount', 'followerscount', 'url', 'description']
csvWriter = csv.writer(csvFile)
csvWriter.writerow(fieldnames)



# Create a list to store follower data
followers_list = []  # For-loop to iterate over tweepy cursors

for user in tweepy.Cursor(api.followers, count=200, monitor_rate_limit=True, wait_on_rate_limit=True).items():
                            
                            
#cursor = tweepy.Cursor(api.followers, count=200).pages()
#for i, page in enumerate(limit_handled(cursor, followers_list)):  
 #   print("\r"+"Loading"+ i % 5 *".", end='')

    # Add latest batch of follower data to the list
    #followers_list += page
    #for user in followers_list:
        
    print(user.id, user.name, user.screen_name, user.location, user.friends_count, user.followers_count, user.url, user.description)
    csvWriter.writerow([user.id, user.name, user.screen_name, user.location, user.friends_count, user.followers_count, user.url, user.description])


csvFile.close()
print("Success! Created file " + fname)

#followers_list = [x._json for x in followers_list]  # Save the data in a JSON file
#save_json('followers_data.json', followers_list)



'''
# Set up CSV file
fname = 'output-' + lastweek +'.csv'
csvFile = open(fname, 'a', encoding='utf8')
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
print("Success! Created file " + fname)
'''