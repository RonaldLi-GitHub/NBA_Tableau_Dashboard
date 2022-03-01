import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import date
import time
import pickle

#This is the link to the API that prvides data on NBA
url="https://www.balldontlie.io/api/v1/"

#Get player data 
def get_player_data():
    df_player=pd.DataFrame()
    player_vars=["id", "first_name", "last_name", "position"]
    team_vars=["abbreviation", "city", "conference", "division", "full_name", "name"]
    for i in range(38):
        response_player=requests.get(url+"players?per_page=100&page="+str(i+1)).json()
        for player in response_player["data"]:
            for var in player_vars:
                globals()[var]=player[var]
            team_id=player["team"]["id"]
            for var in team_vars:
                globals()[var]=player["team"][var]
            player_dict={ x:globals()[x] for x in player_vars+team_vars }
            player_dict["team_id"]=team_id
            df_player=df_player.append(player_dict, ignore_index=True )
            player_dict.clear()
    df_player=df_player.astype({"id":int, "team_id":int})
    df_player=df_player.rename(columns={"id": "player_id"})
    df_player.to_csv("df_player.csv", index=False)

#Get team data 
def get_team_data():
    df_team=pd.DataFrame()
    team_vars=["id","abbreviation", "city", "conference", "division", "full_name", "name"]
    response_team=requests.get(url+"teams").json()
    for team in response_team["data"]:
        for var in team_vars:
                globals()[var]=team[var]
        team_dict={ x:globals()[x] for x in team_vars}
        df_team=df_team.append(team_dict, ignore_index=True)
        team_dict.clear()
    df_team=df_team.astype({"id":int})
    df_team=df_team.rename(columns={"id": "team_id"})
    df_team.to_csv("df_team.csv", index=False)

#Get game data 
def get_game_data():
    df_game=pd.DataFrame()
    game_vars=["id", "date", "home_team_score", "period", "postseason", "season", "status", "visitor_team_score"]
    for i in range(1):
        if (i+1)%60==0:
            time.sleep(60)
        response_game=requests.get(url+"games?per_page=100&page="+str(i+1)).json()
        for game in response_game["data"]:
            for var in game_vars:
                globals()[var]=game[var]
            home_team_id=game["home_team"]["id"]
            visitor_team_id=game["visitor_team"]["id"]
            game_dict={ x:globals()[x] for x in game_vars}
            game_dict["home_team_id"]=home_team_id
            game_dict["visitor_team_id"]=visitor_team_id
            df_game=df_game.append(game_dict, ignore_index=True )
            game_dict.clear()
    def get_date(entry):
        return entry.split("T")[0]
    df_game=df_game.astype({"id":int, "home_team_id":int, "visitor_team_id":int, "home_team_score":int, "visitor_team_score":int,
                        "period":int, "postseason":int, "season":int })
    df_game=df_game.rename(columns={"id": "game_id", "date":"game_date"})
    df_game["game_date"]=df_game["game_date"].apply(get_date)
    df_game.to_csv("df_game.csv", index=False)


#Get game stats data
def get_stats_data():
    df_stat=pd.DataFrame()
    stat_vars=["id", "ast", "blk", "dreb", "fg3_pct", "fg3a", "fg3m", "fg_pct", "fga", "fgm", "ft_pct", "fta", "ftm", "min",
            "oreb", "pf", "pts", "reb", "stl", "turnover"]
    for i in range(11352):
        response_stat=requests.get(url+"stats?per_page=100&page="+str(i+1)).json()
        for stat in response_stat["data"]:
            for var in stat_vars:
                globals()[var]=stat[var]
            game_id=stat["game"]["id"]
            if stat.get("player", np.nan) is None:
                player_id= np.nan
            else:
                player_id=stat["player"]["id"]
            team_id=stat["team"]["id"]
            stat_dict={ x:globals()[x] for x in stat_vars }
            stat_dict["game_id"]=game_id
            stat_dict["player_id"]=player_id
            stat_dict["team_id"]=team_id
            df_stat=df_stat.append(stat_dict, ignore_index=True )
            stat_dict.clear()
    df_stat.to_pickle('df_stat.pkl')

if __name__ == '__main__':
    get_player_data()
    get_team_data()
    get_game_data()
    get_stats_data()



