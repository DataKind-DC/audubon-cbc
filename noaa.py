from concurrent import futures
import datetime
from functools import partial
import logging
import math
import os

# from geopy.distance import geodesic
import pandas as pd
import requests


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
NUM_WORKERS = 12


def haversine_formula(coord1, coord2):
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
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


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
    shortest = pd.np.Inf

    for station in noaa_stations:
        calc_distance = haversine_formula(station['coordinates'], lat_lng_pair)
        if  calc_distance < shortest:
            closest_noaa = {
                'circle_name': row['circle_name'],
                'circle_lat': row['lat'],
                'circle_lng': row['lon'],
                'closest_station_name': station['name'],
                'closest_station_lat': station['coordinates'][0],
                'closest_station_lng': station['coordinates'][-1],
                'distance': calc_distance,
            }
            shortest = calc_distance

    return closest_noaa


def main():
    """Main callable to execute script

    Keep in mind for the this work, you will need to set an environmental variable
    titled "NOAA_API_KEY"

    :return: a dataframe representing the circle name and their closest NOAA station
    :rtype: pandas.DataFrame
    """
    circles_data = pd.read_csv('bird_count_cleaned_may_29_2019.csv')
    noaa_stations = retrieve_noaa_data(os.environ.get('NOAA_API_KEY'))
    noaa_stations['maxdate'] = pd.to_datetime(noaa_stations['maxdate'])
    noaa_stations = noaa_stations.loc[noaa_stations['maxdate'] < pd.Timestamp(2020, 1, 1)]
    noaa_stations.to_csv('noaa_stations.csv.gz', index=False)
    noaa_pairs = [
        {
            'name': row['name'],
            'coordinates': (row['latitude'], row['longitude'])
        }
        for _, row in noaa_stations.iterrows()]
    distance_callable = partial(find_closest_noaa_station, noaa_pairs)
    results = []
    # 6 workers on a 2017 Macbook with 16GB of memory seems
    # to be fine, please adjust to your machine's specs
    #
    # Keep in mind that this will take some time to run since there are
    # over 100k circle records and 130k NOAA stations to reference
    with futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        jobs = [
            executor.submit(distance_callable, row)
            for _, row in circles_data.iterrows()]

        for job in futures.as_completed(jobs):
            output = job.result()
            logging.info(
                'closest NOAA to %s, is %s, with a distance of %s meters',
                output['circle_name'],
                output['closest_station_name'],
                output['distance'])
            results.append(output)
    df = pd.DataFrame.from_dict(results)
    df.to_csv('closest_station.csv.gz', index=False)


if __name__ == "__main__":
    main()
