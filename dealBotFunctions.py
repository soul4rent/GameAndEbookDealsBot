import os, sys #import from parent directory
#TODO: Make things easier and just change it to a file with a git ignore.
#I made this project before I knew what it was, and this was my workaround
#for not showing everyone in the world my passwords for my bot.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import secure
import praw
import time
from threading import Thread
from datetime import datetime


#initialized as globals. Lets see if it works.
#words that trigger positive
trigger_words = ["free", "100%"]

#words that trigger filter
filter_words = ["free shipping", "free weekend", "free to play"]


initialized = False #see if bot is currently initialized to prevent abuse

#setting up bot as global.
bot = praw.Reddit(user_agent='GameDealBot v0.1',
            client_id=secure.client_id,
            client_secret=secure.client_secret,
            username=secure.user,
            password=secure.password)


def preventTimeouts():
    while True:
            time.sleep(60) #relogin every 60 seconds. Don't know if there is a better way.
            bot = praw.Reddit(user_agent='GameDealBot v0.1',
                client_id=secure.client_id,
                client_secret=secure.client_secret,
                username=secure.user,
                password=secure.password)
    

def init(): #an attempt to prevent timeouts through the power of threading
    global initialized
    if (not initialized):
        print("initialized!")
        initialized = True
        t1 = Thread(target=preventTimeouts, args=[])
        t1.start()


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

    retString = "" #Giant String with free games in it

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
