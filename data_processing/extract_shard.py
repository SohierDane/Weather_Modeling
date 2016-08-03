"""
Creates a zip archive containing only weather stations from the
specified country.
"""
import os
import pandas as pd
import zipfile
from get_constants import get_project_constants


def get_country_data_shard(country_code):
    project_constants = get_project_constants()
    metadata_path = project_constants['GSOD_METADATA_PATH']
    processed_data_path = project_constants['PROCESSED_GROUND_STATION_DATA_PATH']
    station_metadata_file = 'ish-history.csv'
    metadata_df = pd.read_csv(os.path.join(
        metadata_path, station_metadata_file),
        dtype={'USAF': str, 'WBAN': str})
    metadata_df['ID'] = metadata_df['USAF']+'-'+metadata_df['WBAN']
    active_stations = os.listdir(processed_data_path)
    active_stations = [x[:x.rfind('.')] for x in active_stations]
    metadata_df = metadata_df[metadata_df.ID.isin(active_stations)]
    metadata_df = metadata_df[metadata_df.CTRY == country_code]
    files_to_archive = metadata_df.ID.values
    files_to_archive = [os.path.join(metadata_path, x+'.csv') for x in files_to_archive]
    zip_path = os.path.join(metadata_path, country_code+'_shard.zip')
    z = zipfile.Zipfile(zip_path, 'w+')
    for file in files_to_archive:
        z.write(file)
    z.close()


if __name__ == '__main__':
    get_country_data_shard('ZA')
    print('archiving complete')
