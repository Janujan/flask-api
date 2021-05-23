from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import commonallplayers
from flask import Flask
import pandas

app = Flask(__name__)



@app.route("/playerSearch/<string:playername>")
def player(playername):
        # populate player dictionary to map ids to player names
    players = commonallplayers.CommonAllPlayers(is_only_current_season=1)
    player_list = players.data_sets[0].data['data']
    player_dict = {}

    for player in player_list:
        # sixth element contains name in lower case, no puncation
        player_dict[player[6]] = player[0]
        
    convert_query = str.lower('_'.join(playername.split(' ')))

    if convert_query in player_dict.keys():
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_dict[convert_query])
        return player_info.get_data_frames()[0].to_dict(orient='records')[0]
    return "Player not found :("

@app.route("/")
def hello():
    return "welcome to the NBA player tracker"