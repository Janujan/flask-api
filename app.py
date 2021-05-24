from flask import Flask
from flask import jsonify
from flask import g #holds information on the request context
from flask_caching import Cache
import pandas
import requests
import twitter
import time
import json

app = Flask(__name__)

cache_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
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

@app.route("/metrics/<string:username>")
@cache.memoize(timeout=120)
def metric_lookup(username):
    token = twitter.retrieve_token()
    return jsonify(twitter.get_metrics_for_tweets(username, token))

@app.route("/tweets/<string:username>")
@cache.memoize(timeout=120)
def tweet_lookup(username):
    token=twitter.retrieve_token()
    return jsonify(twitter.get_user_tweets(username, token))

@app.route("/")
def hello():
    return "welcome to the NBA player tracker"

@app.route("/jokes")
def test():
    return requests.get('https://v2.jokeapi.dev/joke/Any').json()