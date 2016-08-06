"""
Deletes ground stations outside of the acceptable latitudes or
without adequate lat/lon information. Merges stations @ with different
names that are  at the same location.
"""
import os
import pandas as pd
import itertools
import weather_mod_utilities
from get_constants import get_project_constants


def trim_df_to_useful_latitudes(df, min_lat, max_lat):
    '''
    Trim DF to all processed station data files within valid latitudes
    and with enough metadata to use

    Lowest real point on dry land is the border of the dead sea @ 418 M.
    Anything less than that is an invalid entry or a missing/-9999 code.
    '''
    elevation_of_lowest_pt_on_dry_land = -418
    df = df[df['ELEV(M)'] >= elevation_of_lowest_pt_on_dry_land]
    df = df.dropna(axis=0, subset=['LAT', 'LON', 'ELEV(M)', 'CTRY'])
    max_possible_lat = 90
    min_possible_lat = -90
    max_possible_lon = 180
    min_possible_lon = -180
    df = df[df['LAT'] < max_possible_lat]
    df = df[df['LAT'] > min_possible_lat]
    df = df[df['LON'] < max_possible_lon]
    df = df[df['LON'] > min_possible_lon]
    return df


def delete_stations_not_in_list(safelist, tgt_dir):
    stations_in_dir = pd.Series(os.listdir(tgt_dir))
    stns_to_drop = stations_in_dir[
                stations_in_dir.apply(lambda x: x not in safelist)]
    for stn_path in stns_to_drop:
        os.remove(os.path.join(tgt_dir, stn_path))


def get_stations_to_merge(df):
    '''
    Identifies pairs of stations that should be merged based on their ID codes.
    If multiple stations must be merged into, first item pair (x[0]) is stable
    across pairs.

    Does not attemp a name based merge due to low quality
    of the station name data. See high frequency of names such as
    'BOGUS FRENCH' or '...' or 'NAME AND LOC UNKN'

    Some USAF codes are duplicated due to use as special codes:
    049999 = USAF code for many stations in Greenland
    949999 = USAF code for many stations in Australia
    999999 = no USAF code, only WBAN code used
    '''
    special_USAF_codes = ['999999', '949999', '049999']
    USAF_matches = df[df.USAF.duplicated() & ~df.USAF.isin(special_USAF_codes)
                      ].groupby('USAF').groups.keys()
    station_matches = set([tuple(df[df.USAF == x].ID.values) for x in USAF_matches])
    WBAN_matches = df[df.WBAN.duplicated() & ~(df.WBAN == '99999')
                      ].groupby('WBAN').groups.keys()
    station_matches.update([tuple(df[df.WBAN == x].ID.values) for x in WBAN_matches])
    station_matches = [set([(x[0], i) for i in x[1:]]) for x in station_matches]
    return sorted([x for x in itertools.chain.from_iterable(station_matches)])


def merge_stations(stn_pairs, processed_data_path):
    '''
    Merges specified station files.

    Todo: update to always use either newest or oldest station
    '''
    active_stns = set(os.listdir(processed_data_path))
    for pair in stn_pairs:
        stn1 = pair[0]+'.csv'
        stn2 = pair[1]+'.csv'
        if stn1 in active_stns and stn2 in active_stns:
            stn1_path = os.path.join(processed_data_path, stn1)
            stn2_path = os.path.join(processed_data_path, stn2)
            if os.path.exists(stn1_path) and os.path.exists(stn2_path):
                df1 = pd.read_csv(stn1_path, index_col=0, dtype={'Date': str})
                df2 = pd.read_csv(stn2_path, index_col=0, dtype={'Date': str})
                df1 = pd.concat([df1, df2[df2.index.isin(df1.index.values)]])
                df1.to_csv(stn1_path, index=False)
                os.remove(stn2_path)


def filter_stations():
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    max_lat = project_constants['MAX_LATITUDE']
    min_lat = project_constants['MIN_LATITUDE']
    metadata_df = weather_mod_utilities.load_metadata(metadata_path)
    metadata_df = trim_df_to_useful_latitudes(
        metadata_df, min_lat, max_lat)
    stns_to_keep = [x+'.csv' for x in metadata_df['ID'].values]
    delete_stations_not_in_list(stns_to_keep, processed_data_path)
    stns_to_merge = get_stations_to_merge(metadata_df)
    merge_stations(stns_to_merge, processed_data_path)
    with open('stations merged.txt', 'w+') as f:
        for line in stns_to_merge:
            f.write(str(line)+'\n')


if __name__ == '__main__':
    filter_stations()
    print('filtering complete')
