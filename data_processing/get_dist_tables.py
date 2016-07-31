"""
Calculates & saves distances between all stations on the same continent
"""
from __future__ import division
import os
import pandas as pd
import numpy as np
from time import time
from get_constants import get_project_constants
from country_data import get_country_to_continent_map


def haversine_dist(lat1, lon1, lat2, lon2, radius_Earth=6384):
    # accepts lat/long in degrees, converts to radians
    # default radius of earth is in kilometers
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)
    lon1 = np.radians(lon1)
    lon2 = np.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return radius_Earth * c


def calc_table(df):
    """
    Give a dataframe of gsod metadata, returns a numpy array
    of the pairwise distances between stations.
    """
    num_stations = len(df.ID.values)
    dists = np.zeros([num_stations, num_stations])
    for i in xrange(num_stations-1):
        for j in xrange(i+1, num_stations):
            distance = haversine_dist(df.LAT.iloc[i], df.LON.iloc[i],
                                      df.LAT.iloc[j], df.LON.iloc[j])
            dists[i, j] = distance
            dists[j, i] = distance
    print(dists.mean())
    return dists


def calc_dist_tables():
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    station_metadata_file = 'ish-history.csv'
    metadata_df = pd.read_csv(os.path.join(
        metadata_path, station_metadata_file),
        dtype={'USAF': str, 'WBAN': str})
    metadata_df['ID'] = metadata_df['USAF']+'-'+metadata_df['WBAN']
    active_stations = os.listdir(processed_data_path)
    end_of_id_idx = active_stations[0].rfind('.')
    active_stations = set([x[:end_of_id_idx] for x in active_stations])
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
#    dist_tables = {'all': calc_table(metadata_df)}
    
    ctry_to_continent = get_country_to_continent_map()
    metadata_df['Continent'] = metadata_df.CTRY.apply(
        lambda x: ctry_to_continent[x])
    continents = {'Europe', 'Africa', 'Asia', 'North America',
                  'South America', 'Oceania'}
    dist_tables = {cont: calc_table(metadata_df[
                    metadata_df.Continent == cont])
                   for cont in continents}
    for cont, d_table in dist_tables.iteritems():
        save_path = os.path.join(metadata_path, 'distances_'+cont)
        np.save(save_path, d_table)


if __name__ == '__main__':
    start_time = time()
    calc_dist_tables()
    run_time = time()-start_time
    print('distance calculations complete in '+str(int(run_time))+' seconds')
