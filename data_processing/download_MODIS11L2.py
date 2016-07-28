'''
Downloads all hdf and xml files for the MODIS11L2 product over
a specified range of dates and specified times of day.

Please note that this is ~4 terabytes of data, if all times of day
are included.
'''

import os.path
import pycurl
import certifi
from get_constants import get_project_constants


def execute_download(url, output_path, ftp_upass, cookie_path):
    '''
    Downloads file via curl command that functions with NASA's ftp.
    Derived from documentation here:
    https://lpdaac.usgs.gov/sites/default/files/public/get_data/docs/Command%20Line%20Access%20Tips%20for%20Utilizing%20Earthdata%20Login.docx
    '''
    # exit early if file already exists.
    if os.path.isfile(output_path):
        return None
    c = pycurl.Curl()
    with open(output_path, 'wb') as f_out:
        c.setopt(c.USERPWD, ftp_upass)
        c.setopt(c.COOKIEJAR, cookie_path)
        c.setopt(c.COOKIE, cookie_path)
        c.setopt(c.URL, url)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.CAINFO, certifi.where())
        c.setopt(c.UNRESTRICTED_AUTH, True)
        c.setopt(c.WRITEDATA, f_out)
        c.perform()


def download_one_datetime(url, time, raw_data_dlpath, ftp_upass, cookie_path):
    '''
    If the modis file does not already exist, downloads hdf,jpg, and xml
    '''
    idx_date_start = 45
    idx_date_end = 55
    idx_browse_start = 57
    idx_hdf = 98
    date = url[idx_date_start:idx_date_end]
    output_path_base = raw_data_dlpath+'/MODIS11L2.'+date
    execute_download(url, output_path_base+'.hdf', ftp_upass, cookie_path)
    execute_download(url+'.xml', output_path_base+'.hdf.xml', ftp_upass, cookie_path)
    jpg_url = url[:idx_browse_start]+'BROWSE.'+url[idx_browse_start:idx_hdf]+'1.jpg'
    execute_download(jpg_url, output_path_base+'.jpg', ftp_upass, cookie_path)


def download_time_for_all_dates(time, raw_data_dlpath, metadata_path,
                                ftp_upass, cookie_path):
    '''
    Loop through every file in ftp_urls and download the correct time.
    '''
    idx_start_of_time = 75
    idx_end_of_time = 79
    ftp_url_files_path = metadata_path+'/ftp_urls/'
    ftp_url_files = os.listdir(ftp_url_files_path)
    counter = 0
    for url_file in ftp_url_files:
        counter += 1
        if counter % 100 == 0:
            print '@ '+time+' file # '+str(counter)
        with open(ftp_url_files_path+url_file, 'r') as f:
            url_list = f.read()
        url_list = url_list.strip().split('\n')
        url_for_time = [x for x in url_list if
                        x[idx_start_of_time:idx_end_of_time] == time]
        # skip time if for some reason it doesn't exist
        if len(url_for_time) == 1:
            url_for_time = url_for_time[0]
            download_one_datetime(url_for_time, time, raw_data_dlpath,
                                  ftp_upass, cookie_path)


if __name__ == '__main__':
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    ftp_user_id = project_constants['EARTHDATA_USER_ID']
    ftp_pass = project_constants['EARTHDATA_PWD']
    raw_data_dlpath = project_constants['RAW_MODIS11L2_DATA_PATH']
    metadata_path = project_constants['MODIS11L2_METADATA_PATH']
    ftp_upass = ftp_user_id+':'+ftp_pass

    # cookie file must exist for NASA's ftp system
    cookie_path = metadata_path+'/nasa_cookie.txt'
    open(cookie_path, 'a').close()

    # first time of day is 0005
    times_to_dl = [str(x).zfill(2)+'05' for x in range(0, 24)]
    for time_of_day in times_to_dl:
        print('processing '+time_of_day)
        download_time_for_all_dates(time_of_day, raw_data_dlpath,
                                    metadata_path, ftp_upass,
                                    cookie_path)
    print('Downloads complete.')
