import psycopg2
import os 

def create_tables():
    hostname='localhost'
    database='NBAdb'
    username='postgres'
    pwd='admin'
    port_id=5432


    conn=psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
    cur = conn.cursor()
    create_table_cmd = (
                    """CREATE TABLE IF NOT EXISTS teams
                    (
                        Team_ID INTEGER PRIMARY KEY, 
                        Team_Full_Name VARCHAR(30), 
                        Team_Name VARCHAR(30),
                        Team_Abbr VARCHAR(30),
                        Team_City VARCHAR(30),
                        Team_Conf VARCHAR(30),
                        Team_Div VARCHAR(30)
                    )
                    """,
                    """CREATE TABLE IF NOT EXISTS players
                    (
                        Player_ID INTEGER PRIMARY KEY, 
                        First_Name VARCHAR(30), 
                        Last_Name VARCHAR(30),
                        Current_Team_ID INTEGER,
                        Current_Team_Full_Name VARCHAR(30),
                        Current_Team_Name VARCHAR(30),
                        Position VARCHAR(30),
                        Current_Team_Abbr VARCHAR(30),
                        Current_Team_City VARCHAR(30),
                        Current_Team_Conf VARCHAR(30),
                        Current_Team_Div VARCHAR(30),
                        FOREIGN KEY (Current_Team_ID)
                        REFERENCES teams (Team_ID)
                        ON UPDATE CASCADE ON DELETE CASCADE
                    )
                    """ ,
                    """CREATE TABLE IF NOT EXISTS games
                    (
                        Game_Date DATE, 
                        Game_ID INTEGER PRIMARY KEY,
                        Home_Team_Abbr VARCHAR(30), 
                        Home_Team_City VARCHAR(30),
                        Home_Team_Conf VARCHAR(30),
                        Home_Team_Div VARCHAR(30),
                        Home_Team_Full_Name VARCHAR(30),
                        Home_Team_ID INTEGER,
                        Home_Team_Name VARCHAR(30),
                        Home_Team_Score INTEGER,
                        Period INTEGER,
                        Postseason INTEGER,
                        Season INTEGER,
                        Status VARCHAR(30),
                        Visitor_Team_Abbr VARCHAR(30), 
                        Visitor_Team_City VARCHAR(30),
                        Visitor_Team_Conf VARCHAR(30),
                        Visitor_Team_Div VARCHAR(30),
                        Visitor_Team_Full_Name VARCHAR(30),
                        Visitor_Team_ID INTEGER,
                        Visitor_Team_Name VARCHAR(30),
                        Visitor_Team_Score INTEGER,
                        FOREIGN KEY (Home_Team_ID)
                        REFERENCES teams (Team_ID)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Visitor_Team_ID)
                        REFERENCES teams (Team_ID)
                        ON UPDATE CASCADE ON DELETE CASCADE
                    )
                    """,
                    """CREATE TABLE IF NOT EXISTS stats
                    (
                        ast INTEGER, 
                        blk INTEGER, 
                        dreb INTEGER,
                        fg3a INTEGER,
                        fg3m INTEGER,
                        fga INTEGER,
                        fgm INTEGER,
                        fta INTEGER,
                        ftm INTEGER,
                        game_id INTEGER,
                        stat_id INTEGER PRIMARY KEY,
                        oreb INTEGER,
                        pf INTEGER,
                        player_id INTEGER,
                        pts INTEGER,
                        reb INTEGER,
                        stl INTEGER,
                        team_id INTEGER,
                        turnover INTEGER,
                        FOREIGN KEY (game_id)
                        REFERENCES games (Game_ID)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (player_id)
                        REFERENCES players (Player_ID)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (team_id)
                        REFERENCES teams (Team_ID)
                        ON UPDATE CASCADE ON DELETE CASCADE
                    )
                    """
                    )
    for cmd in create_table_cmd:
        cur.execute(cmd)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
