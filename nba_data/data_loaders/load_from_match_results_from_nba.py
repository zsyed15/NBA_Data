import io
import pandas as pd
from pyspark.sql import SparkSession
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import LeagueGameLog
from nba_api.stats.endpoints import commonteamyears, teamyearbyyearstats

pd.DataFrame.iteritems = pd.DataFrame.items

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def game_ids_per_season(spark, season):
    # Fetch game log data for the given season
    game_log = LeagueGameLog(season=season)
    game_log_df = game_log.get_data_frames()[0]
    
    # Convert to PySpark df
    spark_df = spark.createDataFrame(game_log_df)
    # Select unique GAME_IDs
    unique_game_ids = spark_df.select("GAME_ID").distinct().rdd.flatMap(lambda x: x).collect()
    return unique_game_ids

def get_all_seasons():
    #Fetch list of team years from NBA API
    team_years = commonteamyears.CommonTeamYears()
    team_years_data = team_years.get_data_frames()[0]

    team_ids = team_years_data['TEAM_ID'].unique()

    unique_seasons = set()

    # Fetch year-by-year stats for each team to infer seasons
    for team_id in team_ids:
        team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
        team_stats_data = team_stats.get_data_frames()[0]
        unique_seasons.update(team_stats_data['YEAR'].unique())
    unique_seasons_list = sorted(unique_seasons)
    return unique_seasons_list


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Loads data from nba api as collecion of spark dataframes
    """
    spark = SparkSession.builder \
    .appName("NBA Game IDs per Season") \
    .getOrCreate()

    #(box_score,matchup)
    dfs = []
    # seasons_list = get_all_seasons()
    seasons_list = [['2022-23', '2023-24']]
    i = 0
    for season in seasons_list:
        game_ids = game_ids_per_season(spark,season)
        for game_id in game_ids:
            i += 1
            traditional_boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            traditional_data = traditional_boxscore.get_data_frames()
            
            box_score =  spark.createDataFrame(traditional_data[0])
            match_outcome = spark.createDataFrame(traditional_data[1])

            dfs.append((box_score.collect(),match_outcome.collect()))
    return dfs
    #return pd.read_csv(io.StringIO(response.text), sep=',')


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
