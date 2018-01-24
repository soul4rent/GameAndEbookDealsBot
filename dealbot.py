

import smptlib
#attempt to create SMTP server to email me the free games.


import praw
import time
from datetime import datetime

import os, sys #import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import secure
#Name misleading.
#Literally just a python file in the parent directory
#named "secure.py" with four plaintext variables.
#On the local machine only, referenced by this script.
#It's not secure, so make a throwaway account to use.


freegames = [] #make a string list so not spammed with free games


while True: #run forever until forced stop. Doesn't matter if user friendly. Only for my personal use.   

    #relogin every 60 seconds to prevent timeouts
    bot = praw.Reddit(user_agent='GameDealBot v0.1',
                  client_id=secure.client_id,
                  client_secret=secure.client_secret,
                  username=secure.user,
                  password=secure.password)

    #multireddit with deals from various subreddits
    subreddit = bot.subreddit("AndroidGameDeals+GameDeals+ebookdeals+FreeGamesOnAndroid")


    for submission in subreddit.hot(limit=50):

        title = submission.title.lower() #sets the title to lower case to make string manipulation more friendly

        #help make code look cleaner
        subreddit = str(submission.subreddit).lower()
        score = submission.score
        
        #if the item isn't terrible
        if (score > 20 and subreddit == "gamedeals") or (score > 3 and subreddit == "androidgamedeals") or (score > 3 and subreddit == "freegamesonandroid") or (subreddit == "ebookdeals"): 
            #trying to eliminate false positives (todo: use regex if list of keywords gets too long)
            if (title.find('free') != -1 or title.find('100%') != -1) and (title.find('free shipping') == -1) and (title.find('free weekend') == -1) and (title.find('free to play') == -1):
                if freegames.count(title) == 0: #game not already in the list of free games
                    freegames.append(title)
                    print("=========================")
                    print("Title: ", submission.title)
                    print("Score: ", submission.score)
                    print(submission.subreddit)
                    print("Post created ", datetime.fromtimestamp(submission.created)) #convert UTC time when post created to something readable
                    print("=========================\n")

    time.sleep(60) #sleep for 60 seconds
