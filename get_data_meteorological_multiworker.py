import os
import sys
import time
import traceback
import json
import random
import csv
import queue
import logging
from multiprocessing import Pool
import multiprocessing

import requests


TOKEN_FILE = "tokens.listing"
cdo_tokens = multiprocessing.Queue()
STATION_LOOKUP={}


logger = logging.getLogger("noaa_climate_pull")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handlerF = logging.FileHandler("noaa_climate_pull.log")
handlerF.setFormatter(formatter)
handlerF.setLevel(logging.DEBUG)

handlerC = logging.StreamHandler()
handlerC.setFormatter(formatter)
handlerC.setLevel(logging.INFO)

# Add the handlers to the logger
logger.addHandler(handlerF)
logger.addHandler(handlerC)


def get_timeseries_batched(entity_desc, datasetid, stn_id, year_start, year_end, request_uri, out_file_json, out_file_csv, field_list, extra_params=None):

    result_count = 1000000 # does not matter atm, offset of 0 will always dominate
    current_offset = 0
    result_limit = 1000
    no_results = False

    list_obtained = []

    license_key = cdo_tokens.get(block=True)
    logger.debug(f"Using License key {license_key}")

    stn_name = STATION_LOOKUP[stn_id]["stn_name"]
    logger.info(f"Pulling for station {stn_id}, readings from {year_start}-{year_end}, location: {stn_name}")

    try:

        for year_current in range(year_start, year_end+1):
            no_results = False
            current_offset = 0

            head = {'token': license_key}

            while not no_results and (current_offset < result_count):
                time.sleep(1)
                request_uri_parameterized = f"{request_uri}?limit={result_limit}&offset={current_offset}&startdate={year_current}-01-01&enddate={year_current}-12-31&datasetid={datasetid}&stn_id={stn_id}"

                if extra_params:
                    request_uri_parameterized = f"{request_uri_parameterized}&{extra_params}"

                current_offset = current_offset + result_limit

                logger.debug(f"\tPulling for station {stn_id} for {year_current}")

                stations_resp = requests.get(request_uri_parameterized, headers=head)

                if stations_resp.status_code != 200:
                    logger.error(f"Error with request: {request_uri_parameterized}")
                    logger.error(stations_resp)
                    # We DONT want to kill the whole process
                    #raise ValueError(f"Error obtaining {entity_desc} list")

                current_results = stations_resp.json()

                # Only process non-empty requests
                if "metadata" not in current_results:

                    no_results = True
                    logger.debug(f"\tPulling for station {stn_id} for {year_current}: no results")
                else:

                    result_count = current_results["metadata"]["resultset"]["count"]

                    current_batch_results = current_results["results"]
                    list_obtained.extend(current_batch_results)

                    logger.debug(f"\tPulling for station {stn_id} for {year_current}: {len(list_obtained)} total results")

        logger.info(f"Pulling for station {stn_id}, readings from {year_start}-{year_end}, location: {stn_name}, completed with {len(list_obtained)} readings")

        # Write CSV to disk
        logger.debug(f"Writing completed pull for station {stn_id} to {out_file_csv}")
        with open(out_file_csv, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=field_list, delimiter="|")
            dict_writer.writeheader()
            dict_writer.writerows(list_obtained)

    except Exception as err:
        logger.error(f"ERROR: Exception encountered on pull for station {stn_id}")
        logger.error(err)
        traceback.print_exc()

    cdo_tokens.put(license_key)

    return list_obtained

def get_climate_timeseries(stn_id):

    request_uri = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    data_fields = ["date", "datatype", "station", "attributes", "value"]

    if not stn_id.startswith("GHCND"):
        logger.warn(f"Skipping pull for non-GHCND station {stn_id}")
        return

    year_min = STATION_LOOKUP[stn_id]["year_min"]
    year_max = STATION_LOOKUP[stn_id]["year_max"]

    get_timeseries_batched(entity_desc="Daily Summaries",
                           datasetid="GHCND",
                           stn_id=stn_id,
                           year_start=year_min,
                           year_end=year_max,
                           request_uri=request_uri,
                           out_file_json=f"data_extracts_multiworker/{stn_id.replace(':','_')}.json",
                           out_file_csv=f"data_extracts_multiworker/{stn_id.replace(':','_')}.csv",
                           field_list=data_fields,
                           extra_params=None)

