"""
Downloads the entire GSOD archive. 50+ gb, so prepare for a wait.
"""

import os.path
import urllib
import gzip
from get_constants import get_project_constants
from weather_mod_utilities import get_urls
from time import sleep


def download_n_unpack(url, save_dir):
    file_name = url[url.rfind('/')+1:]
    save_path = os.path.join(save_dir, file_name)
    if not os.path.exists(save_path.rstrip('.gz')):
        urllib.urlretrieve(url, save_path)
        with gzip.open(save_path, 'r') as f:
            data = f.read()
        with open(save_path.rstrip('.gz'), 'w+') as f:
            f.write(data)
        os.remove(save_path)


def download_gsod_yr(yr, save_dir):
    print "now downloading "+str(yr)
    if not os.path.isdir(save_dir+str(yr)):
        os.mkdir(os.path.join(save_dir, str(yr)))
    root_url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/'
    dir_url = root_url+str(yr)+'/'
    regex_pattern = '\d{6}\D\d{5}\D'+str(yr)+'\.op\.gz'
    data_files_in_dir = get_urls(dir_url, regex_pattern)
    data_files_in_dir = [dir_url+fname for fname in data_files_in_dir]
    for dl_url in data_files_in_dir:
        try:
            download_n_unpack(dl_url, save_dir+str(yr))
        except:
            sleep(15)
            print("Error downloading "+dl_url+", retrying")
            download_n_unpack(dl_url, save_dir+str(yr))


def download_all_of_gsod(save_dir):
    for year in xrange(2016, 1900, -1):
        download_gsod_yr(year, save_dir)
        print "downloaded "+str(year)


if __name__ == '__main__':
    project_constants = get_project_constants()
    raw_data_dlpath = project_constants['RAW_GROUND_STATION_DATA_PATH']
    download_all_of_gsod(raw_data_dlpath)
