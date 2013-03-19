TwitterBot
==========

Twitter Bots! (Run on a raspberry pi)

All of these are run using cronjobs on a raspberry pi. JSON output is used to store the lexicon and last tweet/last reply data.

 - [@BillyShakesDoe](https://twitter.com/BillyShakesDoe): Tweets a random shakespearean sentence every 15 minutes. Replies to tweets every minute with a shakespearean sentence that starts with the same first word as the tweet.
   * Crontab entry: * * * * * /absolute/path/to/shakespeare.py
   * Algorithm for finding sentence:
     1. Pick a random word from the set of words that Shakespeare ever wrote after a period. (i.e. the set of all words that Shakespeare ever used to start a sentence.) Place this word into the sentence string.
     2. Pick a random word from the set of words that Shakespeare ever use after the previous word and place this word into the sentence string.
     3. Repeat step 2 until you encounter a period, exclamation or question mark.
     4. Ensure that the first word is capitalized and spaces have been trimmed. Throughout the process, ensure that spaces are correctly inserted/removed if commas, semicolons and colons are encountered.
     5. If found sentene is less than or equal to 140 characters long, tweet it. Otherwise, repeat the above steps. Keep doing this for at most 100 tries. Tweet out an apology if you fail after 100 tries.
   * Algorithm for replying to tweets:
     1. Read a word from the tweet until it can be used as the first word for the above algorithm. Tweet it out if it works. If all words are exhausted without coming up with a reply, insult the person who tweeted at you.
   * 
