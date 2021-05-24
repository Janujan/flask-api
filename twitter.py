import requests
import os
from requests.auth import HTTPBasicAuth
import errors
api_key = os.environ['API_KEY'] 
api_secret = os.environ['API_SECRET'] 

base_url = 'https://api.twitter.com'
oauth_url = base_url + '/oauth2/token'
token = None

def retrieve_token(user_key:str=None, user_secret:str=None) -> None:
    auth = HTTPBasicAuth(user_key or api_key, user_secret or api_secret)
    response = requests.post(oauth_url, params={'grant_type': 'client_credentials'}, auth=auth)
    response.raise_for_status()
    return response.json()['access_token']

def get_user_id(username:str) -> list:
    response = requests.get(base_url + f'/2/users/by/username/{username}', headers = {"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    response = response.json()
    if response.get('errors'):
        raise errors.UserNotFoundError
    return response.json()['data']['id']

def get_user_tweets(user_id:str) -> list:
    response = requests.get(base_url + f'/2/users/{user_id}/tweets', headers = {"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()['data']

def get_metrics_for_tweets(user_id:str) -> list:
    tweets = get_user_tweets(user_id)
    tweet_ids = [tweet['id'] for tweet in tweets]
    response = requests.get(base_url + f'/2/tweets', params={'ids':','.join(tweet_ids), 'tweet.fields':['public_metrics']} ,headers = {"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()['data']