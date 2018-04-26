import os, sys #import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import secure
import praw
import time
from datetime import datetime


def phraseTrigger(phrase): #loops through trigger words and returns true if the phrase contains a word
    return True
    

def phraseFilter(phrase):
    return True



#words that trigger positive
trigger_words = ["free", "100%"]

#words that do not trigger response
banned_words = ["free shipping", "free weekend", "free this weekend", "free to play"]

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
                #too many words to keep track of. Currently making a list and having it check through them. If list gets too long, switching to regex or database

                if freegames.count(title) == 0: #game not already in the list of free games
                    freegames.append(title)
                    print("=========================")
                    print("Title: ", submission.title)
                    print("Score: ", submission.score)
                    print(submission.subreddit)
                    print("Post created ", datetime.fromtimestamp(submission.created)) #convert UTC time when post created to something readable
                    print("=========================\n")

    time.sleep(60) #sleep for 60 seconds
