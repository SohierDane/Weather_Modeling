'''
- For each ground station identified as active, build a table with:
    USAF ID, WBAN ID, lat, long
- generate matrices of distances to all other stations on the same continent
- export data to csv
'''

from __future__ import division
import pandas as pd
import numpy as np
import os
from get_constants import get_project_constants
from list_active_ground_stations import list_active_stations


def convert_to_rads(x):
    return x*np.pi/180


def haversine_dist(lat1, lon1, lat2, lon2, radius_Earth=6384):
    # accepts lat/long in degrees, converts to radians
    # default radius of earth is in kilometers
    lat1 = convert_to_rads(lat1)
    lat2 = convert_to_rads(lat2)
    lon1 = convert_to_rads(lon1)
    lon2 = convert_to_rads(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return radius_Earth * c


def get_station_data(first_yr, last_yr, metadata_dir):
    all_station_metadata_path = os.path.join(metadata_dir, 'ish-history.csv')
    all_station_metadata = pd.read_csv(all_station_metadata_path, header=0)
    active_ids_file_name = 'station_codes_active_{0}_to_{1}.txt'.format(
        first_yr, last_yr)
    active_stn_ID_path = os.path.join(metadata_dir, active_ids_file_name)
    if not os.path.isfile(active_stn_ID_path):
        list_active_stations()
    with open(active_stn_ID_path, 'r') as f_open:
        stn_ids = f_open.read()
    stn_ids = stn_ids.strip().split('\n')
    return stn_ids, all_station_metadata


def format_df_stn_ids(df):
    # add column to dataframe that matches convention of stn_ids
    df['USAF'] = df['USAF'].apply(str)
    df['USAF'] = df['USAF'].apply(lambda x: x.zfill(6))
    df['WBAN'] = df['WBAN'].apply(str)
    df['WBAN'] = df['WBAN'].apply(lambda x: x.zfill(5))
    df['ID'] = df['USAF']+', '+df['WBAN']
    return df


def trim_to_useful_latitudes(df, min_lat, max_lat):
    df = df[df['LAT'] > min_lat]
    df = df[df['LAT'] < max_lat]
    return df


def build_distances_table(stn_ids, df):
    df = format_df_stn_ids(df)
    df = df.loc[df['ID'].isin(stn_ids)]
    df = df.dropna(axis=0, subset=['LAT', 'LON', 'ELEV(.1M)'])
    df = trim_to_useful_latitudes(df, min_lat, max_lat)
    return df


def add_continent_id(df):
    '''
    'from http://www.weathergraphics.com/identifiers/:
    The WMO identifier, often called the index number relies on a 6-digit numeric
     code to identify a land weather station. The first two digits are referred to
     as the block number and refer to the geographic area (00-29 Europe, 30-59 Asia
     , 60-68 Africa, 69 special use, 70-79 North America, 80-89 South America,
     90-99 Oceania'

    Based on visual inspection of the data this appears to hold for USAF codes.
    '''
    pass


if __name__ == '__main__':
    first_yr = '2000'
    last_yr = '2009'
    metadata_dir = '/Users/sohier/Desktop/Sample_weather_data'
    max_lat = 50
    min_lat = -50
#    project_constants = get_project_constants()
#    first_yr = project_constants['FIRST_YR']
#    last_yr = project_constants['LAST_YR']
#    metadata_dir = project_constants['GSOD_METADATA_PATH']
#    max_lat = project_constants['MAX_LATITUDE']
#    min_lat = project_constants['MIN_LATITUDE']
    stn_ids, df = get_station_data(first_yr, last_yr, metadata_dir)
    df = build_distances_table(stn_ids, df, min_lat, max_lat)
    