import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import GetOldTweets3 as got
def getTweets():
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('corona')\
                                           .setSince("2019-05-01")\
                                           .setUntil("2022-09-30")\
                                           .setMaxTweets(1000)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    textTweets = [[tweet.text] for tweet in tweets]
    return textTweets

text = ""
text_tweets = getTweets()
length= len(text_tweets)

for i in range(0,length):
    text = text_tweets[i][0]+""+text

lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

tokenized_words = word_tokenize(cleaned_text,"english")


final_words = [word for word in tokenized_words if word not in stopwords.words('english')]
emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clean_line = line.strip().replace(",", "").replace("'", "")
        if ':' in clean_line:
            word, emotion = clean_line.split(":")
            word = word.strip()
            emotion = emotion.strip()
            if word in final_words:
                emotion_list.append(emotion)
w = Counter(emotion_list)
def sentimentAnalyse(sentimentText):
    score = SentimentIntensityAnalyzer().polarity_scores(sentimentText)
    print(score)

sentimentAnalyse(cleaned_text)
fig, ax1 = plt.subplots()
ax1.bar(w.keys(),w.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()