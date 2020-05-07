## Background
"For the Bird Counters"

The general questions we are trying to answer are, "what are the geographic, socioeconomic, or climatic correlates of different types of CBC participation and effort? Is it possible to model and predict participation and effort?".  Keep in mind that some years, counts could be cancelled due to nasty weather. There will not be a record for that count during that year.  Field counters, parties, hours, and distances make up the largest chunks of effort and are the most interesting to us.


## Table of Contents
- [Team Members](#team-members)
- [Deliverables](#deliverables)
- [Data](#data)
- [Project Phases](#phases)

## Team Members
- Name of Member
  - Renzo
    - Data Ambassador
    - [rectheworld](https://github.com/rectheworld)
  - Minh Mai
     - Core Volunteer
     - [minh5](https://github.com/minh5)


## Deliverables
__1. What relationship, if any, exists between geographic, socioeconomic, or climatic correlates features and CBC participation and effort for the Christmas birdcounter?__

  Volunteers For this Research Question will produce descriptive analysis and predictive modeling to examine if a relationship can be determined.

Given the data types and research questions for the Participation Research Question, it would be beneficial to have volunteers design table shells for metrics that would help answer the research question and model designs they would like to see implemented. These shells and designs should include notes on any data aggregations or transformations that would be required by a tech side.

 __2. Should the Audubon society continue to collect weather data during the Christmas Bird Count?__

   Volunteers will
   - Examine the weather data available in the cbc data for completeness and trends
   - connect with a source of weather data (NOAA has been suggested) to determine the past accuracy of weather data recorded by participants
   - make a determination on if weather data provided by cbc participants is valuable to collect.

## Data

The data files are saved into google drive here: https://drive.google.com/drive/folders/1Nlj9Nq-_dPFTDbrSDf94XMritWYG6E2I

The raw Christmas Bird Count Data from the Audubon Socity is the file cbc_effort_weather_1900-2018.txt
Subsequent data files are named after the data the produced them.

### Onboarding

## Cleanest Volunteer Submitted Data
The file 1.0-rec-initial-data-cleaning.txt is the cleanest data to date and limits the scope to circles inside the United Stated and was produced by the 1.0-rec-initial-data-cleaning.ipynb file.

## Official Weather Date: Google BigQuery and Weather data
To obtain the daily measures of weather data, we will be using the GHCN Daily database powered by Google [here] (https://console.cloud.google.com/marketplace/details/noaa-public/ghcn-d?filter=solution-type:dataset&id=9d500d1d-fda4-4413-a789-d8786fd6592e&pli=1)"

Take a look around.
Of Note - each year of the dataset is divided into its own table. So 2019 data is in ghcn_2019.


#### Resources
Read these brief pages for background:

https://www.audubon.org/conservation/join-christmas-bird-count

https://www.audubon.org/christmas-bird-count-compiler-resources

http://www.audubon.org/sites/default/files/documents/updated_compilers_manual_jan_2013.pdf

Some column descriptions here (not comprehensive):
http://www.audubon.org/sites/default/files/documents/cbc_report_field_definitions_2013.pdf


#### Configuration
This is a primarily Python/R setup. Please follow the standard practices of setting up a virtualenv if using Python.

### Datasets
- [1.0-rec-initial-data-cleaning.txt.csv](1.0-rec-initial-data-cleaning.txt)
  - Latest data from the Audubon Society on their circle observation
  - Data Dictionary: http://www.audubon.org/sites/default/files/documents/cbc_report_field_definitions_2013.pdf
  - The notebook used to clean the data can be found [here](https://github.com/DataKind-DC/audubon-cbc/blob/master/notebooks/1.0-rec-initial-data-cleaning.ipynb)
  - All the numeric values appear to possible (perhaps with exception of the maximum number of hours for some tasks.
  - Note that impossible values for derived columns with _imperial_ and _metric_ suffixes were replaced with NaN. The original column values were not replaced (e.g. max_wind wasn't replaced).
  - Outliers remain.
  - Also note that missing values were not imputed. Depending upon the variable of interest and the analysis, missing values might want to be treated various ways.
  - Note the weather columns are often not absolutes. Excerpt:
    - MIN_TEMP - Low temp of the count day to the nearest degree, in degrees F
    - MAX_TEMP - High temp of the count day to nearest degree in F
    - MIN_WIND - Representative lower range of wind speed on count day; this is not the minimum wind speed observed on the count day; stored in MPH
    - MAX_WIND - Representative upper range of wind speed on count day; this is not the max wind speed observed on the count day; stored in MPH
    - MIN_SNOW - Representative lower range for snow depth, reported to the nearest 0.25 inches; reported as 0 if there was no snow; stored in inches
    - MAX_SNOW - Representative upper range for snow depth, reported to the nearest 0.25 inches;
    reported as 0 if there was no snow; stored in inches
- [Attic/noaa_stations_2020_01_17.csv.gz](Attic/noaa_stations_2020_01_17.csv.gz)
  - list of all NOAA stations and their associated metadata.
  - This is pulled from the NOAA API
- [Attic/closest_station_2020_01_20.csv.gz](Attic/closest_station_2020_01_20.csv.gz.csv)
  - Mapping of Audubon Circle and their closest NOAA station
  - used to determine the NOAA station and their weather readings for analysis
  - Special attention was given to making sure the station existed at least up until 2020-01-01
- [Attic/cbc_weather_effort_1900-2018.csv](files/cbc_weather_effort_1900-2018.csv)
  - Original data drop that has since been transformed to the above bird_count_cleaned_29_2019.csv

**Note:  Attic is now a repository for old data**

### Contributing
Anyone is able to contribute! Please follow the steps for a (hopefully) pain-free experience submitting a pull request (PR)
- First, clone the repo `git clone https://github.com/DataKind-DC/audubon-cbc.git`
- After that, create a new branch to work off of
  - you are free to name the branch however you like, however it is best to format it as `<purpose>/<name>`
    - where purpose can be `feature`, `debug`, `refactor`, or any other short form word to _describe_ the purpose of the PR
    - the `<name>` can be whatever you want to be
    - for example:
      - the name `feature/new_noaa_stations` will tell me this is a new feature regarding NOAA stations
      - the name `refactor/csv_parsing` will signal that this is a rewrite of a specific function of the repo
  - you can create a new branch with `git branch -b <purpose>/<name>`
- Get the data.  Go to this folder and download it: https://drive.google.com/drive/folders/1Nlj9Nq-_dPFTDbrSDf94XMritWYG6E2I
Paste it into the data folder in your local repository. The path should look like this: audubon-cbc/data/Cloud_Data/
- Work on the branch as you would normally, committing changes as you please. Use the example notebook [here](https://github.com/DataKind-DC/audubon-cbc/blob/master/notebooks/0.0-rec-example-notebook-with-header.ipynb) to set up your notebooks if you are creating a new notebook. 
- After you feel confident of your changes, head over to the [Pull Request](https://github.com/DataKind-DC/audubon-cbc/pulls) page
  and click on `New Pull Request`
- A page will show up with two field boxes with an arrow pointing from the right box to the left; this indicates the branch you are
  attempting to merge (right field) into the desired branch (left field)
  - for the right field, pick your branch, make sure you push up your changes first (`git push `)
- Follow the instructions and fill out the necessary information in the PR template
- Tag the appropriate person to review your work, see the [Team Member](#team-members) if you are unsure
- Your reviewer (should) provide feedback and you will make commits to your branch to reflect the necessary changes
- If all goes well, your reviewer will accept the PR and merge into master, CONGRATS!


#### Known Next Steps
Designing the Models
Look below on the onboarding steps for info on latest data and data sources.
We have Audubon Society submitted Volunteer weather data and an 'official' source of weather data.
  - TASK: We need to define how we will determine if these values are the 'same' or 'different'. Add the steps you will like to see happen to this ticket: Steps for Investigating If Weather Data is the 'Same'


The previous Team of Volunteers has left a todo list to finish cleaning the cbc data
  - Numeric data (temperature, snow, wind, distance):
    - Convert to same unit (Done!)
    - Impute missing values and Investigate Outliers
      - TASK: Need to investigate the Outliers and determine if they are most likely typos or data
    - Standardize/normalize
  - For categorical data:
    - TASK: Encode appropriately
       - Composites -> if no 4 then take average and treat as new category, 4 trumps all
    - TASK - Visualize the Weather data (Temp, Precipitation) over time
 Longitudinal Check
  - Age of circles - older circles are more numerous
    - TASK: Question: Should All circles be used or should we limit the circles in the final data set
  - Open Questions:
    - what does snow_unit stand for?
    - What should we do with outliers for snow
    - what is wind unit? direction?
    - Suggestion: remove large outliers?
    - What are temperature units

## Phases
Phases usually follow this lifecycle. It may vary from project to project but the general phases
- [Research and Design](#research-and-design)
- [Testing and Implementation](#testing-and-implementation)
- [Feedback and Wrap-up](#feedback-and-wrap-up)
