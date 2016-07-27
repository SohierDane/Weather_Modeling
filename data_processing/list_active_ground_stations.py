'''
Generates a set of the GSOD stations active in any one of the
specified years. Does not check for data completeness within the year.

Expects file names in the format of: 165970-99999-2002.op
With format: USAF ID-WBAN ID-year
'''
import os
from get_constants import get_project_constants


def get_station_nms_in_yr(path):
    stn_names = [x.split('-') for x in os.listdir(path)]
    stn_names = [(x[0], x[1]) for x in stn_names]
    return set(stn_names)


def get_names_in_yrs(first_yr, last_yr):
    yrs_to_check = [str(i) for i in range(first_yr, last_yr+1)]
    top_GSOD_dir = 'gsod/'
    all_active_stations = set()
    for folder in os.listdir(top_GSOD_dir):
        if folder in yrs_to_check:
            folder_path = os.path.join(top_GSOD_dir, folder)
            cur_stations = get_station_nms_in_yr(folder_path)
            all_active_stations = all_active_stations.union(cur_stations)
    return all_active_stations


if __name__ == '__main__':
    project_constants = get_project_constants()
    first_yr = int(project_constants['FIRST_YR'])
    last_yr = int(project_constants['LAST_YR'])
    metadata_path = project_constants['GSOD_METADATA_PATH']
    nms = get_names_in_yrs(first_yr, last_yr)
    USAF_names = set([x[0] for x in nms])
    WBAN_names = set([x[1] for x in nms])
    USAF_path = os.path.join(metadata_path, 'relevant_USAF_codes.txt')
    with open(USAF_path, 'w') as f_open:
        f_open.seek(0)
        for nm in USAF_names:
            f_open.write(nm+'\n')
        f_open.truncate()
    WBAN_path = os.path.join(metadata_path, 'relevant_WBAN_codes.txt')
    with open(WBAN_path, 'w') as f_open:
        f_open.seek(0)
        for nm in WBAN_names:
            f_open.write(nm+'\n')
        f_open.truncate()
        f_open.close()
