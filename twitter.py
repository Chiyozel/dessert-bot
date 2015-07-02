# coding: utf8
import base64
import logging
import time
import json

import oauth2 as oauth

import httplib2

import urllib

import twitter_settings

class TwitterError(Exception):
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content
    def __str__(self):
        return "Twitter returned " + str(self.status_code) + " : " + self.content


def get_mentions(since=-1):
    client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
    
    if since > -1:
        resp, content = client.request("https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=800&since_id=" + str(since), "GET")
    else:
        resp, content = client.request("https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=200", "GET")
    
    if resp.status != 200:
        raise TwitterError(resp.status, content)
    
    return json.loads(content)

def get_tweets(screen_name, auth=True):
    if auth:
        client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
    else:
        client = httplib2.Http(timeout=30)
    
    
    resp, content = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=' + screen_name + '&count=800&trim_user=true', "GET")
    
    if resp.status != 200:
        raise TwitterError(resp.status, content)
    
    return json.loads(content)

def get_timeline_tweets(count):
    client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
    
    resp, content = client.request('https://api.twitter.com/1.1/statuses/home_timeline.json?count=' + str(count), "GET")
    
    if resp.status != 200:
        raise TwitterError(resp.status, content)
    
    return json.loads(content)

def get_timeline_tweets_since(since_id=-1):
    client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
    tweets = []
    
    if since_id < 0:
        resp, content = client.request('https://api.twitter.com/1.1/statuses/home_timeline.json', "GET")
        
        if resp.status != 200:
            raise TwitterError(resp.status, content)
        
        tweets.extend(json.loads(content))
    else:
        # TODO 1 or 0?
        current_page = 0
        while len(tweets) == 0 or not since_id >= max(map(lambda t:int(t['id']), tweets)):
            resp, content = client.request('https://api.twitter.com/1.1/statuses/home_timeline.json?count=800&page=' + str(current_page), "GET")
            new_tweets = json.loads(content)
            if len(new_tweets) == 0:
                break
            tweets.extend(new_tweets)
            current_page += 1
    
    return tweets

def post_tweet(text, replyID = None, mediaID = None):
	args = [("status", unicode(text).encode('utf-8'))]
	
	if replyID != None : args.append(("in_reply_to_status_id", replyID))
	if mediaID != None : args.append(("media_ids", mediaID))

	urlArgs = urllib.urlencode(args)

	client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
	resp, content = client.request("https://api.twitter.com/1.1/statuses/update.json", "POST", urlArgs)
	
	if resp.status != 200:
		raise TwitterError(resp.status, content)
	
	return content
	
def post_photo(text, imagePath, replyID = None):
	file = open(imagePath, 'rb')
	data = base64.b64encode(file.read())
	
	urlArgs = urllib.urlencode([("media_data", data)])
	
	client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
	resp, content = client.request("https://upload.twitter.com/1.1/media/upload.json", "POST", urlArgs)
	
	if resp.status != 200:
		raise TwitterError(resp.status, content)
	
	return post_tweet(text, replyID, json.loads(content)['media_id_string'])
	
def retweet_tweet(idTweet):
	print(idTweet)
	client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
	resp, content = client.request("https://api.twitter.com/1.1/statuses/retweet/{}.json".format(idTweet), "POST")
	if resp.status != 200:
		raise TwitterError(resp.status, content)
	
	return json.loads(content)
		
def search_tweet(text, nombreTweets = 1):
	urlArgs = urllib.urlencode([("q", unicode(text).encode('utf-8')),("count",nombreTweets)])
	
	client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
	resp, content = client.request("https://api.twitter.com/1.1/search/tweets.json?{}".format(urlArgs), "GET")
	
	if resp.status != 200:
		raise TwitterError(resp.status, content)
	
	return json.loads(content)
	
def follow_user(screen_name):
    client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
    resp, content = client.request("https://api.twitter.com/1.1/friendships/create.json", "POST", urllib.urlencode([("screen_name", screen_name)]))
    
    # TODO Check status code
    
    return content

def get_rate_limit_status(auth=True):
    if auth:
        client = oauth.Client(twitter_settings.consumer, twitter_settings.token)
    else:
        client = httplib2.Http(timeout=30)
    resp, content = client.request('https://api.twitter.com/1.1/application/rate_limit_status.json', "GET")
    
    return json.loads(content)
