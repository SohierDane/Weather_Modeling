'''
Exports all station files in the active years to one file per station
in the processed data folder.
'''

import os
from get_constants import get_project_constants


def list_station_IDs():
    '''
    For all files in all folders within the project timeframe, export
    processed data
    '''
    project_constants = get_project_constants()
    raw_data_path = project_constants['RAW_GROUND_STATION_DATA_PATH']
    metadata_path = project_constants['GSOD_METADATA_PATH']
    file_lists = [x[2] for x in os.walk(raw_data_path)]
    file_nms = []
    for file_list in file_lists:
        file_nms.extend(file_list)
    file_nms = [x for x in file_nms if x[-3:] == '.op']
    # remove the file suffix and the year (ex: -1999.op)
    unique_IDs = set([x[:x.rfind('-')] for x in file_nms])
    output_path = os.path.join(metadata_path, 'existing_station_names.txt')
    with open(output_path, 'w+') as f:
        for id in unique_IDs:
            f.write(id+'\n')


if __name__ == '__main__':
    list_station_IDs()
    print("finished identifying unique, existing stations")
