'''
Exports all station files in the active years to one file per station
in the processed data folder.
'''

import os
from get_constants import get_project_constants


def extract_date_info(yrmoda):
    '''
    Unpack NASA yrmoda string in to date, year, month, day

    For example:
    >>> extract_date_info('20020103')
    ['2002-01-03', '2002', '01', '03']
    '''
    date_parts = [yrmoda[:4], yrmoda[4:6], yrmoda[6:]]
    return ['-'.join(date_parts)] + date_parts


def process_raw_file(raw_f_path):
    '''
    Take original NASA data, drops several columns,
    splits date into more useful formats, and converts to csv format
    '''
    with open(raw_f_path, 'r') as f:
        # read one line to skip past the header
        f.readline()
        data = [line.strip().split() for line in f.readlines()]
    col_to_keep_idxs = [2, 3, 9, 17, 18, 19]
    data = [[line[i] for i in col_to_keep_idxs] for line in data]
    data = [extract_date_info(x[0])+x[1:] for x in data]
    # strip precip flag off as separate column
    for line in data:
        precip_flag = line[-1][-1]
        line[-1] = line[-1][:-1]
        line += precip_flag
    data = [', '.join(x)+'\n' for x in data]
    return data


def add_data_to_station_file(raw_f_path, processed_data_dir_path):
    '''
    Configure output file name and header then export processed data

    Expect input file names in the format of: 165970-99999-2002.op
    With format: USAF ID-WBAN ID-year
    '''
    idx_end_station_id = raw_f_path.rfind('-')
    station_id = os.path.basename(raw_f_path)[idx_end_station_id]
    output_path = os.path.join(processed_data_dir_path, station_id)+'.csv'
    output_cols = ['Date', 'Year', 'Month', 'Day', 'Temp', 'STP',
                   'Max_Temp', 'Min_Temp', 'Precipitation', 'Precip_Flag']
    if not os.path.isfile(output_path):
        # if the file doesn't exist, create it and add a 2 line header
        with open(output_path, 'w+') as f:
            f.write(', '.join(output_cols)+'\n')
    processed_data = process_raw_file(raw_f_path)
    with open(output_path, 'a') as f:
        for line in processed_data:
            f.write(line)


def export_active_stations():
    '''
    For all files in all folders within the project timeframe, export
    processed data
    '''
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    raw_data_path = project_constants['RAW_GROUND_STATION_DATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    yrs_to_check = [str(i) for i in range(int(first_yr), int(last_yr)+1)]
    counter = 0
    for folder in os.listdir(raw_data_path):
        if folder in yrs_to_check:
            for file in os.listdir(raw_data_path+'/'+folder):
                counter += 1
                if counter % 1000 == 0:
                    print (str(counter)+' files processed')
                f_path = '/'.join([raw_data_path, folder, file])
                add_data_to_station_file(f_path, processed_data_path)


if __name__ == '__main__':
    export_active_stations()
    print("finished exporting gsod data")
