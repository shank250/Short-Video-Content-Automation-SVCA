# intehrating tweeter api
import tweepy
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

api_key_twitter = config['twitter']['api_key']
api_key_secret_twitter = config['twitter']['api_key_secret']
access_token_twitter = config['twitter']['access_token']
access_token_secret_twitter = config['twitter']['access_token_secret']
# print(access_token_secret)
# print(access_token)
# print(api_key_secret)
# print(api_key)
auth = tweepy.OAuthHandler(api_key_twitter, api_key_secret_twitter)
auth.set_access_token(access_token_twitter,access_token_secret_twitter)

api =  tweepy.API(auth)
tweet_text = "Hello, Twitter! This is my first tweet using the Twitter API v2."
api.update_status(tweet_text)

print("Tweet sent successfully!")
# public_tweets = api.home_timeline()
# print(public_tweets)


api_key_openai = config['openai']['api_key']

