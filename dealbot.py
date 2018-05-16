import os, sys #import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import secure
import praw
import time
from datetime import datetime


def phraseFilter(phrase, t_words, f_words): #loops through trigger words and returns true if the phrase contains a word, but not a filter word
    for x in f_words: #filter out duds
        if x.lower() in phrase:
            return False
        
    for y in t_words: #add successes
        if y.lower() in phrase:
            return True
        else:
            return False
        
    
#words that trigger positive
trigger_words = ["free", "100%"]

#words that trigger filter
filter_words = ["free shipping", "free weekend", "free to play"]

freegames = [] #make a string list of already printed games so not spammed with free games (script runs continuously)

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

        title = submission.title.lower()
        #sets the title to lower case to make string manipulation more friendly

        subreddit = str(submission.subreddit).lower()
        score = submission.score
        
        #if the item isn't terrible (TODO: update to dictionary)
        if (score > 20 and subreddit == "gamedeals") or (score > 3 and subreddit == "androidgamedeals") or (score > 3 and subreddit == "freegamesonandroid") or (subreddit == "ebookdeals"): 
            #Currently using a list and having it check through them. If list gets too long, switching to regex or database
            if phraseFilter(title, trigger_words, filter_words):
                
                if freegames.count(title) == 0: #game not already in the list of free games
                    freegames.append(title)
                    print("=========================")
                    print("Title: ", submission.title)
                    print("Score: ", submission.score)
                    print(submission.subreddit)
                    print("Post created ", datetime.fromtimestamp(submission.created)) #convert UTC time when post created to something readable
                    print("=========================\n")

    time.sleep(60)
    #Sleep to prevent Reddit Timeouts. Program keeps getting games as it find them.
