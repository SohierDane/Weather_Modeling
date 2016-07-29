'''
Exports all station files in the active years to one file per station
in the processed data folder.
'''
import os
import pandas as pd
from get_constants import get_project_constants


def process_raw_file(raw_f_path):
    '''
    Takes original NASA data, drops several columns,
    splits date into more useful formats, and converts to csv format
    '''
    with open(raw_f_path, 'r') as f:
        header = f.readline().strip().split()
        data = [line.strip().split() for line in f.readlines()]
    cols_to_keep = ['YEARMODA', 'TEMP', 'STP', 'MAX', 'MIN', 'PRCP']
    col_to_keep_idxs = [header.index(x) for x in cols_to_keep]
    return [[line[i] for i in col_to_keep_idxs] for line in data]


def add_data_to_station_file(raw_f_path, processed_data_dir_path):
    '''
    Expects input file names in the format of: 165970-99999-2002.op
    With format: USAF ID-WBAN ID-year
    '''
    processed_data = process_raw_file(raw_f_path)
    idx_station_id = raw_f_path.rfind('/')+1
    idx_end_station_id = idx_station_id+12
    station_id = raw_f_path[idx_station_id:idx_end_station_id]
    USAF, WBAN = station_id.split('-')
    output_path = processed_data_dir_path+'/'+station_id+'.csv'
    output_cols = ['Date', 'Year', 'Month', 'Day', 'Temp', 'STP',
                   'Max_Temp', 'Min_Temp']
    if not os.path.isfile(output_path):
        # if the file doesn't exist, create it and add a 2 line header
        with open(output_path, 'w') as f:
            f.write('USAF:'+USAF+'WBAN:'+WBAN+'\n')
            f.write(', '.join(output_cols))
    with open(output_path, 'a') as f:


def export_active_stations():
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    raw_data_path = project_constants['RAW_GROUND_STATION_DATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    yrs_to_check = [str(i) for i in range(int(first_yr), int(last_yr)+1)]
    for folder in os.listdir(raw_data_path):
        if folder in yrs_to_check:
            for file in os.listdir(raw_data_path+'/'+folder):
                f_path = '/'.join([raw_data_path, folder, file])
                add_data_to_station_file(f_path, processed_data_path)




if __name__ == '__main__':
    export_active_stations()
