'''
Given a url of a mirador file listing urls for TRMM downloads,
downloads only those files in the specified range of years.

Assumes mirador file such as can be obtained here:
http://mirador.gsfc.nasa.gov/cgi-bin/mirador/collectionlist.pl?keyword=TRMM_3B42_daily
'''

import requests
from urllib import urlretrieve

# constants
min_yr = 2000
max_yr = 2009
mirador_dat_url = 'http://mirador.gsfc.nasa.gov/WWW-TMP/a998cd8b7287af47b194c23e65ce1769_all_data.txt?ftpscript=wget_data_only'
output_directory = 'raw_data_downloads/'

mirador_dat = requests.get(mirador_dat_url)
mirador_dat = mirador_dat.text.strip().split('\n')
yrs_to_download = [str(i) for i in range(min_yr, max_yr+1)]

for line in mirador_dat:
    if sum([1 if i in line else 0 for i in yrs_to_download]) > 0:
        '''
        Set file name as the last portion of the url.
        Should look something like '3B42_Daily.20160429.7.nc4'
        '''
        fpath = output_directory+line.split('/')[-1]
        fpath = fpath.encode('ascii')
        urlretrieve(line, fpath)
