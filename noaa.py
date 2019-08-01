from concurrent import futures
from functools import partial
import logging
from math import cos
from math import sqrt
import os 

import pandas as pd
import requests


LOGGER = logging.getLogger(__name__)
NUM_WORKERS = 6


def calculate_distance(lat_long_pair_1, lat_long_pair_2):
    """Calculate distance between a pair of lat ands longs

    TODO: possibly a more accurate, performant solution can 
    be used

    :param tuple lat_long_pair_1: 
        a tuple representing the lat and long coordinates
    :param tuple lat_long_pair_2: 
        a tuple representing the lat and long coordinates

    :return: the distance between the two coordinate pairs
    :rtype: float
    """
    lat1, lng1 = lat_long_pair_1[0], lat_long_pair_1[1]
    lat2, lng2 = lat_long_pair_2[0], lat_long_pair_2[1]
    r = 6371000 # radius of the Earth in m
    x = (lng2 - lng1) * cos(0.5*(lat2+lat1))
    y = (lat2 - lat1)
    return r * sqrt( x * x + y * y )


def retrieve_noaa_data(token):
    """Retrieve and create a dataframe from the NOAA API

    :param str token: 
        string representing API token

    :return: a dataframe representing all NOAA stations
    :rtype: pandas.DataFrame
    """
    results = []
    offset = 0

    while True:
        res = requests.get(
            'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations', 
            headers={'Token': token}, 
            params={'limit':'1000', 'offset': str(offset)})
        res.raise_for_status()
        results.extend(res.json()['results'])
        if len(results) > res.json()['metadata']['resultset']['count']:
            break
        else:
            print(f'length of results is {len(results)}')
            offset += 1000
    
    # ensure results align with the API counts
    assert len(results) == res.json()['metadata']['resultset']['count']
        
    df = pd.DataFrame.from_dict(results)
    return df


def find_closest_noaa_station(noaa_stations, row):
    """Find the closest station given a row from the circle data

    :param list noaa_stations: 
        A list of dictionaries representing the NOAA stations and their
        coordinates
    :param pandas.core.series.Series row: 
        a row from a pandas DataFrame

    :return: the closest NOAA station and their coordinates
    :rtype: dict
    """
    lat_lng_pair = (row['lat'], row['lon'])
    dist_calc = partial(calculate_distance, lat_lng_pair)
    closest_noaa = sorted(
        noaa_stations, key = lambda d: dist_calc((d['coordinates'])))[0]
    result = {
        'circle_name': row['circle_name'],
        'circle_coordinates': (row['lat'], row['lon']),
        'closest_station': closest_noaa['name'],
        'closest_coordinates': closest_noaa['coordinates']
    }
    return result


def main():
    """Main callable to execute script

    Keep in mind for the this work, you will need to set an environmental variable
    titled "NOAA_API_KEY"
    
    :return: a dataframe representing the circle name and their closest NOAA station
    :rtype: pandas.DataFrame
    """
    circles_data = pd.read_csv('audubon-cbc/bird_count_cleaned_may_29_2019.csv')
    noaa_stations = retrieve_noaa_data(os.environ.get('NOAA_API_KEY'))
    noaa_pairs = [
        {'name': row['name'], 'coordinates': (row['latitude'], row['longitude'])}
        for _, row in noaa_stations.iterrows()]
    distance_callable = partial(find_closest_noaa_station, noaa_pairs)
    results = []

    # 6 workers on a Macbook with 16GB of memory seems to be fine
    # please adjust to your machine's specs
    #
    # keep in mind that this will take some time to run since there are
    # over 100k circle records and 130k NOAA stations to reference
    with futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        jobs = [
            executor.submit(distance_callable, row)
            for _, row in circles_data.iloc[0:10, :].iterrows()]

        for job in futures.as_completed(jobs):
            output = job.result()
            LOGGER.info(output)
            results.append(output)

    df = pd.Dataframe.from_dict(results)
    return df


if __name__ == "__main__":
    main()
