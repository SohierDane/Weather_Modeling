"""
Calculates & saves distances between all stations in the folder.
Recommend subsetting the data before running.
"""
from __future__ import division
import os
import numpy as np
import weather_mod_utilities
from time import time
from get_constants import get_project_constants
from geopy.distance import great_circle


def calc_table(df):
    """
    Give a dataframe of gsod metadata, returns a numpy array
    of the pairwise distances between stations.
    """
    num_stations = len(df.ID.values)
    dists = np.zeros([num_stations, num_stations])
    counter = 0
    for i in xrange(num_stations-1):
        for j in xrange(i+1, num_stations):
            counter += 1
            if counter % 10000 == 0:
                print "processed "+str(counter)+" out of "+str(int(num_stations**2/2))
            distance = great_circle(
                (df['LAT'].iloc[i], df['LON'].iloc[i]),
                (df['LAT'].iloc[j], df['LON'].iloc[j])).miles
            dists[i, j] = distance
            dists[j, i] = distance
    return dists


def calc_dist_table(metadata_path, processed_data_path, bounds=None):
    start_time = time()
    metadata_df = (weather_mod_utilities.load_metadata_for_active_stns(metadata_path))
    distances = calc_table(metadata_df)
    run_time = time()-start_time
    print('distance calculations complete in '+str(int(run_time))+' seconds')
    return distances


def neighbors_of(stn_ID, df, k, min_distance=10):
    """
    Returns only the neighbors of the target station as a sorted list
    in the format [(stn_id: distance)]
    """
    


def get_all_nearest_neighbors(df, k, min_distance=10):
    """
    Returns the k station ids closest to each station as long as they
    are at least min_distance away.
    """
    num_stations = len(df)
    df.reset_index(inplace=True)
    for j in xrange(k):
        df['neighbor_'+str(j)] = 0
        df['dist_to_neighbor_'+str(j)] = 0
    distance_table = calc_table(df)
    id_idx = 0
    dist_idx = 1
    for i in xrange(len(df)):
        cur_dists = [(j, distance_table[i, j]) for j in xrange(num_stations)]
        cur_dists = [x for x in cur_dists if x[1] > min_distance]
        cur_dists.sort(key=lambda x: x[1])
        for j in xrange(k):
            df['neighbor_'+str(j)].iloc[i] = cur_dists[j][id_idx]
            df['dist_to_neighbor_'+str(j)].iloc[i] = cur_dists[j][dist_idx]
    return df


def run_neighbors_calc(metadata_path, processed_data_path, bounds=None):
    start_time = time()
    active_stations = weather_mod_utilities.get_active_station_IDs_in_folder(
        processed_data_path)
    metadata_df = weather_mod_utilities.load_metadata(metadata_path)
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
    if bounds is not None:
        metadata_df = limit_to_bounding_box(metadata_df, bounds)
    distances = calc_table(metadata_df)
    run_time = time()-start_time
    print('distance calculations complete in '+str(int(run_time))+' seconds')
    return distances


if __name__ == '__main__':
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    df = run_neighbors_calc(metadata_path, processed_data_path, )
    save_path = os.path.join(metadata_path, 'isd-with-neighbors')
    df.to_csv(save_path, index=None)
