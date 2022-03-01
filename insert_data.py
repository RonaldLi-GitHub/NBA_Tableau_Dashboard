from sqlalchemy import create_engine
import psycopg2
import os 
import pandas as pd

def insert_data():
    hostname='localhost'
    database='NBAdb'
    username='postgres'
    pwd='admin'
    port_id=5432

    conn_url= "postgres://{}:{}@{}:{}/{}".format(username, pwd, hostname, port_id, database)
    engine=create_engine(conn_url)
    conn=engine.connect()

    df_game=pd.read_csv("df_game.csv")
    df_game.columns= df_game.columns.str.lower()
    df_team=pd.read_csv("df_team.csv")
    df_team.columns= df_team.columns.str.lower()
    df_player=pd.read_csv("df_player.csv")
    df_player.columns= df_player.columns.str.lower()
    df_stat=pd.read_pickle("df_stat.pkl")
    df_stat=df_stat.drop(["min", "fg3_pct", "fg_pct", "ft_pct"], axis=1)
    df_stat=df_stat.rename(columns={"id":"stat_id"})
    df_stat.columns= df_stat.columns.str.lower()
    df_team.to_sql('teams', con=conn, if_exists='append', index=False)
    df_player.to_sql('players', con=conn, if_exists='append', index=False)
    df_game.to_sql('games', con=conn, if_exists='append', index=False)
    df_stat.to_sql('stats', con=conn, if_exists='append', index=False)
    conn.close()

if __name__ == '__main__':
    insert_data()