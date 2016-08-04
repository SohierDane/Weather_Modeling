"""
Creates a zip archive containing only weather stations from the
specified country.
"""
import os
import pandas as pd
import zipfile
import pdb
import weather_mod_utilities
from get_constants import get_project_constants


def get_country_data_shard(country_code):
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    metadata_df = weather_mod_utilities.load_metadata(metadata_path)
    active_stations = os.listdir(processed_data_path)
    active_stations = [x[:x.rfind('.')] for x in active_stations]
    print "Found "+str(len(active_stations))+" total stations"
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
    metadata_df = metadata_df[metadata_df.CTRY == country_code]
    pdb.set_trace()
    print "Found "+str(len(metadata_df))+" stations in "+country_code
    files_to_archive = metadata_df.ID.values
    files_to_archive = [os.path.join(processed_data_path, x+'.csv') for x in files_to_archive]
    save_path = os.path.join(metadata_path, 'metadata')
    zip_path = os.path.join(save_path, country_code+'_shard.zip')
    zip_path = zip_path.encode('ascii')
    z = zipfile.ZipFile(zip_path, 'w')
    for file in files_to_archive:
        z.write(file)
    z.close()


if __name__ == '__main__':
    get_country_data_shard('ZA')
    print('archiving complete')
