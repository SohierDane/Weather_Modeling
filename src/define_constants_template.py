'''
Writes a json file with constants used by the project
such as file paths, years of data to consider, etc

Edit as needed for your data folder organization.
'''

import json

project_constants = {
    "PROCESSED_GROUND_STATION_DATA_PATH": "",
    "PROCESSED_TRMM_3B43_DATA_PATH": "",
    "RAW_TRMM_3B43_DATA_PATH": "",
    "MAX_LATITUDE": 50,
    "PROCESSED_TRMM_3B42_DATA_PATH": "",
    "PROCESSED_ELEVATION_DATA_PATH": "",
    "LAST_YR": "2009",
    "RAW_GROUND_STATION_DATA_PATH": "",
    "TRMM_3B42_METADATA_PATH": "",
    "ELEVATION_METADATA_PATH": "",
    "RAW_ELEVATION_DATA_PATH": "",
    "PROCESSED_ECOSYSTEM_DATA_PATH": "",
    "DAT_FILES_PATH": "",
    "RAW_ECOSYSTEM_DATA_PATH": "",
    "EARTHDATA_PWD": "",
    "FIRST_YR": "1998",
    "RAW_TRMM_3B42_DATA_PATH": "",
    "MIN_LATITUDE": -50,
    "EARTHDATA_USER_ID": "",
    "ECOSYSTEM_METADATA_PATH": "",
    "TRMM_3B43_METADATA_PATH": "",
    "GSOD_METADATA_PATH": ""
}


with open('project_constants.json', 'w') as f_open:
    f_open.seek(0)
    json.dump(project_constants, f_open, indent=4)
    f_open.truncate()
