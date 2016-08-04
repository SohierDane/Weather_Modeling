
"""
Downloads the entire GSOD archive. 50+ gb.
"""

import os.path
import urllib
from get_constants import get_project_constants
from weather_mod_utilities import get_urls

# http://www1.ncdc.noaa.gov/pub/data/gsod/2014/007026-99999-2014.op.gz


def download_n_unpack(url, save_dir):
    file_name = url[url.rfind('/')+1:]
    save_path = os.path.join(save_dir, file_name)
    #unzip the gz file if needed
    urllib.urlretrieve(url, save_path)
    if save_path[-2:] == 'gz':
        with gzip.open(save_path, 'r') as f:
            data = f.read()
        with open(save_path[:-2], 'w+') as f:
            f.write(data)
        os.remove(save_path)


def download_gsod_yr(yr):
    root_url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/'
    dir_url = root_url+str(yr)+'/'
    regex_pattern = dir_url+'\d*6-\d*5-\d*4.op.gz'
    data_files_in_dir = get_urls(dir_url, regex_pattern)
    return data_files_in_dir
    

def download_all_of_gsod():
    for year in xrange(2016, 1900, -1):
        download_gsod_yr(year)


#if __name__ == '__main__':
#    project_constants = get_project_constants()
#    raw_data_dlpath = project_constants['RAW_MODIS11L2_DATA_PATH']
