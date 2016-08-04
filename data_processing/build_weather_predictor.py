
"""
Given a weather station metadata file, plus a set of csvs
"""

from __future__ import division
import pandas as pd
import numpy as np
import os
import weather_mod_utilities
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from time import time
from get_constants import get_project_constants
from get_dist_tables import calc_dist_table


if __name__ == "__main__":
    config = get_project_constants()
    metadata_path = config['GSOD_METADATA_PATH']
    processed_data_path = config['PROCESSED_GROUND_STATION_DATA_PATH']
    distances = calc_dist_table(metadata_path, processed_data_path)
