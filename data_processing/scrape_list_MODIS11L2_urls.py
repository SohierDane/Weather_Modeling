'''
Extracts the urls from the NASA ftp website that will be used to
download the MODIS11_L2 data.

Each subdirectory in the NASA site is saved as a separate .txt file
'''

import requests
import re
import multiprocessing
from get_constants import get_project_constants


def get_urls(root_url, regex_str):
    html = requests.get(root_url).text
    date_re = re.compile('\d\d\d\d\.\d\d\.\d\d')
    urls = set(date_re.findall(html))
    urls = [x.encode('ascii') for x in urls]
    return urls


def download_urls_in_subdir(dir_suffix, ftp_root_url, metadata_dlpath):
    dir_root_url = '/'.join([ftp_root_url, dir_suffix])
    cur_suffixes = get_urls(dir_root_url, 'MOD11_L2.A[a-zA-Z0-9\.]*\.hdf')
    modis_urls = ['/'.join([dir_root_url, x]) for x in cur_suffixes]
    save_path = metadata_dlpath+dir_suffix+'_hdf_urls.txt'
    with open(save_path, 'w') as f_open:
        f_open.seek(0)
        for url in modis_urls:
            f_open.write(url+'\n')
        f_open.truncate()


def wrapper_for_downloads(arg_list):
    '''
    Workaround for pool.map not allowing multiple arguments
    '''
    download_urls_in_subdir(dir_suffix, ftp_root_url, metadata_dlpath)


if __name__ == "__main__":
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    metadata_dlpath = project_constants['MODIS11L2_METADATA_PATH']
    metadata_dlpath += '/ftp_urls/'
    ftp_root_url = 'http://e4ftl01.cr.usgs.gov/MOLT/MOD11_L2.006/'
    ftp_root_re = '\d\d\d\d\.\d\d\.\d\d'
    subdir_suffixes = get_urls(ftp_root_url, ftp_root_re)
    yrs_to_keep = [str(i) for i in range(int(first_yr), int(last_yr)+1)]
    subdir_suffixes = [x for x in subdir_suffixes if x[:4] in yrs_to_keep]
    dl_args = [(dir_suffix, ftp_root_url, metadata_dlpath)
                for dir_suffix in subdir_suffixes]
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(wrapper_for_downloads, dl_args)
    print("MODIS urls downloaded")
