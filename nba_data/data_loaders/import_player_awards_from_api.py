import io
import pandas as pd
import requests
from nba_api.stats.endpoints import playerawards
from nba_api.stats.static import players
import time

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def fetch_player_awards(player_id, player_name):
    try:
        awards = playerawards.PlayerAwards(player_id=player_id)
        awards_data = awards.get_data_frames()[0] 
        awards_data['PlayerID'] = player_id
        awards_data['PlayerName'] = player_name
        return awards_data
    except Exception as e:
        print(f"Could not fetch awards for player {player_name} ({player_id}): {e}")
        return pd.DataFrame()

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    all_players = players.get_players()

    # Initialize an empty list to store the awards dataframes
    all_awards = []

    # Iterate over each player and fetch their awards
    for i, player in enumerate(all_players):
        player_id = player['id']
        player_name = player['full_name']
        
        awards_df = fetch_player_awards(player_id, player_name)
        
        if not awards_df.empty:
            all_awards.append(awards_df)
        
        # Sleep to prevent hitting the rate limit
        time.sleep(0.5)
        
        # Print progress
        if (i + 1) % 50 == 0 or (i + 1) == len(all_players):
            print(f"Processed {i + 1}/{len(all_players)} players")

    # Concatenate all awards dataframes into one
    if all_awards:
        all_awards_df = pd.concat(all_awards, ignore_index=True)
        print(all_awards_df)
    else:
        print("No awards data found.")

    return all_awards_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
