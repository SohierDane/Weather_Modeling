'''
Given a url of a mirador file listing urls for TRMM downloads,
downloads only those files in the specified range of years.

Assumes mirador file such as can be obtained here:
http://mirador.gsfc.nasa.gov/cgi-bin/mirador/collectionlist.pl?keyword=TRMM_3B42_daily
'''

import requests
import os
from urllib import urlretrieve
from get_constants import get_project_constants


def download_trmm(mirador_dat_url, output_dir):
    # mirador dat website is a list of the actual file urls
    mirador_dat = requests.get(mirador_dat_url)
    mirador_dat = mirador_dat.text.strip().split('\n')
    yrs_to_download = [i for i in range(int(first_yr), int(last_yr)+1)]

    for line in mirador_dat:
        if sum([1 if i in line else 0 for i in yrs_to_download]) > 0:
            '''
            Set file name as the last portion of the url.
            Should look something like '3B42_Daily.20160429.7.nc4'
            '''
            fpath = os.path.join(output_dir, line.split('/')[-1])
            fpath = fpath.encode('ascii')
            # ignore files that have already been downloaded
            print(fpath)
            if not os.path.isfile(fpath):
                urlretrieve(line, fpath)


if __name__ == '__main__':
    project_constants = get_project_constants()
    first_yr = project_constants['FIRST_YR']
    last_yr = project_constants['LAST_YR']
    trmm_3b42_url = 'http://mirador.gsfc.nasa.gov/WWW-TMP/a998cd8b7287af47b194c23e65ce1769_all_data.txt?ftpscript=wget_data_only'
    trmm_3b43_url = 'http://mirador.gsfc.nasa.gov/WWW-TMP/94fe384fcb12dd1db9f7c37bd5da8853_all_data.txt?ftpscript=wget_data_only'
    download_trmm(trmm_3b42_url, project_constants['RAW_TRMM_3B42_DATA_PATH'])
    print "3b42 downloads complete"
    download_trmm(trmm_3b43_url, project_constants['RAW_TRMM_3B43_DATA_PATH'])
    print "3b43 downloads complete"
