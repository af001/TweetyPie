set #!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@author      : Anton
@date        : 04/29/2018
@description : Python 3 tool that can be used to extract tweets from Twitter
               using the Twitter API. The tool stores all tweets in a pandas 
               dataframe, and the user can save the tweets to a sqlalchemy 
               database once complete. 
@filename    : tweetypie.py
'''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              EXAMPLE USAGE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
set query 10    : Set query to a max of 10 tweets
set table dfir  : Override the default table and name it dfir
query dfir hack : Query Twitter for instances of text containing query hack
flush tweets    : Not satisfied with output, flush dfir hack query results
query #dfir     : Query Twitter for instances of text containing #dfir
save tweets     : Save tweet to the database, using default (twitter.db)
csv dfir        : Export the results to a csv file
exit            : Exit the console application
'''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              LIBRARY IMPORTS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import time
import glob
import signal
import tweepy
import datetime as dt
import pandas as pd
import numpy as np
from cmd import Cmd
from pyfiglet import Figlet
from config import Config
from sqlalchemy import create_engine, inspect

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                              TWEETYPIE CMDLETS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
    
class TweetyPie(Cmd):
    
    '''
    # Initial logo and version display
    '''
    def preloop(self):
        fig = Figlet(font='big')
        print(fig.renderText('TweetyPie'))
        print('Version 1.0a')
    
    '''
    # Query Twitter for tweets based on hashtag, mention, or keywords
    Usage:
        query <key_words>   : Retrieve tweets based on key words
    '''
    def do_query(self, query):
        # Add url enconding for a space to allow searching multiple terms
        words = query.split(' ')
        if len(words) > 1:
            q = '%20'.join(words)
        else:
            q = words[0]
        
        # Code from @gumption at https://stackoverflow.com/questions/22469713/
        # managing-tweepy-api-search         
        # Alternative method using pagination. The method is harder to get unique,
        # non-retweets.
        searched_tweets = []
        last_id = -1
        
        while (len(searched_tweets) < config.MAX_TWEETS):
            
            time.sleep(2)
            # Attempt to query based on variables that have been set by the 
            # user. Variables include: lang, since_id, count, q
            count = config.MAX_TWEETS - len(searched_tweets)
            try:
                if config.LANG == 'all' and config.SINCE_ID == '1970-01-01':
                    new_tweets = config.API.search(q=q, 
                                                   count=count, 
                                                   max_id=str(last_id-1))
                elif config.LANG != 'all' and config.SINCE_ID == '1970-01-01':
                    new_tweets = config.API.search(q=q, 
                                                   count=count, 
                                                   max_id=str(last_id-1), 
                                                   lang=config.LANG)
                elif config.LANG == 'all' and config.SINCE_ID != '1970-01-01':
                    new_tweets = config.API.search(q=q, 
                                                   count=count, 
                                                   max_id=str(last_id-1), 
                                                   since_id = config.SINCE_ID)
                elif config.LANG != 'all' and config.SINCE_ID != '1970-01-01':
                    new_tweets = config.API.search(q=q, 
                                                   count=count, 
                                                   max_id=str(last_id-1), 
                                                   since_id = config.SINCE_ID)
                
                # Break the while loop if there are no new tweets
                if not new_tweets:
                    break
                
                # Mitigate duplicates. Only add tweets that do not begin with RT
                # to the list
                for tweet in new_tweets:
                    if not tweet.text.startswith('RT'):
                        searched_tweets.append(tweet)
                
                # Since we aren't using pagination, we need a marker
                last_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                print('\n[!] Search parameters resulted in an error. Please reset.')
                break
        
        # Process tweets - Store in a pandas dataframe, and show the first 5 
        # tweets to the user.
        clean_tweets = []       
        if len(searched_tweets) > 0:
            print('\n[COLLECTION PREVIEW]')
        
        # Loop over the tweets and begin processing        
        for tweet in searched_tweets:
            tweets = {}
            mentions = []
            urls = []
            hashtags = []
            
            # Print the first 5 tweets to the user. 
            if len(clean_tweets) < 5:
                print('\n[TWEET]')
                if tweet.text.startswith('RT'):
                    print('Retweet detected!')
                
                # Remove white space and newlines in some tweets
                print(stringify_text(tweet.text))
                print('\nScreenName : @{}'.format(tweet.user.screen_name))
                print('UserName   : {}'.format(tweet.user.name))
                print('Date       : {}'.format(tweet.created_at))
                print('Retweet Ct : {}'.format(tweet.retweet_count))
                print('Favorit Ct : {}'.format(tweet.favorite_count))
                print('Language   : {}'.format(tweet.lang))
                print('Tweet id   : {}'.format(tweet.id_str))
            
            # Process hashtags, print and store
            try:
                hashtag = tweet.entities['hashtags']
            except:
                hashtag = None
                
            if hashtag is not None:
                if len(clean_tweets) < 5:
                    print('Hashtags   :', end=' ')
                for i in hashtag:
                    hashtags.append(remove_non_ascii(i['text']))
                    if len(clean_tweets) < 5:
                        print('#{}'.format(i['text']), end=' ')
            
            # Process mentions, print and store
            try:
                mention = tweet.entities['user_mentions']
            except:
                mention = None
                
            if mention is not None:
                if len(clean_tweets) < 5:
                    print('\nMentions   :', end=' ')
                for i in mention:
                    mentions.append(remove_non_ascii(i['screen_name']))
                    if len(clean_tweets) < 5:
                        print('@{}'.format(i['screen_name']), end=' ')
            
            # Process urls, store only
            try:
                url = tweet.entities['urls']
            except:
                url = None
                
            if url is not None:
                for i in url:
                    urls.append(i['url'])
            
            if len(clean_tweets) < 5:
                print('\n[END TWEET]')
            
            # Store the results in a Python dictionary    
            tweets['id_str'] = int(tweet.id)
            tweets['created_at'] = str(tweet.created_at)
            tweets['screen_name'] = remove_non_ascii(tweet.user.screen_name)
            tweets['user_name'] = remove_non_ascii(tweet.user.name)
            tweets['retweet_ct'] = int(tweet.retweet_count)
            tweets['favorite_ct'] = int(tweet.favorite_count)
            tweets['text'] = stringify_text(tweet.text)
            tweets['language'] = tweet.lang
            
            if len(hashtags) > 0:
                tweets['hashtags'] = ' '.join(hashtags)
            else:
                tweets['hashtags'] = np.nan
            
            if len(mentions) > 0:
                tweets['mentions'] = ' '.join(mentions)
            else:
                tweets['mentions'] = np.nan
                
            if len(urls) > 0:
                tweets['urls'] = ' '.join(urls)
            else:
                tweets['urls'] = np.nan
                
            tweets['link'] = 'https://twitter.com/i/web/status/{}'.format(tweet.id_str)
            
            # Add the tweet in the form of a Python dictionary to a list
            clean_tweets.append(tweets)
        
        # Add list of Python dictionaries to the working Pandas dataframe. Modify
        # type for integers and datetime. Append the newly created dataframe
        # to the main dataframe and resent the index
        df = pd.DataFrame(clean_tweets)
        #df['retweet_ct'] = df['retweet_ct'].astype(np.int64)
        #df['favorite_ct'] = df['favorite_ct'].astype(np.int64)
        config.TWEETS_DF = config.TWEETS_DF.append(df, ignore_index=True)
        config.TWEETS_DF.reset_index(drop=True)
         
        # DEBUG ONLY - Verify tweets are in the dataframe correctly
        # print(config.TWEETS_DF.head(5))
        
    '''
    # Help command for do_query 
    Usage:
        help query   : show usage and description to console
    '''    
    def help_query(self):
        print('\nSet application settings')
        print('Usage:')
        print('  query <key_words>   : Retrieve tweets based on key words')

    '''
    # Restore values to defaults. Defaults include: lang, date, size, all
    Usage:
        unset lang   : Reset the language to 'all'
        unset date   : Reset the date to 1970-01-01
        unset size   : Reset the size to 1000
        unset all    : Reset all values to their default
    '''
    def do_unset(self, arg):
        global config
        
        # Validate user input and process. Print values if unset command is
        # successful
        if arg == 'lang':
            config.LANG = 'all'
            print('\n[+] Language set to default.')
        elif arg == 'date':
            config.SINCE_ID = '1970-01-01'
            print('\n[+] Date set to default.')
        elif arg == 'size':
            config.MAX_TWEETS = 1000
            print('\n[+] Size set to default.')
        elif arg == 'all':
            config.LANG = 'all'
            config.SINCE_ID = '1970-01-01'
            config.MAX_TWEETS = 1000
            print('\n[+] Defaults set:')
            print('  Language : {}'.format(config.LANG))
            print('  Size     : {}'.format(config.MAX_TWEETS))
            print('  Date     : {}'.format(config.SINCE_ID))
        else:
            print('\n[!] No argument! Run \'help unset\'')
            
    '''
    # Help command for do_unset 
    Usage:
        help unset   : show usage and description to console
    '''    
    def help_unset(self):
        print('\nSet application settings')
        print('Usage:')
        print('  unset lang   : Reset the language to \'all\'')
        print('  unset date   : Reset the date to 1970-01-01')
        print('  unset size   : Reset the size to 1000')
        print('  unset all    : Reset all values to their default')
    
    '''
    # Modify a default value. Values include table, db, size, date, lang
    Usage:
        set lang <lang_code>   : Set the language for tweets
        set table <table_name> : Set the name of the database table
        set db <db_name>       : Set the name of the database 
        set size <size>        : Set the max number of tweets
        set date <date>        : Set the since date (YYYY-MM-DD)
    '''    
    def do_set(self, args):
        global config
        
        # Split the args variable. If there aren't two variables, complain       
        x = args.split(' ')
        if len(x) != 2:
            print('\n[!] Invalid arguments. Run \'help set\'')
            return
        
        arg1 = x[0]
        arg2 = x[1]
        
        # Process the command based on user input. Assign the value and print 
        # success 
        if arg1 == 'table':
            config.SQL_TABLE = arg2
            print('\n[+] Table set to {}!'.format(arg2))
        elif arg1 == 'db':
            try:
                if arg1.split('.')[1] == '.db':
                    config.DB_NAME = arg2
                    print('\n[+] Database set to {}!'.format(arg2))
            except IndexError:
                config.DB_NAME = arg2 + '.db'
                print('\n[+] Database set to {}!'.format(arg2))
        elif arg1 == 'size':
            print('\n[+] Number of tweets set to {}'.format(int(arg2)))
            config.MAX_TWEETS = int(arg2)
        elif arg1 == 'date':
            print('\n[+] Search set to query last {} days'.format(arg2))
            config.SINCE_ID = (dt.datetime.now() - dt.timedelta(days=int(arg2))).date()
        elif arg1 == 'lang':
            print('\n[+] Search set to search for \'{}\' tweets'.format(arg2))
            config.LANG = arg2
        else:
            print('\n[!] Invalid argument. Run \'help set\'')
            
    '''
    # Help command for do_set 
    Usage:
        help set   : show usage and description to console
    '''    
    def help_set(self):
        print('\nSet application settings')
        print('Usage:')
        print('  set lang <lang_code>   : Set the language for tweets')
        print('  set table <table_name> : Set the name of the database table')
        print('  set db <db_name>       : Set the name of the database')
        print('  set size <size>        : Set the max number of tweets')
        print('  set date <date>        : Set the since date (YYYY-MM-DD)')

    '''
    # Display the configuration settings that have been set by the user
    Usage:
        show table      : Display the current working database table
        show db         : Display the current working database
        show size       : Display the max number of tweets to query
        show date       : Display the since date for querying
        show lang       : Display the desired tweet language
        show defaults   : Display all settings
        show lang codes : Display language codes
    '''        
    def do_show(self, arg):  
        # Split the args variable. If there aren't two variables, complain       
        x = arg.split(' ')
        arg1 = arg
        arg2 = None
        
        try:
            arg1 = x[0]
            arg2 = x[1]
        except IndexError:
            pass
        
        if arg1 == 'table':
            print('\n[+] Default table: {}'.format(config.SQL_TABLE))
        elif arg1 == 'db':
            print('\n[+] Default database: {}'.format(config.DB_NAME))
        elif arg1 == 'size':
            print('\n[+] Default size: {}'.format(config.MAX_TWEETS))
        elif arg1 == 'date':
            print('\n[+] Default date: {}'.format(config.SINCE_ID))
        elif arg1 == 'lang' and arg2 != 'codes':
            print('\n[+] Default language: {}'.format(config.LANG))
        elif arg1 == 'lang' and arg2 == 'codes':
            print('\n[+] Language Codes:')
            for code in config.LANGUAGES:
                print('  {}\t: {}'.format(code, config.LANGUAGES[code]))
        elif arg1 == 'defaults':
            print('\n[+] Defaults:')
            print('  Table    : {}'.format(config.SQL_TABLE))
            print('  Database : {}'.format(config.DB_NAME))
            print('  Language : {}'.format(config.LANG))
            print('  Size     : {}'.format(config.MAX_TWEETS))
            print('  Date     : {}'.format(config.SINCE_ID))
        else:
            print('\n[!] Invalid argument!. Run \'help show\'')
            
    '''
    # Help command for do_show 
    Usage:
        help show   : show usage and description to console
    '''    
    def help_show(self):
        print('\nShow default settings')
        print('Usage:')
        print('  show table      : Display the current working database table')
        print('  show db         : Display the current working database')
        print('  show size       : Display the max number of tweets to query')
        print('  show date       : Display the since date for querying')
        print('  show lang       : Display the desired tweet language')
        print('  show defaults   : Display all settings')
        print('  show lang codes : Display language codes')
            
    '''
    # Save reviews on user demand to the local sqlalchmey database. 
    Usage:
        save tweets   : Save all past retrieved tweets into a database called 
                        <db_name> in a table called <table_name>
    '''          
    def do_save(self, arg):
        global config
        
        # If the argument is 'tweets', then store into the database and table
        # that was defined by the user (or use the defaults). Data will be
        # stored in a SQLAlchemy database in the working path
        if arg == 'tweets':
            engine = create_engine('sqlite:///{}'.format(config.DB_NAME))
            con = engine.connect()
            config.TWEETS_DF.to_sql(name=config.SQL_TABLE, index=False, con=con, 
                                    if_exists='append')
            config.TWEETS_DF = pd.DataFrame(columns=config.COLUMNS)
            con.close()
        
            print('\n[+] Save complete!')
        else:
            print('\n[!] Invalid argument! Run \'help save\'')

    '''
    # Help command for do_save 
    Usage:
        help save   : show usage and description to console
    '''    
    def help_save(self):
         print('\nSaves tweets to a local SQL database')
         print('Usage:\n  save tweets')
    
    '''
    # Flush the results of a query. Note: If a previous query was performed
    # and not saved, the data will be lost. 
    Usage:
        flush tweets   : Flush tweets from the Pandas dataframe
    '''      
    def do_flush(self, arg):
        global config
        
        if arg == 'tweets':
            config.TWEETS_DF = pd.DataFrame(columns=config.COLUMNS)
            print('\n[+] Successfully flushed tweets!')
        else:
            print('\n[!] Invalid argument. Run \'help flush\'')
            
        '''
    # Help command for do_flush
    Usage:
        help flush   : show usage and description to console
    '''    
    def help_flush(self):
         print('\nFlushes all tweets from the Pandas dataframe. If used before ' +
               'the save command, all previous queries will be lost!')
         print('Usage:\n  flush tweets   : Flush tweets from the Pandas dataframe')
         
    '''
    # Exit the application
    Usage:
        exit : exit the application                     
    '''          
    def do_exit(self, now):
        print('\nYou\'re My Boy, Blue! - [Old School]')
        os.kill(os.getpid(), signal.SIGINT)

    '''
    # Help command for do_exit 
    Usage:
        help exit : show usage and description to console
    '''           
    def help_exit(self):
        print('\nExit the application')
        print('Usage:\n  exit')
        
    '''
    # Inspect database for available tables and local path for databases 
    Usage:
        inspect tables    : Show available tables in working database
        inspect databases : Show available databases in working path
    '''           
    def do_inspect(self, arg):
        global config
        
        # Check tables argument and print them to the console
        if arg == 'tables':
            engine = create_engine('sqlite:///{}'.format(config.DB_NAME))
            inspector = inspect(engine)
            
            if inspector is not None:
                print('\n[+] Available Tables:', end=' ')
                for table in inspector.get_table_names():
                    print(table, end=' ')
                print()
            else:
                print('\n[!] No sotred tables found!\n')
        elif arg == 'databases':
            os.chdir(os.getcwd())
            print('\n[+] Available Databases:', end=' ')
            for file in glob.glob("*.db"):
                print(file, end=' ')
            print()
        else:
            print('\n[!] Invalid inspect command! Run \'help inspect\' for details.\n')
            
    '''
    # Help command for do_inspect 
    Usage:
        help inspect : show usage and description to console
    '''           
    def help_inspect(self):
        print('\nShow available tables stored in the database')
        print('Usage:')
        print('  inspect tables    : Show available tables in working database')
        print('  inspect databases : Show available databases in working path')
    
    '''
    # Read sqlalchemy table and export to a csv for post-processing  
    Usage:
        csv <table_name> : read sqlalchemy table and store as a csv in the user's
                           working directory
    '''           
    def do_csv(self, table_name):
        # Set variables and instantiate a db connector
        now = dt.datetime.now()
        sql = 'SELECT * FROM {}'.format(table_name)
        engine = create_engine('sqlite:///{}'.format(config.DB_NAME))
        inspector = inspect(engine)
        
        # Get data and write to a csv in the user's path
        if table_name in inspector.get_table_names():
            con = engine.connect()              
            df = pd.read_sql(sql, con=con, columns=config.COLUMNS)              
            df.to_csv('{}-{}.csv'.format(table_name, 
                      now.strftime("%Y%m%d%H%M")), index=False, columns=config.COLUMNS)
            print('\n[+] File wrote to: {}-{}.csv'.format(os.getcwd()+'/'+
                  table_name, now.strftime("%Y%m%d%H%M")))
        else:
            print('\n[!] Table not in list!')
            
    '''
    # Help command for do_csv
    Usage:
        help csv : show usage and description to console
    '''           
    def help_csv(self):
        print('\nStore a sqlalchemy table to a csv')
        print('Usage:\n  csv <table_name>')
        
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                                   MAIN
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   

config = Config()

# Simple function to strip non-ascii characters from text
def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def stringify_text(text):
    text = text.splitlines()
    text = list(filter(None, text))
    text = ' '.join(text)  
    return remove_non_ascii(text)

'''
# Main application prompt
'''
def main():
    print()
    prompt = TweetyPie()
    prompt.prompt = '> '
    prompt.cmdloop('\nAt age 11, I audited my parents. Believe me, there were ' +
                   'some discrepancies, and I was grounded. - [The Other Guys]')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
