import io
import pandas as pd
from nba_api.stats.endpoints import LeagueLeaders
from nba_api.stats.endpoints import commonteamyears, teamyearbyyearstats

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

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
    Template for loading data from API
    """
    seasons = get_all_seasons()[50:]
    
    stat_categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'FT_PCT']

    # Initialize an empty list to store dataframes
    league_leaders_dataframes = []

    # Iterate over seasons and statistical categories
    for season in seasons:
        for stat in stat_categories:
            # Fetch league leaders data for the specified season and statistical category
            league_leaders = LeagueLeaders(season=season)
            league_leaders_df = league_leaders.get_data_frames()[0]
            
            # Add season and stat category as additional columns
            league_leaders_df['SEASON'] = season
            league_leaders_df['STAT_CATEGORY'] = stat
            
            # Append the dataframe to the list
            league_leaders_dataframes.append(league_leaders_df)

    # Concatenate all dataframes into a single dataframe
    all_league_leaders_df = pd.concat(league_leaders_dataframes, ignore_index=True)
    return all_league_leaders_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
