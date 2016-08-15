'''
Generates a set of the GSOD stations active in any one of the
specified years. Does not check for data completeness within the year.

Expects file names in the format of: 165970-99999-2002.op
With format: USAF ID-WBAN ID-year
'''
import os
import pandas as pd
from calendar import isleap
from get_constants import get_project_constants


def count_station_days_data(USAF, WBAN, raw_data_path, year):
    '''
    Given a station's USAF and WBAN ID codes, returns data on the station's
    activity.

    Precipitation is ignored since many stations use the same value for
    zero and missing precipitation.
    '''
    station_path = raw_data_path+'/'+year+'/'+USAF+'-'+WBAN
    station_path += '-'+year+'.op'

    '''
    Initialize counts to # of days in the year, then subtract one
    for each day of data found.
    '''
    days_in_yr = {True: 366, False: 365}[isleap(year)]
    missing_counts = {x: days_in_yr for x in ['TEMP', 'STP', 'MAX', 'MIN']}
    if not os.path.isfile(station_path):
        return missing_counts
    df = pd.read_table(station_path)
    missing_val_codes = {'TEMP': '9999.9', 'STP': '9999.9',
                         'MAX': '9999.9', 'MIN': '9999.9'}
    # add separate field for 'all 4 present


def get_station_nms_in_yr(path):
    stn_names = [x.split('-') for x in os.listdir(path)]
    stn_names = [(x[0], x[1]) for x in stn_names]
    return set(stn_names)


def get_names_in_yrs(first_yr, last_yr, top_GSOD_dir):
    yrs_to_check = [str(i) for i in range(int(first_yr), int(last_yr)+1)]
    all_active_stations = set()
    for folder in os.listdir(top_GSOD_dir):
        if folder in yrs_to_check:
            folder_path = os.path.join(top_GSOD_dir, folder)
            cur_stations = get_station_nms_in_yr(folder_path)
            all_active_stations = all_active_stations.union(cur_stations)
    return all_active_stations


def list_active_stations():
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    raw_data_path = project_constants['RAW_GROUND_STATION_DATA_PATH']
    nms = get_names_in_yrs(first_yr, last_yr, raw_data_path)
    station_ids = set([(x[0], x[1]) for x in nms])
    metadata_path = project_constants['GSOD_METADATA_PATH']
    file_name = 'station_codes_active_{0}_to_{1}.txt'.format(first_yr, last_yr)
    output_path = os.path.join(metadata_path, file_name)
    with open(output_path, 'w') as f_open:
        f_open.seek(0)
        for nm in station_ids:
            line = nm[0]+', '+nm[1]+'\n'
            f_open.write(line)
        f_open.truncate()

if __name__ == '__main__':
    list_active_stations()
