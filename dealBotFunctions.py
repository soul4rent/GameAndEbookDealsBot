import os, sys #import from parent directory
#possible TODO: Make things easier and just change it to a file with a git ignore.
#I made this project before I knew what it was, and this was my workaround
#for not showing everyone in the world my passwords for my bot.
#UPDATE: definately change... later

#TODO: Didn't work initially on my Raspberry Pi, so need to change.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import secure
import praw
import time
import threading as thr
from datetime import datetime


#initialized as globals. Lets see if it works.
#words that trigger positive
trigger_words = ["free", "100%"]

#words that trigger filter
filter_words = ["free shipping", "free weekend", "free to play"]

retString = "" #large string of games to return

initialized = False #see if bot is currently initialized to prevent abuse

data_lock = False
#simple way of keeping retString from being read until AFTER it is changed.
#might want to switch over to built in semaphores/locks later if the overall
#design is terrible.


def preventTimeouts(): #relogs in every 60 seconds to prevent timeouts, then gets the games
    global retString #string that constantly gets updated
    global data_lock #mutex for the return string (for GimmeGames method) 
    while True:

            #from what I understand, this is what logs the reddit bot in
            bot = praw.Reddit(user_agent='GameDealBot v0.1',
                client_id=secure.client_id,
                client_secret=secure.client_secret,
                username=secure.user,
                password=secure.password)

            subreddit = bot.subreddit("AndroidGameDeals+GameDeals+ebookdeals+FreeGamesOnAndroid")

            retString = "" #reset return string so that it can be refreshed

            #-------MUTEX--------
            data_lock = True
            
            for submission in subreddit.hot(limit=50):

                title = submission.title.lower() #sets the title to lower case to make string manipulation more friendly

                #help make code look cleaner
                subreddit = str(submission.subreddit).lower()
                score = submission.score
                
                #if the item isn't terrible
                if (score > 20 and subreddit == "gamedeals") or (score > 3 and subreddit == "androidgamedeals") or (score > 3 and subreddit == "freegamesonandroid") or (subreddit == "ebookdeals"): 
                    #trying to eliminate false positives (todo: look into using regex/database)
                    if phraseFilter(title, trigger_words, filter_words):

                            #print("=========================")
                            retString += "============ \n"
                            #print("Title: ", submission.title)
                            retString += "Title: " #post title
                            retString += str(submission.title)
                            retString += "\n"
                            #print("Score: ", submission.score)
                            retString += "Score: " #reddit post score
                            retString += str(submission.score)
                            retString += "\n"
                            #print(submission.subreddit)
                            retString += str(submission.subreddit) #subreddit where the free thing came from
                            retString += "\n"
                            #print("Post created ", datetime.fromtimestamp(submission.created)) #convert UTC time when post created to something readable
                            retString += "Post created "
                            retString += str(datetime.fromtimestamp(submission.created)) #timestamp of reddit post
                            retString += "\n"
                            retString += str(submission.url) #link to free thing
                            retString += "\n"
                            #print("=========================\n")

            data_lock = False
            #------END-MUTEX-------
            
            time.sleep(60) #prevent API abuse, since the reddit api only allows access every 3 seconds. This is a bit overkill, but free games aren't posted that often anyway.

    

def init(): #must be run before bot can start.
    global initialized

    #TODO: check to see if built in thread locking would be better
    if (not initialized):
        print("initialized!")
        initialized = True
        t1 = thr.Thread(target=preventTimeouts, args=[])
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
    while True:
        if data_lock == True:
            time.sleep(1)
        else:
            s = retString
            return s
