#!/usr/bin/python
import tweepy, os
from datetime import datetime

MAX_ITERS = 100
MAX_CHARS = 140
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
consumer_key = 'YOU_CONSUMER_KEY_HERE'
consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
access_token = 'YOUR_ACCESS_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'
api = None
MUSIC_LONG = '♫ ♪ ♫ DING DONG DONG DING DING DING ♫ ♪ ♫'
MUSIC = '♫ ♪ ♫ DING DONG DING ♫ ♪ ♫'

log_file = open('campanile-' + time.strftime("%y-%m-%d") + '.log', 'a')
def log(mesg):
    mesg = time.strftime("%y-%m-%d[%H:%M]") + ": " + mesg + "\n"
    print(mesg)
    log_file.write(mesg)
    log_file.flush()

def main():
    log("Authenticating.")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    global api
    api = tweepy.API(auth)

    dtime = datetime.now()
    if dtime.weekday() == 6:
        # Chime from 2 to 2:45
        if dtime.hour == 14:
            if dtime.minute == 0:
                api.update_status(MUSIC_LONG)
            elif dtime.minute <= 44:
                api.update_status(MUSIC)
            elif dtime.minute == 45:
                api.update_status(MUSIC_LONG)

    elif dtime.weekday() == 5:
        # Chime from 12 to 12:15
        if dtime.hour == 12:
            if dtime.minute == 0:
                api.update_status(MUSIC_LONG)
            elif dtime.minute <= 14:
                api.update_status(MUSIC)
            elif dtime.minute == 15:
                api.update_status(MUSIC_LONG)
        # Chime from 6 to 6:10
        elif dtime.hour == 18:
            if dtime.minute == 0:
                api.update_status(MUSIC_LONG)
            elif dtime.minute <= 9:
                api.update_status(MUSIC)
            elif dtime.minute == 10:
                api.update_status(MUSIC_LONG)
    else:
        # Chime from 7:50 to 8
        if dtime.hour == 7:
            if dtime.minute == 50:
                api.update_status(MUSIC_LONG)
            elif 50 < dtime.minute <= 59:
                api.update_status(MUSIC)
        elif dtime.hour == 8 and dtime.minute == 0:
            api.update_status(MUSIC_LONG)
        # Chime from 12 to 12:10
        elif dtime.hour == 12:
            if dtime.minute == 0:
                api.update_status(MUSIC_LONG)
            elif dtime.minute <= 9:
                api.update_status(MUSIC)
            elif dtime.minute == 10:
                api.update_status(MUSIC_LONG)
        # Chime from 6 to 6:10
        elif dtime.hour == 18:
            if dtime.minute == 0:
                api.update_status(MUSIC_LONG)
            elif dtime.minute <= 9:
                api.update_status(MUSIC)
            elif dtime.minute == 10:
                api.update_status(MUSIC_LONG)

    if 8 <= dtime.hour <= 22 and dtime.minute == 0:
        # Chime hour times
        curr_hour = dtime.hour
        if curr_hour > 12:
            curr_hour = curr_hour - 12
        api.update_status(('DONG ' * curr_hour).strip())
    log("Tweeting.")

    # api.update_status("An' they're hangin' Danny Deever in the mornin'.")
    log("Done. Now Exiting.\n")

log("Starting.")
main()
