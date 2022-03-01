# NBA Data Visualization

**Summary**
---
In This project I attempt to retrieve all NBA-related data such as players, teams, games, game statistics since the 1979 season. Data is collected from the free API at https://www.balldontlie.io/#introduction. The API is constantly updated with current game data up to and including the current 2021 season. For this project, I will focus on seasons 1979 through 2019. I use Python to extract data from the API, clean the data and insert the data into a PostgreSQL database. Once all data is stored in the PostgreSQL database, I perform various queries from the database and import the results to Tableau Public to create an interactive dashboard.

**Tableau Dashboard**
---
Please check out the dashboard at https://public.tableau.com/views/NBADashboard_16444836938170/Dashboard1TeamStatistics?:language=en-US&:display_count=n&:origin=viz_share_link

* Here are some screenshots
![](img/Dashboard_1_Team_Statistics.png)
![](img/Dashboard_2_Player_Statistics.png)

**Step 1: Data Preparation**
---
* [data_preparation.py](https://github.com/RonaldLi-GitHub/NBA_Data_Visualization/blob/main/data_preparation.py) contains the code for this section
* The free API is at https://www.balldontlie.io/#introduction
* The script retrieves data from the following 4 sections
  * Players-all players with attributes such as name, player id, current team or last team for players who are retired
  * Teams-all teams with attributes such as team id, team name, city, conference, division
  * Games-all games with one record per game, each record contains game id, season, home team, visitor team, scores
  * Stats-all stats for all games with one record per stat per player, each record contains stat id, player id, team id, game id, ast, reb, pts and other stats
* Each section of data is of json format. The json files are then converted and stored in a dataframe. Player, Team, Game data are exported to csv files. Stat data is exported to a pickle file due to its size

**Step 2: Set up PostgreSQL Database and Create Tables**
---
* [create_tables.py](https://github.com/RonaldLi-GitHub/NBA_Data_Visualization/blob/main/create_tables.py) contains the code for this section
* For this project, I create a PostgreSQL Database locally using pgAdmin 4. After creating the database, I recorded the hostname/database/username/port_id
* I create a table for each of Players/Teams/Games/Stats, each with its primary id and/or foreign id
* The ERD diagram is the following
 ![](img/ERD_diagram.JPG)
 
**Step 3: Insert Data into PostgreSQL Database**
---
* [insert_data.py](https://github.com/RonaldLi-GitHub/NBA_Data_Visualization/blob/main/insert_data.py) contains the code for this section
* This section inserts Players/Teams/Games/Stats dataframes into the cooresponding table in the database

**Step 4: Perform SQL Queries for Data Visualization**
---
* [queries_for_visualization.sql](https://github.com/RonaldLi-GitHub/NBA_Data_Visualization/blob/main/queries_for_visualization.sql) contains the queries used for the Tableau dashboard
* Query 1: Display statistics for each game for seasons 1979 to 2019
  * This generates the average game statistics for each season, such as average ast/reb/pts per game
* Query 2: Display win/loss statistics for each game for seasons 1979 to 2019
  * This generates win/loss record for each team, but this table makes a distinct between which team is the home team and which is the visitor team
* Query 3: Display team-level vs. other teams. for seasons 1979 to 2019
  * This generates win/loss record for each team, but this table contains aggregate results that combine home/visitor position. The user can select any one team and another team to see their win/loss history for any given season
* Query 4: Create view to display team-level statistics for seasons 1979 to 2019
  * This creates the view that will be used in Query 5. This contains team-level statistics regardless of home/visitor position
* Query 5: Display win streak for seasons 1979 to 2019
  * This returns the longest winning streak for each team and each season. A winning streak is the number of consecutive wins until the first loss. Season end will reset the streak. Thus, if the last game is a win, it will still count towards a streak
* Query 6: Display player-level statistics for seasons 1979 to 2019, include triple double
  * This generates player-level statistics for each game and each season

**Step 5: Upload all Query Results to Tableau Public for Dashboard**
---
* The user is able to visualize the following
  * Win/loss record for any two teams and for any season (can select multiple seasons)
  * Average game statistics per season 
  * Win/loss record for each team for any season
  * Longest winning streak for each team for any season
  * Top 10 players for each season in total ast/reb/pts, average ast/reb/pts, number of triple double

