'''
Extracts the urls from the NASA ftp website that will be used to
download the MODIS11_L2 data.

Each subdirectory in the NASA site is saved as a separate .txt file
'''

from get_constants import get_project_constants
from weather_mod_utilities import get_urls


def download_urls_in_subdir(dir_suffix, ftp_root_url, metadata_dlpath):
    """
    Saves a list of modis files available in this directory of the ftp server
    """
    dir_root_url = ftp_root_url+dir_suffix+'/'
    cur_suffixes = get_urls(dir_root_url, 'MOD11_L2.A[a-zA-Z0-9\.]*\.hdf')
    modis_urls = ['/'.join([dir_root_url, x]) for x in cur_suffixes]
    save_path = metadata_dlpath+dir_suffix+'_hdf_urls.txt'
    with open(save_path, 'w') as f_open:
        f_open.seek(0)
        for url in modis_urls:
            f_open.write(url+'\n')
        f_open.truncate()


def get_all_MODIS_urls():
    """
    Save lists of all modis files available for the project years.
    """
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
    for subdir in subdir_suffixes:
        download_urls_in_subdir(subdir, ftp_root_url, metadata_dlpath)
    print("MODIS urls downloaded")


if __name__ == "__main__":
    get_all_MODIS_urls()
