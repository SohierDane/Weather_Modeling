"""
Calculates & saves distances between all stations in the folder.

Recommend subsetting the data before running as the pairwise distances
use a O(N^2) implementation.
"""

from __future__ import division
import os
import pandas as pd
import weather_mod_utilities
from time import time
from get_constants import get_project_constants
from geopy.distance import great_circle
from copy import deepcopy


def get_nearest_neighbors(tgt_coords, metadata_df, k, min_distance=10):
    """
    Give a dataframe of gsod metadata and target coordinates,
    returns a numpy array of the pairwise distances between stations.
    """
    df = deepcopy(metadata_df)
    df['coord_pairs'] = df.coords.apply(lambda x: tuple([tgt_coords, x]))
    df['dists'] = df.coord_pairs.apply(lambda x: great_circle(*x).miles)
    df = df[df['dists'] > min_distance]
    df = df[df.dists.isin(df.dists.nsmallest(k))]
    results = zip(df.index.values.tolist()+df.dists.values.tolist())
    results.sort(key=lambda x: x[1])
    return [x[0] for x in results]+[x[1] for x in results]


def get_all_nearest_neighbors(Y_df, X_stations, k, min_distance=10):
    """
    Add columns detailing relationship between each station in Y_df
    its nearest neighbors.
    """
    X_df = deepcopy(X_stations)
    X_df.set_index(['ID'], inplace=True)
    new_cols = Y_df.coords.apply(
        lambda x: get_nearest_neighbors(x, X_df, k, min_distance))
    for i in range(k):
        Y_df['neighbor_'+str(i)] = new_cols.apply(lambda x: x[i])
        Y_df['neighbor_dist_'+str(i)] = new_cols.apply(lambda x: x[i+k])
        Y_df['elev_diff_'+str(i)] = Y_df['neighbor_'+str(i)].apply(
            lambda x: X_df['ELEV(M)'].loc[x])
        Y_df['elev_diff_'+str(i)] = Y_df['elev_diff_'+str(i)] - Y_df['ELEV(M)']
        Y_df['neighbor_lat_'+str(i)] = Y_df['neighbor_'+str(i)].apply(
            lambda x: X_df['LAT'].loc[x])
    return Y_df


def load_station_data(station_ID, processed_data_path):
    """
    Loads the date & mean temperature data for a station
    """
    cur_path = os.path.join(processed_data_path, station_ID)+'.csv'
    df = pd.read_csv(cur_path, parse_dates=[0], infer_datetime_format=True)
    df.set_index('Date', inplace=True)
    return pd.DataFrame(df['Temp'])


def unpack_stations_daily_data(Y_ID, neighbor_IDs, processed_data_path):
    """
    Loads the daily data for one Y station and its nearest neighbors.

    Only retains days where all stations have reported data.
    """
    Y_df = load_station_data(Y_ID, processed_data_path)
    Y_df.rename(columns={'Temp': 'Temp_Y'}, inplace=True)
    Y_df['Y_ID'] = Y_ID
    data = []
    for i, ID in enumerate(neighbor_IDs):
        X_station = load_station_data(ID, processed_data_path)
        X_station.rename(columns={'Temp': 'Temp_'+str(i)}, inplace=True)
        data.append(X_station)
    for X_df in data:
        Y_df = Y_df.merge(X_df, left_index=True, right_index=True)
    return Y_df


def unpack_all_daily_data(meta_df, processed_data_path, k):
    """
    Adds nearest neighbor metrics to the metadata
    """
    meta_df.set_index('ID', inplace=True)
    meta_columns_to_add_to_daily = []
    for i in xrange(k):
        meta_columns_to_add_to_daily.append('neighbor_lat_'+str(i))
        meta_columns_to_add_to_daily.append('neighbor_dist_'+str(i))
        meta_columns_to_add_to_daily.append('elev_diff_'+str(i))

    daily_data = []
    for Y_ID in meta_df.index:
        neighbors = meta_df[['neighbor_'+str(i) for i in xrange(k)]].loc[Y_ID].values
        cur_data = unpack_stations_daily_data(Y_ID, neighbors, processed_data_path)
        for col in meta_columns_to_add_to_daily:
            cur_data[col] = meta_df[col].loc[Y_ID]
        daily_data.append(cur_data)
    return pd.concat(daily_data)


def prep_analytics_base_table(k, min_distance=10):
    """
    Generates an analytics base table with data on the K nearest neighbors
    of each Y station. Includes option to exclude stations closer than
    a minimum distance to model sparse data.

    Min_distance should stay above 10 to weather stations that are actually
    at the same airport.
    """
    start_time = time()
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    meta_df = weather_mod_utilities.load_metadata(metadata_path)
    meta_df = meta_df[meta_df.ID.isin(weather_mod_utilities.
                      get_active_station_IDs_in_folder(processed_data_path))]
    Y_stations = meta_df.sample(frac=0.1, random_state=42)
    X_stations = meta_df[~meta_df.ID.isin(Y_stations.ID)]
    meta_df = get_all_nearest_neighbors(Y_stations, X_stations, k, min_distance)
    got_neighbors_time = int(time()-start_time)
    print("Got nearest neighbors after "+str(got_neighbors_time)+" seconds")
    analytics_base_table = unpack_all_daily_data(meta_df, processed_data_path, k)
    analytics_base_table.reset_index(inplace=True)
    del analytics_base_table['Date']
    del analytics_base_table['Y_ID']
    print("Analytics base table loaded")
    return analytics_base_table


if __name__ == '__main__':
    k = 5
    abt = prep_analytics_base_table(k)
