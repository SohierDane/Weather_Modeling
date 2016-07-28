'''
Downloads all hdf and xml files for the MODIS11L2 product over
a specified range of dates and specified times of day.

Please note that this is ~4 terabytes of data, if all times of day
are included.
'''

import requests
import os.path
import pycurl
from urllib import urlretrieve
from get_constants import get_project_constants

'''
curl notes:
-u == --username
-L == --location
-c == --cookie-jar
-b == --cookie
'''



def get_link(year, month, day, time_of_day, urls_dir_path=urls_dir_path):
    year = year.zfill(4)
    month = month.zfill(2)
    day = day.zfill(2)
    url_file_path = urls_dir_path+'.'.join([year, month, day])
    with open(url_file_path, 'r') as f_open:
        pass
    '''
    find closest match
    '''


def download_yr(year, time_of_day, raw_data_dlpath, metadata_dlpath,
                ftp_root_url, ftp_user_id, ftp_pass):
    '''
    Downloads all files in year at a given time, such as all 1300 GMT data from 2004
    '''


def download_one_file(year, month, day, time_of_day,
                      raw_data_dlpath, metadata_dlpath,
                      ftp_user_id, ftp_pass):
    '''
    If the modis file does not already exist, downloads both hdf and xml
    Returns 1 if successful or file already exists, zero if error.

confirmed that this curl command works:
curl -u username:pass -L -c test_cookie.txt -b test_cookie.txt http://e4ftl01.cr.usgs.gov/MOLT/MOD09A1.006/2001.01.09/MOD09A1.A2001009.h13v01.006.2015140120258.hdf --output MOD09A1.A2001009.h13v01.006.2015140120258.hdf

    '''
    subdir_prexif = '.'.join([str(year),str(month),+str(day)])
    fname = 'dlkjs'
    fpath = raw_data_dlpath+subdir_prexif+fname
    if os.path.isfile(fpath):
        return 1




if __name__ == '__main__':
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    ftp_user_id = project_constants['EARTHDATA_USER_ID']
    ftp_pass = project_constants['EARTHDATA_PWD']
    raw_data_dlpath = project_constants['RAW_MODIS11L2_DATA_PATH']
    metadata_dlpath = project_constants['MODIS11L2_METADATA_PATH']

    '''
    cookie file must exist for NASA's ftp system
    '''
    cookie_path = metadata_dlpath+'/nasa_cookie.txt'
    open(cookie_path, 'a').close()

    times_to_dl = [str(x).zfill(2)+'05' for x in range(0, 24)]
    for time_of_day in times_to_dl:
        for yr in range(int(first_yr), int(last_yr)+1):
            download_yr(yr, time_of_day,
                        raw_data_dlpath, metadata_dlpath,
                        ftp_user_id, ftp_pass)
