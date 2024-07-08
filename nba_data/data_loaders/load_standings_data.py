import io
import pandas as pd
from nba_api.stats.endpoints import leaguestandings
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    standings_dfs = []

    seasons = range(1960, 2024)

    for season_year in seasons:
        standings = leaguestandings.LeagueStandings(season=season_year)
        standings_df = standings.get_data_frames()[0] 
        standings_df['Season'] = season_year  # Add a column for the season year
        standings_dfs.append(standings_df)

    # Concatenate all dataframes into one big dataframe
    all_standings_df = pd.concat(standings_dfs, ignore_index=True)
    return all_standings_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
