'''
Writes a json file with constants used by the project
such as file paths, years of data to consider, etc

Edit as needed for your data folder organization.
'''

import json

project_constants = {
    'FIRST_YR': '',
    'LAST_YR': '',
    'RAW_TRMM_3B42_DATA_PATH': '',
    'RAW_ELEVATION_DATA_PATH': '',
    'GROUND_STATION_DATA_PATH': '',
    'RAW_ECOSYSTEM_DATA_PATH': '',
    'DAT_FILES_PATH': '',
    'EARTHDATA_USER_ID': '',
    'EARTHDATA_PWD': ''}


with open('project_constants.json', 'w') as f_open:
    f_open.seek(0)
    json.dump(project_constants, f_open, indent=4)
    f_open.truncate()
