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


def haversine_dist(lat1, lon1, cos_lat_1, lat2, lon2, cos_lat_2,
                   radius_Earth=6384):
    # expects lat/long in radians
    # default radius of earth is in kilometers
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + cos_lat_1 * cos_lat_2 * np.sin(dlon/2)**2
    return 2 * radius_Earth * np.arctan2(np.sqrt(a), np.sqrt(1-a))


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
            distance = haversine_dist(df.LAT.iloc[i], df.LON.iloc[i],
                                      df.cos_LAT.iloc[i],
                                      df.LAT.iloc[j], df.LON.iloc[j],
                                      df.cos_LAT.iloc[j])
            dists[i, j] = distance
            dists[j, i] = distance
    return dists


def load_metadata_in_radians(metadata_path):
    metadata_df = weather_mod_utilities.load_metadata(metadata_path)
    metadata_df['LAT'] = metadata_df['LAT'].apply(np.radians)
    metadata_df['LON'] = metadata_df['LON'].apply(np.radians)
    metadata_df['cos_LAT'] = metadata_df['LAT'].apply(np.cos)
    return metadata_df


def calc_dist_table(metadata_path, processed_data_path):
    start_time = time()
    metadata_df = load_metadata_in_radians(metadata_path)
    active_stations = weather_mod_utilities.get_active_station_IDs_in_folder(
        processed_data_path)
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
    distances = calc_table(metadata_df)
    run_time = time()-start_time
    print('distance calculations complete in '+str(int(run_time))+' seconds')
    return distances


def get_all_nearest_neighbors(distance_table, k, idx_to_ids, min_distance=10):
    """
    Returns the k station ids closest to each station, as long as they
    are at least min_distance away (to avoid issues with multiple stations
    at, for example, one large air force base)
    """
    neighbors = {id: [] for id in idx_to_ids.values()}
    num_stations = distance_table.shape[0]
    for i in num_stations:
        cur_dists = [(idx_to_ids[j], distance_table[i, j]) for j in num_stations]
        cur_dists.sort(key=lambda x: x[1])
        cur_dists = [x for x in cur_dists if x[1] > min_distance]
        neighbors[i] = cur_dists[:k]
    return neighbors


if __name__ == '__main__':
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    d_table = calc_dist_table(metadata_path, processed_data_path)
    save_path = os.path.join(metadata_path, 'pairwise_distances')
    np.save(save_path, d_table)
