"""
Deletes ground stations outside of the acceptable latitudes or
without adequate lat/lon information. Merges stations @ with different
names that are  at the same location.
"""
import os
import pandas as pd
import pdb
from numpy import nan
from get_constants import get_project_constants


def convert_noaa_missing_to_null(df, stn):
    ''' converts noaa codes for missing data to null values'''
    df.replace({'9999.9': nan}, inplace=True)
    try:    
        df['Precipitation'].replace({'99.99': nan}, inplace=True)
    except KeyError:
        print(stn)
        print(df.head)
    return df


def clean_temp_data(df, stn):
    '''
    Strips trailing * tokens, if any
    '''
    for col in ['Temp', 'Max_Temp', 'Min_Temp']:
        try:
            df[col] = df[col].apply(lambda x: x[:3])
        except KeyError:
            print(stn)
    return df


def has_enough_days_complete_day(df):
    return len(df.dropna()) > 1000


def clean_all_stations():
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    deleted_stns = []
    counter = 0
    for stn in os.listdir(processed_data_path):
        counter += 1
        if counter % 100 == 0:
            print('cleaning station # '+str(counter))
        stn_path = os.path.join(processed_data_path, stn)
        df = pd.read_csv(stn_path, dtype=str)
        df.columns = df.columns.str.strip()
        df = convert_noaa_missing_to_null(df, stn)
        if has_enough_days_complete_day(df):
            df = clean_temp_data(df, stn)
            df.to_csv(stn_path)
        else:
            deleted_stns.append(stn)
            os.remove(stn_path)

    log_path = os.path.join(metadata_path, 'stations_with_too_little_data.txt')
    with open(log_path, 'w+') as f:
        for line in deleted_stns:
            f.write(str(line)+'\n')


if __name__ == '__main__':
    clean_all_stations()
    print('data cleaning complete')