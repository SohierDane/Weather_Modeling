'''
1) For each station identified as active, build a table with:
    USAF ID, WBAN ID, lat, long
2) add columns with distances to all other stations
3) export data to csv
'''

from __future__ import division
import pandas as pd
import numpy as np
import os
from get_constants import get_project_constants


def convert_to_rads(x):
    return x*np.pi/180


def haversine_dist(lat1, lon1, lat2, lon2, radius_Earth=6384):
    # accepts lat/long in degrees, converts to radians
    # R = radius of earth in kilometers
    lat1 = convert_to_rads(lat1)
    lat2 = convert_to_rads(lat2)
    lon1 = convert_to_rads(lon1)
    lon2 = convert_to_rads(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return radius_Earth * c


def build_distances_table():
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    metadata_dir = project_constants['GSOD_METADATA_PATH']
    all_station_metadata_path = os.path.join(metadata_dir, 'ish-history.csv')
    all_station_metadata = pd.read_csv(all_station_metadata_path, header=0)
    active_ids_file_name = 'station_codes_active_{0}_to_{1}.txt'.format(
        first_yr, last_yr)
    active_stn_ID_path = os.path.join(metadata_dir, active_ids_file_name)
    with open(active_stn_ID_path, 'r') as f_open:
        stn_ids = f_open.read()
    stn_ids = stn_ids.strip().split('\n')


if __name__ == '__main__':
    build_distances_table()
