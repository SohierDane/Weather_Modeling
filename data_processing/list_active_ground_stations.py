'''
Generates a set of the GSOD stations active in any one of the
specified years. Does not check for data completeness within the year.

Expects file names in the format of: 165970-99999-2002.op
With format: USAF ID-WBAN ID-year
'''
import os


def get_station_nms_in_yr(path):
    stn_names = {(x[0], x[1]) for x in os.listdir(path).split('-')}
    return stn_names


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
    first_yr = 2000
    last_yr = 2009
    nms = get_names_in_yrs(first_yr, last_yr)
    USAF_names = [x[0] for x in nms]
    WBAN_names = [x[1] for x in nms]
    with open('relevant_USAF_codes.txt', 'w') as f_open:
        for nm in USAF_names:
            f_open.write(nm+'\n')
    with open('relevant_WBAN_codes.txt', 'w') as f_open:
        for nm in WBAN_names:
            f_open.write(nm+'\n')
