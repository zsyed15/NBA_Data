import io
import pandas as pd
import requests
from nba_api.stats.endpoints import franchiseplayers

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_players_per_team_from_nba_api(*args, **kwargs):
    """
    Load Data of players who have played for each NBA_Team
    """
    team_ids = args[0]['id'].unique()
    #List of dataframese that have all players that have played for each team
    dfs = []

    for team_id in team_ids:
        
        fp = franchiseplayers.FranchisePlayers(team_id)
        fp_df = fp.get_dict()['resultSets'][0]

        df = pd.DataFrame(fp_df['rowSet'],columns = fp.get_dict()['resultSets'][0]['headers'])
        
        dfs.append(df)
    
    team_and_players_df = pd.concat(dfs, ignore_index=True)
    
    return team_and_players_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
