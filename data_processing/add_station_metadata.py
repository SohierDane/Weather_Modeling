from __future__ import division
import pandas as pd
import numpy as np


def convert_to_rads(x):
    return x*np.pi/180


def haversine_dist(lat1, lon1, lat2, lon2, radius_Earth=6384):
    # accepts lat/long in degrees, converts to radians
    # R = radius of earth in kilometers
    lat1 = convert_to_rads(lat1)
    lat2 = convert_to_rads(lat2)
    lon1 = convert_to_rads(lon1)
    lon2 = convert_to_rads(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return radius_Earth * c


base_metadata_path = '/Users/sohier/Desktop/Malaria_Rainfall_sample_data/ish-history.csv'
df = pd.read_csv(base_metadata_path, header=0)