def get_list_batched(entity_desc, request_uri, out_file_json, out_file_csv, field_list, extra_params=None):

    result_count = 1000000 # does not matter atm, offset of 0 will always dominate
    current_offset = 0
    result_limit = 1000

    list_obtained = []

    print(f"Looping through list of {entity_desc}")
    print(f"Current Offset: {current_offset}")
    print(f"Result Limit: {result_limit}")
    print(f"Result Count: {result_count}")

    while current_offset < result_count:

        request_uri_parameterized = f"{request_uri}?limit={result_limit}&offset={current_offset}"
        if extra_params:
            request_uri_parameterized = f"{request_uri_parameterized}&{extra_params}"

        current_offset = current_offset + result_limit

        stations_resp = requests.get(request_uri_parameterized, headers=head)

        if stations_resp.status_code != 200:
            print(stations_resp)
            raise ValueError(f"Error obtaining {entity_desc} list")

        print(stations_resp.json())
        current_results = stations_resp.json()
        result_count = current_results["metadata"]["resultset"]["count"]


        current_batch_results = current_results["results"]
        list_obtained.extend(current_batch_results)
        print()
        print("------------------------")
        print(f"Completed pull via: {request_uri_parameterized}")
        print(current_results["metadata"])
        print(f"Successfully obtained another batch of {len(current_batch_results)} {entity_desc}")
        print(f"We now have data for {len(list_obtained)} {entity_desc} total")
        print("Current Batch:")
        for cbr in current_batch_results:
            print( cbr)

        print("Looping")
        print(f"Current Offset: {current_offset}")
        print(f"Result Limit: {result_limit}")
        print(f"Result Count: {result_count}")

    print()
    print()
    print(f"Pull Complete, total stations extracted: {len(list_obtained)}")

    # Write JSON to disk
    with open(out_file_json, 'w') as f:
        json.dump(list_obtained, f)

    # Write CSV to disk
    with open(out_file_csv, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=field_list, delimiter="|")
        dict_writer.writeheader()
        dict_writer.writerows(list_obtained)

    return list_obtained

def get_station_list():
    STATIONS_URI = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
    station_fields=["elevation", "mindate", "maxdate", "latitude", "name", "datacoverage", "id", "elevationUnit", "longitude"]

    _ = get_list_batched(entity_desc = "stations",
                         request_uri=STATIONS_URI,
                         out_file_json="stations.json",
                         out_file_csv="stations.csv",
                         field_list=station_fields,
                         extra_params="extent=37.28,-122.6,38.28,-121.83")
    '''
    extent is a string of the form "lat_lo,lng_lo,lat_hi,lng_hi" for this bounds,
        where "lo" corresponds to the southwest corner of the bounding box,
        while "hi" corresponds to the northeast corner of that box.
        see: https://developers.google.com/maps/documentation/javascript/reference/coordinates#LatLngBounds.toUrlValue
    '''

def main():

    #get_station_list()

    # Prepare License Key(s)
    with open(TOKEN_FILE) as fh_token:
        for tkn in fh_token.readlines():
            cdo_tokens.put(tkn.strip())

    tasq = []

    with open("station_ids_of_interest.csv") as soifile:
        reader = csv.DictReader(soifile, delimiter="|", fieldnames=["stn_id", "year_min", "year_max", "stn_name"])
        for stindex, row in enumerate(reader):
            stn_id = row["stn_id"]
            STATION_LOOKUP[stn_id] = {}
            STATION_LOOKUP[stn_id]["year_min"] = int(row["year_min"])
            STATION_LOOKUP[stn_id]["year_max"] = int(row["year_max"])
            STATION_LOOKUP[stn_id]["stn_name"] = row["stn_name"]
            tasq.append(stn_id)

    # Size the pool based on available token(s)
    pool_size = cdo_tokens.qsize()

    logger.info(f"Running with {pool_size} workers")
    p = Pool(cdo_tokens.qsize())
    p.map(get_climate_timeseries, tasq)


if __name__ == "__main__":
    main()