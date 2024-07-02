import io
import pandas as pd
import requests
from nba_api.stats.static import players

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
   Load Players from NBA Players API 
    """
    p = players.get_players()
    df = pd.DataFrame(p)
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None
