/* Query 1: Display statistics for each game for seasons 1979 to 2019  */
WITH cte_stats as (
select game_id, sum(ast) ast , sum(blk) blk, sum(dreb) dreb, sum(fg3a) fg3a ,
sum(fg3m) fg3m, sum(fga) fga, sum(fgm) fgm, sum(fta) fta, sum(ftm) ftm, sum(oreb) oreb,
sum(pf) pf, sum(reb) reb, sum(stl) stl, sum(turnover) turnover from stats 
group by game_id
)
select * from cte_stats join games on cte_stats.game_id=games.game_id 
where season between 1979 and 2019;

/* Query 2: Display win/loss statistics for each game for seasons 1979 to 2019  */
select *, case when home_team_score > visitor_team_score then 'Win' else 'Loss' end home_result, 
case when home_team_score < visitor_team_score then 'Win' else 'Loss' end visitor_result
from games
where season between 1979 and 2019;

/* Query 3: Display team-level vs. other teams. for seasons 1979 to 2019  */
with cte_games as (select home_team_id, visitor_team_id,home_team_full_name, visitor_team_full_name, season,
coalesce(sum(case when home_team_score>visitor_team_score then 1 end),0) home_win, 
coalesce(sum(case when home_team_score<visitor_team_score then 1 end),0) home_loss
from games
where season between 1979 and 2019
group by home_team_id, visitor_team_id, home_team_full_name, visitor_team_full_name, season
order by 1,2,5)

select team_id, team_full_name, opponent_team_id, opponent_team, season, sum(win) win, sum(loss) opponent_win
from
(select teams.team_id, teams.team_full_name,cte_games.visitor_team_id opponent_team_id, cte_games.visitor_team_full_name opponent_team, cte_games.season, 
cte_games.home_win win, cte_games.home_loss loss
from teams join cte_games on teams.team_id=cte_games.home_team_id
union all
select teams.team_id, teams.team_full_name, cte_games.home_team_id opponent_team_id, cte_games.home_team_full_name opponent_team, cte_games.season, 
cte_games.home_loss win, cte_games.home_win loss
from teams join cte_games on teams.team_id=cte_games.visitor_team_id
order by 1,3,5) as temp_game_table
group by team_id, team_full_name, opponent_team_id, opponent_team, season
order by 1,3,5;


/* Query 4: Create view to display team-level statistics for seasons 1979 to 2019  */
create or replace view view_team_game as (

with cte_teams as(
select stats.team_id, games.season, stats.game_id, sum(ast) ast , sum(blk) blk, sum(dreb) dreb, sum(fg3a) fg3a ,
sum(fg3m) fg3m, sum(fga) fga, sum(fgm) fgm, sum(fta) fta, sum(ftm) ftm, sum(oreb) oreb,
sum(pf) pf, sum(reb) reb, sum(stl) stl, sum(turnover) turnover
from stats join teams on stats.team_id = teams.team_id join games on stats.game_id = games.game_id
where games.season between 1979 and 2019
group by stats.team_id, games.season, stats.game_id
order by 1,2,3)

select cte_teams.*, game_date, home_team_id, home_team_full_name, visitor_team_id, visitor_team_full_name, home_team_score,
visitor_team_score,
case when team_id=home_team_id then home_team_score
when team_id=visitor_team_id then visitor_team_score
end score,
case when team_id=home_team_id then home_team_full_name
when team_id=visitor_team_id then visitor_team_full_name
end team_name,
case when team_id=visitor_team_id then home_team_full_name
when team_id=home_team_id then visitor_team_full_name
end opponent_team_name,
case when team_id=home_team_id and home_team_score>visitor_team_score then 'win'
when team_id=home_team_id and home_team_score<visitor_team_score then 'loss'
when team_id=visitor_team_id and home_team_score>visitor_team_score then 'loss'
when team_id=visitor_team_id and home_team_score<visitor_team_score then 'win' 
end game_result
from cte_teams join games on cte_teams.game_id=games.game_id
order by team_id, season, game_date
)

select * from view_team_game
where game_result is not null

/* Query 5: Display win streak for seasons 1979 to 2019  */
with cte_win as(
select *
from
(select team_id, team_name, season, game_date, row_number() over(partition by team_id, season order by game_date) rownum,
game_result
from view_team_game
where game_result is not null
order by team_id, season, game_date) as temp
where game_result='win'),

cte_loss as(
select *
from
(select team_id, team_name, season, game_date, row_number() over(partition by team_id, season order by game_date) rownum,
game_result
from view_team_game
where game_result is not null
order by team_id, season, game_date) as temp
where game_result='loss'),

cte_comb as(	
select cte_win.team_id, cte_win.team_name, cte_win.season, cte_win.game_date d1, cte_win.rownum t1, cte_win.game_result r1,
coalesce (cte_loss.game_date, max(cte_win.game_date) over(partition by cte_win.team_id, cte_win.season)+1) d2,
coalesce (cte_loss.rownum, max(cte_win.rownum) over(partition by cte_win.team_id, cte_win.season)+1) t2, cte_loss.game_result r2
from cte_win left join cte_loss on cte_win.rownum<cte_loss.rownum
and cte_win.team_id=cte_loss.team_id
and cte_win.season=cte_loss.season
)

select team_id, team_name, season, min(d1) streak_start, min(t1) t_start, min_d2 streak_end, min_t2 t_end, min_t2-min(t1) streak
from
(select team_id, team_name, season, d1, t1, min(d2) min_d2, min(t2) min_t2
from cte_comb
group by team_id, team_name, season, d1,  t1) as temp_tab
group by team_id, team_name, season, min_d2, min_t2

/* Query 6: Display player-level statistics for seasons 1979 to 2019, include triple double  */
select stats.player_id, first_name||' '||last_name player_name, stats.game_id,game_date, Home_Team_Full_Name,
Visitor_Team_Full_Name, season, stat_id, ast , blk, dreb, fg3a,fg3m, fga, fgm, fta, ftm, oreb, pf, pts, 
reb, stl, turnover,
case when least(coalesce(ast,0),coalesce(pts,0), coalesce(reb,0))>=10 then 1
else 0
end triple_double
from stats join players on stats.player_id=players.player_id
join games on stats.game_id = games.game_id
where games.season between 1979 and 2019





