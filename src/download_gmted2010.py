'''
Downloads & unzips the GMTED2010 30 arc second median statistic
'''
from zipfile import ZipFile
from urllib import urlretrieve

data_url = 'http://edcintl.cr.usgs.gov/downloads/sciweb1/shared/topo/downloads/GMTED/Grid_ZipFiles/md30_grd.zip'
output_directory = 'elevation_raw_data/'
fpath = output_directory + 'GMTED2010.zip'
urlretrieve(data_url, fpath)
ZipFile.extractall(fpath)
