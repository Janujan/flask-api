from flask import Flask
from flask import jsonify
from flask import g #holds information on the request context
from flask_caching import Cache
import pandas
import requests
import twitter
import time
import json
import errors

app = Flask(__name__)

cache_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 86400 # one day
}

app.config.from_mapping(cache_config)

cache = Cache(app)

@app.before_request
def before_request():
    g.start = time.time()

@app.teardown_request
def after_request(exception):
    end = time.time() - g.start
    print(f'time elapsed for request : {end}')
    # print(cache.cache._cache)

@app.route("/metrics/<string:username>", methods=['GET'])
@cache.memoize(timeout=120)
def metric_lookup(username:str):
    twitter.token =  twitter.retrieve_token()
    user_id = get_user_id(username)
    return jsonify(twitter.get_metrics_for_tweets(user_id))

@app.route("/tweets/<string:username>", methods=['GET'])
@cache.memoize(timeout=120)
def tweet_lookup(username:str):
    twitter.token =  twitter.retrieve_token()
    user_id = get_user_id(username)
    return jsonify(twitter.get_user_tweets(user_id))

@cache.memoize()
def get_user_id(username:str):
    return twitter.get_user_id(username)

@app.route("/", methods=['GET'])
def hello():
    return "Welcome to Jay's tweet service! For more info on how to use this API, check out the repo : https://github.com/Janujan/flask-api"

@app.route("/jokes", methods=['GET'])
def test():
    return requests.get('https://v2.jokeapi.dev/joke/Any').json()

@app.errorhandler(errors.UserNotFoundError)
def handle_user_not_found(error):
    return "Uh-oh, that username doesn't exist!", 404

@app.errorhandler(requests.HTTPError)
def handle_bad_request(error):
    return "Bad Request To Twitter!", 400