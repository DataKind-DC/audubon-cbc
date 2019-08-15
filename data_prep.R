library(tidyverse)
library(lubridate)

setwd("../Desktop")

# The goal of this file is to load the raw Audobon data,
# `cbc_effort_weather_1900-2018.csv` and then clean, recode,
# and reformat the data for further processing.


# First, read the file, setting most of the columns to specific types.
# Try to fix any readr::read_csv format warnings like:
#
#   Warning: 6559 parsing failures.
#   row       col               expected actual                               file
#   60909 min_temp  no trailing characters     .5 'cbc_effort_weather_1900-2018.csv'
# 
# In this case, the problem was that the 'min_temp' column was formatted as an integer,
# `col_integer()`, while data contained values that looked like Numbers or floats (0.5).
# Changing `min_temp=col_integer()` to `min_temp=col_float()` let `read_csv()` correctly
# load the column, eliminating the format warnings
raw <- readr::read_csv(
  "cbc_effort_weather_1900-2018.csv",
  col_types=cols(
    feeder_hours=col_number(),
    n_feeder_counters=col_number(),
    
    n_field_counters=col_number(),
    field_distance=col_number(),
    field_hours=col_number(),
    
    min_temp=col_number(),
    max_temp=col_number(),
    temp_unit=col_character(),
    
    min_snow=col_number(),
    max_snow=col_number(),
    am_snow=col_character(),
    pm_snow=col_character(),
    snow_unit=col_integer(),
    
    min_wind=col_number(),
    max_wind=col_number(),
    wind_unit=col_integer(),
    
    am_cloud=col_number(),
    pm_cloud=col_number(),
    
    am_rain=col_character(),
    pm_rain=col_character(),
    
    nocturnal_hours=col_number(),
    nocturnal_distance=col_number(),
    
    min_field_parties=col_integer(),
    max_field_parties=col_integer()
    )
  ) %>% select(
    circle_name,
    country_state,
    lat,
    lon,
    count_year,
    count_date,
    
    feeder_hours,
    n_feeder_counters,
    
    n_field_counters,
    min_field_parties,
    max_field_parties,
    field_hours,
    field_distance,
    nocturnal_hours,
    nocturnal_distance,
    distance_units,
    
    min_temp,
    max_temp,
    temp_unit,
    
    min_snow,
    max_snow,
    am_snow,
    pm_snow,
    snow_unit,
    
    min_wind,
    max_wind,
    wind_unit,
    
    am_cloud,
    pm_cloud,
    
    am_rain,
    pm_rain,
  
    everything()
  )


# Filter rows to just those in the US
data <- raw %>%
  filter(str_detect(country_state, 'US-'))

# Add circle identifier
data <- data %>%
  mutate(
    # Identify circles uniquely based on name and state.
    # Names can be reused: e.g. "Abilene" was a circle in Kansas
    # for 1905 and 1906, but then a circle named "Abilene" was made
    # in Texas in 1960 and continues to today.
    circle_id = paste(circle_name, country_state, sep="_")
  ) %>%
  select(circle_id, everything())

# =================================
# Data profiling
# =================================
summary(data$count_year)
unique(data$country_state)

filtered <- data %>% filter(count_year > 2017)

d2 <- data %>%
  group_by(circle_name) %>%
  summarise(count=n_distinct(country_state), 
            count_lat_long=n_distinct(paste(as.character(lat), as.character(lon))))

d3 <- data %>%
  group_by(circle_name, country_state) %>% summarise(count=n())

write_csv(d2, 'tmp.csv')

?read_csv
