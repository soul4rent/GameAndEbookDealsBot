import os, sys #import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import smtplib
import secure
import praw
import time
from datetime import datetime

#words that trigger positive
trigger_words = ["free", "100%"]

#words that trigger filter
filter_words = ["free shipping", "free weekend", "free to play"]


def phraseFilter(phrase, t_words, f_words): #loops through trigger words and returns true if the phrase contains a word, but not a filter word
    for x in f_words: #filter out duds
        if x.lower() in phrase:
            return False
        
    for y in t_words: #add successes
        if y.lower() in phrase:
            return True
        else:
            return False

        
#prints out free games
def prettyPrintGames(freegames):
    for submission in freegames:
        print("=========================")
        print("Title: ", submission.title)
        print("Score: ", submission.score)
        print(submission.subreddit)
        print("Post created ", datetime.fromtimestamp(submission.created)) #convert UTC time when post created to something readable
        print("Url: ", submission.url)
        print("=========================\n")


#takes list of free games, and returns a pretty string
def prettyFormatGames(freegames):
    returnString = ""
    for submission in freegames:
        returnString=returnString+ "=========================\n"
        returnString=returnString+ "Title: " + str(submission.title) + "\n"
        returnString=returnString+ "Score: " + str(submission.score) + "\n"
        returnString=returnString+ str(submission.subreddit) + "\n"
        returnString=returnString+ "Post created " + str(datetime.fromtimestamp(submission.created)) + "\n"
        returnString=returnString+ "URL: " + str(submission.url) + "\n"
        returnString=returnString+ "=========================\n"
    return returnString


#sets up a temp SMTP server and sends an email.
def simpleSmtpSendGames(smtpAddress, email, email_password, targetEmail, freegames):
    smtpClient=smtplib.SMTP(smtpAddress, 587)
    smtpClient.ehlo()
    smtpClient.starttls()
    smtpClient.login(email, email_password)
    smtpClient.sendmail(email, targetEmail, "Subject: [Automated] Games Scraped from Reddit! \n"
                        +prettyFormatGames(freegames))
    smtpClient.quit()

def gimmeGames(gamedeals_min, android_gamedeals_min, free_games_android_min, ebook_deals_min):
    bot = praw.Reddit(user_agent='GameDealBot v0.1',
                  client_id=secure.client_id,
                  client_secret=secure.client_secret,
                  username=secure.user,
                  password=secure.password)

    #multireddit with deals from various subreddits
    subreddit = bot.subreddit("AndroidGameDeals+GameDeals+ebookdeals+FreeGamesOnAndroid")

    freegames = []

    for submission in subreddit.hot(limit=50):

        #sets the title to lower case to make string manipulation more friendly
        title = submission.title.lower()
        subreddit = str(submission.subreddit).lower()

        score = submission.score
        
        #if the item isn't terrible (TODO: update to dictionary)
        if (score > gamedeals_min and subreddit == "gamedeals") or (score > android_gamedeals_min and subreddit == "androidgamedeals") or (score > free_games_android_min and subreddit == "freegamesonandroid") or (score > ebook_deals_min and subreddit == "ebookdeals"): 
            #Currently using a list and having it check through them. If list gets too long, switching to regex or database
            if phraseFilter(title, trigger_words, filter_words):
                
                if freegames.count(title) == 0: #game not already in the list of free games
                    freegames.append(submission)

    return freegames #returns list of submission objects with tiles, links, post scores, etc.
                    

if __name__ == '__main__': #example use
    gameList = gimmeGames(20, 3, 3, 1)
    prettyPrintGames(gameList)

    #exampleSmtpSendGames
    #simpleSmtpSendGames('smtp.gmail.com', secure.email, secure.email_pass, secure.email, gameList)
    
