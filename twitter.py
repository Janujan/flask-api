import requests
import os
from requests.auth import HTTPBasicAuth
from functools import lru_cache

api_key = os.environ['API_KEY'] 
api_secret = os.environ['API_SECRET'] 
auth = HTTPBasicAuth(api_key, api_secret)

def retrieve_token():
    response = requests.post('https://api.twitter.com/oauth2/token', params={'grant_type': 'client_credentials'}, auth=auth)
    response.raise_for_status()
    return response.json()['access_token']

def get_user_id(username, token):
    response = requests.get(f'https://api.twitter.com/2/users/by/username/{username}', headers = {"Authorization": f"Bearer {token}"})
    return response.json()['data']['id']

@lru_cache
def get_user_tweets(username, token):
    user_id = get_user_id(username, token)
    response = requests.get(f'https://api.twitter.com/2/users/{user_id}/tweets', headers = {"Authorization": f"Bearer {token}"})
    return response.json()['data']

@lru_cache
def get_metrics_for_tweets(username, token):
    tweets = get_user_tweets(username, token)
    tweet_ids = [tweet['id'] for tweet in tweets]
    response = requests.get(f'https://api.twitter.com/2/tweets', params={'ids':','.join(tweet_ids), 'tweet.fields':['public_metrics']} ,headers = {"Authorization": f"Bearer {token}"})
    return response.json()['data']