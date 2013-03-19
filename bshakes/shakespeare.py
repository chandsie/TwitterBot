#!/usr/bin/python
import json, tweepy, random, time, os
MAX_ITERS = 100
MAX_CHARS = 140
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
consumer_key = 'YOU_CONSUMER_KEY_HERE'
consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
access_token = 'YOUR_ACCESS_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'
api = None

log_file = open('bshakes-' + time.strftime("%y-%m-%d") + '.log', 'a')
def log(mesg):
    mesg = time.strftime("%y-%m-%d[%H:%M]") + ": " + mesg + "\n"
    print(mesg)
    log_file.write(mesg)
    log_file.flush()

log("Starting new invocation.")
log("Loading lexicon.")
table = json.loads(open(CURRENT_DIR + '/table.json', 'r').read())

def construct_sent(word):
    log("\tCreating sentence.")
    if word not in table:
        return ''
    result = ''
    while word not in ['.', '!', '?']:
        if word in [',', ';', ':', "'"]:
            result = result.strip()
        result += word + ' '
        word = random.choice(table[word])

    result = (result[0].upper() + result[1:]).strip() + word
    log("\tCreated sentence: " + result)
    return result

def shake_it_up():
    log("Finding regular tweet to send.")
    tweet_text = construct_sent(random.choice(table['.']))
    iters = 0
    while len(tweet_text) >= MAX_CHARS and iters < MAX_ITERS:
        log("\tRejected tweet: " + tweet_text)
        tweet_text = construct_sent(random.choice(table['.']))
        iters += 1
    if len(tweet_text) >= MAX_CHARS:
        log("\tUnable to find tweets. #faileth")
        api.update_status('I shall attempteth once more in 15eth minutes to entertaineth you whoresons. #faileth')
    else:
        log("\tSending tweet: " + tweet_text)
        api.update_status(tweet_text)
    return

def shake_back(tweet, reply_handle, reply_id):
    log("Fnding @tweet reply to send.")
    mention_words = tweet.split()[1:]
    tweet_text = ''
    for word in mention_words:
        tweet_text = construct_sent(word)
        if len(tweet_text) > 0:
            log("\tFound start word: " + word)
            break;
        log("\tRejected start word: " + word)
    iters = 0
    tweet_text = reply_handle + " " + tweet_text
    while len(tweet_text) >= MAX_CHARS and iters < MAX_ITERS:
        log("\tRejected tweet: " + tweet_text)
        tweet_text = reply_handle + " " + construct_sent(word)
        iters += 1
    if len(tweet_text) >= MAX_CHARS or len(tweet_text) == len(reply_handle) + 1:
        log("\tUnable to find tweets. #faileth")
        api.update_status(reply_handle + ' Thou hast me stumped, thou cockered flap-mouthed strumpet. #damnethyou', in_reply_to_status_id=reply_id)
    else:
        log("\tSending tweet: " + tweet_text)
        api.update_status(tweet_text, in_reply_to_status_id=reply_id)
    return

def main():
    log("Authenticating.")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    global api
    api = tweepy.API(auth)

    log("Restoring context data.")
    ld = json.loads(open(CURRENT_DIR + '/loop_data.json', 'r').read())
    last_tweet_time = ld[0]
    last_reply = ld[1]

    if (time.time() - last_tweet_time) > 900:
        log("About to send out regular tweet.")
        shake_it_up()
        last_tweet_time = time.time()
        open(CURRENT_DIR + '/loop_data.json', 'w').write(json.dumps([last_tweet_time, last_reply]))
    try:
        log("Getting mention list.")
        mentions = api.mentions_timeline(since_id = last_reply)
        if mentions:
            log("\tProcessing list.")
        else:
            log("\tNone found.")
        for mention in mentions:
            last_reply = mention.id
            open(CURRENT_DIR + '/loop_data.json', 'w').write(json.dumps([last_tweet_time, last_reply]))
            user_handle = u'@' + mention.user.screen_name
            log("\tReplying to direct tweet from " + user_handle)
            shake_back(mention.text , user_handle, last_reply)
    except Exception as e:
        log("!!!Exception occurred while processing mentions: " + str(e.message))
        pass
    log("Done. Now Exiting.\n\n")

main()
