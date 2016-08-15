'''
Downloads the WWWF terrestrial ecosystems of the world file
'''

from urllib import urlretrieve

data_url = 'http://assets.worldwildlife.org/publications/15/files/original/official_teow.zip?1349272619&_ga=1.35062946.244009636.1468964253'
output_directory = 'ecoregion_data/'
fpath = output_directory + 'teow.zip'
urlretrieve(data_url, fpath)