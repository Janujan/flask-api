# Tweet Service 🦉

This is a minimal Flask app that can retreive public tweets through a lightweight wrapper. 

The purpose of this app is to learn about the process of deploying an app to Microsoft Azure.

You can find the application running [here](https://flask-api-jay.azurewebsites.net/metrics/KingJames) (its prepopulated to Lebron's twitter account)


## Usage:

There are two main endpoints: `metrics` and `tweets`

### `/metrics/<username:str>`

This endpoint retrieves the last 10 tweets and their corresponding [public metrics](https://developer.twitter.com/en/docs/twitter-api/metrics) made by the user (if the username exists)

**Example**:
```
https://flask-api-jay.azurewebsites.net/metrics/KingJames
```
Response:

```json
[ 
  {
    "id": "1395950846655954950", 
    "public_metrics": {
      "like_count": 135085, 
      "quote_count": 3222, 
      "reply_count": 2012, 
      "retweet_count": 12906
    }, 
    "text": "JA!"
  },
  ...
]
```
### `/tweets/<username:str>`

This endpoint retrieves the last 10 tweets made by the user (if the username exists). No metrics here.

**Example**:
```
https://flask-api-jay.azurewebsites.net/metrics/KingJames
```

Response:
```json
[
  {
    "id": "1395950846655954950", 
    "text": "JA!"
  },
  ...
]
```

## Implementation Details

 ### Caching
 Since there is a limit on free twitter developer accounts, I wanted to make sure that user's requests are cached where it makes sense. Requests made to `/tweets` and `/metrics` are cached and have a TTL for 2 minutes. The rationale here is that user's dont tweet often and its unlikely that a user has tweeted within 2 minutes of the last request. 

 User_ids are also cached for 1 day. This reduces one extra query for user_ids after the first request. Since user_ids are unlikely to change (we are beholden to Twitter here), the TTL could actually be longer.
 
 **TL:DR** There is a **2 minute** lag since the last request.

## Running This App
Since its a flask app, its relatively straight forward. You just have to clone this repo, navigate to the base directory and run the following commands:

1. install requirements

```bash
pip install requirements.txt
```

**NOTE**: There is a PipFile in place so you can use pipenv as well. 

2. Set Twitter API Key/Secret in environment variables
```bash
export API_KEY=<YOU KEY HERE SHHH>
export API_SECRET=<YOUR SECRET HERE SHHH> 
```

3. Run the flask app

```bash
flask run
```

## Next Steps
- Increase limit of tweets returned (as a parameter in the request)
- Store username to user_id translation in a database
- Allow user's to observe their own tweets if they have private accounts
- Post scheduled tweets (I hope)