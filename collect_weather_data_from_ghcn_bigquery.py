"""
Collect Weather Data from GHCN 
Author: Francisco Vannini 
Date: 2020-01-29

Requires: 
Google Project - For more information see : https://cloud.google.com/bigquery/docs/authentication/

Inputs:
cbc_cleaned_usa_statid.csv - csv file of cleaned cbc data matched with closest station id 

Outputs: 
flatten_data_from_<DATE>.csv - csv file of Percipitation, Temp low, Temp high and station ID and yer 

"""
import pandas as pd # Read in unfinished dataset
from google.cloud import bigquery
from google.cloud.bigquery.job import LoadJobConfig, WriteDisposition, CreateDisposition
import pandas as pd


# Change this to the PATH of your cbc_cleaned_usa_statid station
df_shell = pd.read_csv('C:\\Users\\Frankie-Figz\\Downloads\\cbc_cleaned_usa_statid.csv')
# Find the required dates and station ids 
station_list = df_shell.loc[:, 'closest_station_id'].unique()
date_list = df_shell.loc[:,'count_date'].unique()
# Format the dates and stations ids as to be acceptable to the query that will later be formed
string_parameter_stations  = ""
seperator = ' \',\' '
string_parameter_stations = seperator.join(station_list)
string_parameter_stations = "(\'" + string_parameter + "\')"
string_parameter_stations = string_parameter.replace(" ", "")
string_parameter_dates = ""
string_parameter_dates = seperator.join(date_list)
string_parameter_dates = "(\'" + string_parameter_dates + "\')"
string_parameter_dates = string_parameter_dates.replace(" ", "")


# This is the name of your google project. It is related to the key you use to register with google API services
# For more information see : https://cloud.google.com/bigquery/docs/authentication/
PROJECT='fjvr-testing'  # CHANGE THIS TO YOUR PROJECT 


# Create the date frame that will be used to accumulate the results from each year
df = pd.DataFrame(columns=['date','id','name','precipitation_value','state','temp_max_value','temp_min_value'])
# Instantiate a big query object
bq = bigquery.Client(project=PROJECT)
# The initial date and final date that the query will use to retrieve data
initial_year = 2018
final_year = 2019
#A table for every year of observations is used in the NOAA dataset.
# For each year we query the dataset and thus have to reformulate the table name
# list tables in the big query GHCN dataset
tables = bq.list_tables("bigquery-public-data.ghcn_d")
# Iterates over all tables in the bigquery-public-data.ghcn_d datasets and only takes the once that have a year as the last 4 digits.
for table in tables:
    try:
        if int(table.table_id[-4:]) >= initial_year and int(table.table_id[-4:]) <= final_year:
            # Constructs a query to flatten data. Here we are doing a SELF-JOIN (see examples online if neccesary) to extract the attributes of interest
            query = """
            SELECT DISTINCT
              base.id, 
              base.date,
              stations.name,
              stations.state,
              temp_min.value as temp_min_value,
              temp_max.value as temp_max_value,
              precipitation.value as precipitation_value
            FROM {} base
            INNER JOIN {} temp_min ON base.id = temp_min.id AND base.date = temp_min.date
            INNER JOIN {} temp_max ON base.id = temp_max.id AND base.date = temp_max.date
            INNER JOIN {} precipitation ON base.id = precipitation.id AND base.date = precipitation.date
            INNER JOIN `bigquery-public-data`.ghcn_d.ghcnd_stations stations ON base.id = stations.id
            WHERE temp_min.element = 'TMIN' AND temp_max.element = 'TMAX' AND precipitation.element = 'PRCP' AND stations.id IN {} AND base.date IN {}
            ORDER BY base.id, base.date
            """
            # This parameter is determined baased on the current year we are iterating over
            parameter = "`bigquery-public-data`.ghcn_d." + table.table_id
            # The format function replaces instances of {} with the corresponding sequential input
            query = query.format(parameter,parameter,parameter,parameter,string_parameter_stations, string_parameter_dates)
            # Queries BigQuery public data set and creates a new dataframe object
            df_temp = bq.query(query).to_dataframe()
            # Appends the dataframe object to accumulated data frame
            df = df.append(df_temp)
    except:
        pass
# Change the PATH relative to you
df.to_csv(r'C:\\Users\\Frankie-Figz\\Documents\\code-space\\audubon-cbc\\datasets\\flatten_data_from_' + str(initial_year) + '_to_' + str(final_year) + '.csv')

