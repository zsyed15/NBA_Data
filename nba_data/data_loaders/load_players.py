import io
import pandas as pd
import requests
from nba_api.stats.static import players
from pyspark.sql import SparkSession
import json

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load Players from NBA Players API using PySpark
    """
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("NBA Players Data Load") \
        .getOrCreate()

    # Get players data from API
    p = players.get_players()

    # Convert the list of players to JSON strings for Spark
    players_json = [json.dumps(player) for player in p]

    # Create a Spark DataFrame from the JSON strings
    df = spark.read.json(spark.sparkContext.parallelize(players_json))
    df.show()
    return 'test'


@test
def test_output(output, *args) -> None:
    assert output is not None
