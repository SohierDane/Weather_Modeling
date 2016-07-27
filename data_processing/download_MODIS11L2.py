'''
Downloads all hdf and xml files for the MODIS11L2 product over 
a specified range of dates and specified times of day.


Notes on NASA's conventions:
Incoming file names look like 'MOD11_L2.A2000055.1720.006.2015054160015.hdf'.
Mapped to useful info:
MOD11_L2.A    2000     055   17 20      .006.  2015054160015.hdf
prefix         yr  day_of_yr hr min   version# processing date

url for that file:
http://e4ftl01.cr.usgs.gov/MOLT/MOD11_L2.006/2000.02.24/
MOD11_L2.A2000055.1720.006.2015054160015.hdf

<- month and day sections are always len == 2 (01 not 1)

metadata is the same but suffixed .xml after the .hdf

'''

# set up to download only specific time of day for specific year to start,
# so can get 1 usable data first
# logging?
# zfill as needed to add zeroes to dates

import requests
import multiprocessing
import os.path
from urllib import urlretrieve
from get_constants import get_project_constants

project_constants = get_project_constants()
first_yr = project_constants['FIRST_YR']
last_yr = project_constants['LAST_YR']
ftp_user_id = project_constants['EARTHDATA_USER_ID']
ftp_pass = project_constants['EARTHDATA_PWD']
raw_data_dlpath = project_constants['RAW_MODIS11L2_DATA_PATH']
metadata_dlpath = project_constants['MODIS11L2_METADATA_PATH']

ftp_root_url = 'http://e4ftl01.cr.usgs.gov/MOLT/MOD11_L2.006/'
max_possible_days_in_yr = 366


def download_yr(year, hr, min, raw_data_dlpath=raw_data_dlpath,
                metadata_dlpath=metadata_dlpath, ftp_root_url=ftp_root_url,
                ftp_user_id=ftp_user_id, ftp_pass=ftp_pass):
    '''
    Downloads all files in year at a given time, such as all 1300 GMT data from 2004
    '''


def download_one_file(year, month, day, hr, min,
                 raw_data_dlpath=raw_data_dlpath,
                 metadata_dlpath=metadata_dlpath, ftp_root_url=ftp_root_url,
                 ftp_user_id=ftp_user_id, ftp_pass=ftp_pass):
    '''
    If the modis file does not already exist, downloads both hdf and xml
    Returns 1 if successful or file already exists, zero if error.
    '''
    subdir_prexif = str(year)+'.'+str(month)+'.'+str(day)
    fname = 'dlkjs'
    fpath = raw_data_dlpath+subdir_prexif+fname
    if os.path.isfile(fpath):
        return 1


#mirador_dat = requests.get(mirador_dat_url)
#mirador_dat = mirador_dat.text.strip().split('\n')
#yrs_to_download = [str(i) for i in range(first_yr, last_yr+1)]
#
#for line in mirador_dat:
#    if sum([1 if i in line else 0 for i in yrs_to_download]) > 0:
#        '''
#        Set file name as the last portion of the url.
#        Should look something like '3B42_Daily.20160429.7.nc4'
#        '''
#        fpath = output_directory+line.split('/')[-1]
#        fpath = fpath.encode('ascii')
#        urlretrieve(line, fpath)
