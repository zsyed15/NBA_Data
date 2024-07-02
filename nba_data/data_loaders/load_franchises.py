from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_teams_from_google_cloud_storage(*args, **kwargs):
    """
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    bucket_name = kwargs['bucket_name']
    folder_name = kwargs['folder_name']
    team_object = kwargs['team_path']
    player_object = kwargs['player_path']
    team_path = f'{folder_name}/{team_object}.parquet'
    player_path = f'{folder_name}/{player_object}.parquet'

    team_names = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        team_path,
    )

    return team_names


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
