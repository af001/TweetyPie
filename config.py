#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@author      : Anton Foltz
@professor   : Dr. Thomas Miller
@date        : 04/29/2018
@class       : MSDS 452 - Web and Data Analytics
@description : Configuration file for TweetyPi 
@filename    : config.py
'''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              LIBRARY IMPORTS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tweepy
import pandas as pd

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                          TWEETYPIE DEFAULT SETTINGS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

class Config():
    ## GLOBAL VARIABLES - TWITTER DEFAULT SETTINGS ##
        
    # Authenticate on start to minimize auth API calls
    auth = tweepy.OAuthHandler('key', 
                               'secret')
    
    auth.set_access_token('key', 
                         'secret')
    
    API = tweepy.API(auth)
    
    # Set a default table name for SQLAlchemy
    SQL_TABLE = 'tweets'
    
    # Set a default name for the SQLAlchemy database
    DB_NAME = 'tweets.db'
    
    # Set a default language
    LANG = 'all'
    
    # Set a default tweets to return per page (max 100)
    MAX_TWEETS = 1000
    
    # Set a default since_id. Default is 3 days.
    SINCE_ID = '1970-01-01'
    #limit = (dt.datetime.now() - dt.timedelta(days=3)).date()
    #since_id = '{}-{}-{}'.format(limit.year, limit.month, limit.day)
    
    # Available Twitter lanaguages for queries
    LANGUAGES = {'en': 'English', 'ar': 'Arabic', 'bn': 'Bengali', 'cs': 'Czech', 
                 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'es': 'Spanish', 
                 'fa': 'Persian', 'fi': 'Finnish', 'fil': 'Filipino', 'fr': 'French',
                 'he': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian', 'id': 'Indonesian',
                 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'msa': 'Malay',
                 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portugese',
                 'ro': 'Romanian', 'ru': 'Russian', 'sv': 'Swedish', 'th': 'Thai',
                 'tr': 'Turkish', 'uk': 'Ukranian', 'ur': 'Urdu', 'vi': 'Vietnamese',
                 'zn-ch': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)'}
    
    # Pandas and SQL column names
    COLUMNS = ['id_str', 'created_at', 'screen_name', 'user_name', 'retweet_ct',
               'favorite_ct', 'language', 'text', 'hashtags', 'mentions', 'urls', 
               'link']
    
    # Main Pandas dataframe
    TWEETS_DF = pd.DataFrame(columns=COLUMNS)
