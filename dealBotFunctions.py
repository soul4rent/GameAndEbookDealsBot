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



def GimmeGames():
    
    #words that trigger positive
    trigger_words = ["free", "100%"]

    #words that trigger filter
    filter_words = ["free shipping", "free weekend", "free to play"]

    retString = "" #Giant String with free games in it
    
    bot = praw.Reddit(user_agent='GameDealBot v0.1',
                  client_id=secure.client_id,
                  client_secret=secure.client_secret,
                  username=secure.user,
                  password=secure.password)

    subreddit = bot.subreddit("AndroidGameDeals+GameDeals+ebookdeals+FreeGamesOnAndroid")


    for submission in subreddit.hot(limit=50):

        title = submission.title.lower() #sets the title to lower case to make string manipulation more friendly

        #help make code look cleaner
        subreddit = str(submission.subreddit).lower()
        score = submission.score
        
        #if the item isn't terrible
        if (score > 20 and subreddit == "gamedeals") or (score > 3 and subreddit == "androidgamedeals") or (score > 3 and subreddit == "freegamesonandroid") or (subreddit == "ebookdeals"): 
            #trying to eliminate false positives (todo: use regex if list of keywords gets too long)
            if phraseFilter(title, trigger_words, filter_words):

                    #print("=========================")
                    retString += "============ \n"
                    #print("Title: ", submission.title)
                    retString += "Title: " #post title
                    retString += str(submission.title)
                    retString += "\n"
                    #print("Score: ", submission.score)
                    retString += "Score: " #post score
                    retString += str(submission.score)
                    retString += "\n"
                    #print(submission.subreddit)
                    retString += str(submission.subreddit) #subreddit
                    retString += "\n"
                    #print("Post created ", datetime.fromtimestamp(submission.created)) #convert UTC time when post created to something readable
                    retString += "Post created "
                    retString += str(datetime.fromtimestamp(submission.created)) #timestamp
                    retString += "\n"
                    retString += str(submission.url) #link to free thing
                    retString += "\n"
                    #print("=========================\n")

    time.sleep(3) #prevent Reddit API abuse
    return retString
