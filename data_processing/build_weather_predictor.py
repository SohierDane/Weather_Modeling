"""

"""

from __future__ import division
import pandas as pd
import numpy as np
import os
import weather_mod_utilities
import get_dist_tables
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from time import time
from get_constants import get_project_constants


if __name__ == "__main__":
    config = get_project_constants()
    metadata_path = config['GSOD_METADATA_PATH']
    processed_data_path = config['PROCESSED_GROUND_STATION_DATA_PATH']
    df = weather_mod_utilities.load_metadata_for_active_stns(
        metadata_path, country_code='AS')
    Y_stations = df.sample(frac=0.1, random_state=42)
    X_stations = df[~df.ID.isin(Y_stations.ID)]
    Y_stations = get_neighbor_data(Y_stations, X_stations)

    """
    for station in y_stations:
        append weather data from all days where all nearest neighbors have data
        to a central dataframe
    test_train split on central dataframe
    model central dataframe
    """
