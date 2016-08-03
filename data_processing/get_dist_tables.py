"""
Calculates & saves distances between all stations on the same continent
"""
from __future__ import division
import os
import pandas as pd
import numpy as np
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
                print "processed "+str(counter)+" out of "+str(num_stations**2/2)
            distance = haversine_dist(df.LAT.iloc[i], df.LON.iloc[i],
                                      df.cos_LAT.iloc[i],
                                      df.LAT.iloc[j], df.LON.iloc[j],
                                      df.cos_LAT.iloc[j])
            dists[i, j] = distance
            dists[j, i] = distance
    print(dists.mean())
    return dists


def load_metadata(metadata_path):
    station_metadata_file = 'ish-history.csv'
    metadata_df = pd.read_csv(os.path.join(
        metadata_path, station_metadata_file),
        dtype={'USAF': str, 'WBAN': str})
    metadata_df['ID'] = metadata_df['USAF']+'-'+metadata_df['WBAN']
    metadata_df['LAT'] = metadata_df['LAT']/1000
    metadata_df['LON'] = metadata_df['LON']/1000
    metadata_df['LAT'] = metadata_df['LAT'].apply(np.radians)
    metadata_df['LON'] = metadata_df['LON'].apply(np.radians)
    metadata_df['cos_LAT'] = metadata_df['LAT'].apply(np.cos)
    return metadata_df


def calc_dist_tables():
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    active_stations = os.listdir(processed_data_path)
    end_of_id_idx = active_stations[0].rfind('.')
    active_stations = set([x[:end_of_id_idx] for x in active_stations])
    metadata_df = load_metadata(metadata_path)
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
    dist_tables = {'all': calc_table(metadata_df)}
    for cont, d_table in dist_tables.iteritems():
        save_path = os.path.join(metadata_path, 'distances_'+cont)
        np.save(save_path, d_table)


if __name__ == '__main__':
    start_time = time()
    calc_dist_tables()
    run_time = time()-start_time
    print('distance calculations complete in '+str(int(run_time))+' seconds')
