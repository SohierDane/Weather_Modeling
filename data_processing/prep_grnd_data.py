"""
Runs the complete ground station data preparation process:
1) Consolidate each set of annual station files into 1 file per station
2) Filter out stations that aren't relevant
3) Clean the remaining data
"""

from gsod_raw_to_1_file_per_station import export_active_stations
from filter_grnd_station_files import filter_stations
from clean_grnd_data import clean_all_stations

if __name__ == '__main__':
    export_active_stations()
    filter_stations()
    clean_all_stations()
