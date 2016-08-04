"""
Utilities for the weather modeling project
"""

from __future__ import division
import pandas as pd
import requests
import os
import re
from get_constants import get_project_constants


def get_active_station_IDs_in_folder(path):
    active_stations = os.listdir(path)
    # handling in case directory was extracted from a zip
    if '.DS_Store' in active_stations:
        active_stations.remove('.DS_Store')
    end_of_id_idx = active_stations[0].rfind('.')
    active_stations = [x[:end_of_id_idx] for x in active_stations]
    return active_stations


def load_metadata(metadata_path):
    station_metadata_file = 'isd-history.csv'
    metadata_df = pd.read_csv(os.path.join(
        metadata_path, station_metadata_file),
        dtype={col: str for col in ['USAF', 'WBAN', 'BEGIN', 'END']})
    metadata_df['ID'] = metadata_df['USAF']+'-'+metadata_df['WBAN']
    metadata_df['LAT'] = metadata_df['LAT']/1000
    metadata_df['LON'] = metadata_df['LON']/1000
    return metadata_df


def get_urls(root_url, regex_str):
    html = requests.get(root_url).text
    date_re = re.compile(regex_str)
    url_suffixes = set(date_re.findall(html))
    url_suffixes = [x.encode('ascii') for x in url_suffixes]
    return url_suffixes


if __name__ == "__main__":
    config = get_project_constants()
    metadata_path = config['GSOD_METADATA_PATH']
    processed_data_path = config['PROCESSED_GROUND_STATION_DATA_PATH']
