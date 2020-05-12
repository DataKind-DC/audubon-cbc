import datetime
import logging
import math
import os
import pandas as pd
import numpy as np


def haversine_formula(coords):
    """Haversine Forumla for calculating distance between two
    coordinates in meters.

    Distaince is similar to the GeoPy distance formulas except
    the geopy formula uses Vincenty’s formula. At longer distances,
    the difference is much more pronounced, however, since we are trying
    to find the closest one, the Haversine formula is a suitable
    approximation for our purposes.

    :param set coord1:
        A set containing the lat and long of the first location
    :param set coord1:
        A set containing the lat and long of the second location

    :return: distance between two sets in meters
    :rtype: float
    """
    R = 6372800  # Earth radius in meters
    #lat1, lon1 = coord1
    #lat2, lon2 = coord2
    lat1, lon1, lat2, lon2 = coords

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def main_calcs(df):

    # calculate distances between circles and stations
    df.loc[:, 'distance'] = df.loc[:, ['lat', 'lon', 'latitude', 'longitude']].apply(haversine_formula, axis=1)

    # Convert NOAA temperatures from a tenth of a degree to degrees
    df.loc[:, 'noaa_tmax_value'] = df.loc[:, 'temp_max_value'] / 10.0 * 1.8 + 32.0
    df.loc[:, 'noaa_tmin_value'] = df.loc[:, 'temp_min_value'] / 10.0 * 1.8 + 32.0

    # Make variable for precipitation boolean
    df.loc[:, 'cbc_is_prec'] = (pd.notna(df.loc[:, 'min_snow']) |
                                pd.notna(df.loc[:, 'max_snow']) |
                                pd.notna(df.loc[:, 'am_rain']) |
                                pd.notna(df.loc[:, 'pm_rain']))

    # absolute temperature differece
    df.loc[:, 'tmin_diff'] = df.loc[:, 'min_temp'] - df.loc[:, 'noaa_tmin_value']
    df.loc[:, 'tmin_diff_abs'] = df.loc[:, 'tmin_diff'].abs()

    df.loc[:, 'tmax_diff'] = df.loc[:, 'max_temp'] - df.loc[:, 'noaa_tmax_value']
    df.loc[:, 'tmax_diff_abs'] = df.loc[:, 'tmax_diff'].abs()

    # remove temperature errors
    df.loc[df['tmax_diff_abs'] > 100.0, 'tmax_diff_abs'] = np.nan
    df.loc[df['tmin_diff_abs'] > 100.0, 'tmin_diff_abs'] = np.nan

    return df