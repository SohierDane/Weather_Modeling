"""
Calculates & saves distances between all stations in the folder.
Recommend subsetting the data before running.
"""
from __future__ import division
import os
import numpy as np
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
    return df.index.values.tolist()+df.dists.values.tolist()


def get_all_nearest_neighbors(Y_df, X_stations, k, min_distance=10):
    X_df = deepcopy(X_stations)
    X_df.set_index(['ID'], inplace=True)
    new_cols = Y_df.coords.apply(
        lambda x: get_nearest_neighbors(x, X_df, 5, 10))
    for i in range(k):
        Y_df['neighbor_'+str(i)] = new_cols.apply(lambda x: x[i])
        Y_df['neighbor_dist_'+str(i)] = new_cols.apply(lambda x: x[i+k])
        Y_df['evel_diff'+str(i)] = Y_df['neighbor_'+str(i)].apply(
            lambda x: X_df['ELEV(M)'].loc[x])
        Y_df['evel_diff'+str(i)] = Y_df['evel_diff'+str(i)] - Y_df['ELEV(M)']
        Y_df['neighbor_lat'+str(i)] = Y_df['neighbor_'+str(i)].apply(
            lambda x: X_df['LAT'].loc[x])
    return Y_df


#if __name__ == '__main__':
#    project_constants = get_project_constants()
#    metadata_path = project_constants['GSOD_METADATA_PATH']
#    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
#    df = weather_mod_utilities.load_metadata(metadata_path)
#    df = df.sample(n=1000)
#    Y_stations = df.sample(frac=0.1, random_state=42)
#    X_stations = df[~df.ID.isin(Y_stations.ID)]
#    df = run_neighbors_calc(metadata_path, processed_data_path, )
#    save_path = os.path.join(metadata_path, 'isd-with-neighbors')
#    df.to_csv(save_path, index=None)
