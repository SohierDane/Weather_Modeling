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


def limit_to_bounding_box(df, coords):
    min_lat, max_lat, min_lon, max_lon = coords
    df = df[df['LAT'] < max_lat]
    df = df[df['LAT'] > min_lat]
    df = df[df['LON'] < max_lon]
    df = df[df['LON'] > min_lon]
    return df


def load_metadata(metadata_path):
    station_metadata_file = 'isd-history.csv'
    metadata_df = pd.read_csv(os.path.join(
        metadata_path, station_metadata_file),
        dtype={col: str for col in ['USAF', 'WBAN', 'BEGIN', 'END']})
    metadata_df.dropna(subset=['LAT', 'LON', 'ELEV(M)'], inplace=True)
    metadata_df['ID'] = metadata_df['USAF']+'-'+metadata_df['WBAN']
    metadata_df['coords'] = metadata_df[['LAT', 'LON']].apply(tuple, axis=1)
    return metadata_df


def load_metadata_for_active_stns(metadata_path,
                                  bounds=None, country_code=None):
    active_stations = get_active_station_IDs_in_folder(
        processed_data_path)
    metadata_df = load_metadata(metadata_path)
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
    if bounds is not None:
        metadata_df = limit_to_bounding_box(metadata_df, bounds)
    if country_code is not None:
        metadata_df = metadata_df[metadata_df.CTRY == country_code]
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
    df = load_metadata(metadata_path)
