## Background
"For the Bird Counters"

The Christmas Bird Count is a tradition where each year bird enthusiasts gather during December-January for a one day bird counting extravaganza.  Volunteers gather for a single day to cover a 15 miles diameter circle and attempt to count every bird that they see. The count has only grown in locations and volunteers over its 100+ year history . 

The Audubon Society, which manages the Christmas Bird Count, has approach Data kind with two questions.

The primary question addressed by this repository is if volunteer submitted weather data is accurate and if Audubon should continue to expect volunteers to submit this data. 

The secondary questions we are trying to answer are, "What are the geographic, socioeconomic, or climatic correlates of different types of CBC participation and effort? Is it possible to model and predict participation and effort?".  (Keep in mind that some years, counts could be cancelled due to nasty weather. There will not be a record for that count during that year.  Field counters, parties, hours, and distances make up the largest chunks of effort and are the most interesting to us.)

As of the time of writing (September 2020) only work on the primary question has been done. 

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

- Hamza 
    - Volenteer and Analytics superstar
    - https://github.com/hamzaelsaawy
- Ian 
    - Volenteer and Data API wrangaler
    - hhttps://github.com/ijd5004
- Jacob Ellena 
    - Volenteer and Research and Analytics Enthusiant 
    - https://github.com/jellena
    
- Hamza 
    - Volenteer and Analytics Superstar
    - https://github.com/hamzaelsaawy
    
- Francisco J Vannini R
    - Volenteer and Google BigQuery Master
    - https://github.com/Frankie-Figz
    
- Nathan Pavlovic
    - Volenteer and ArcGIS Hero

## Deliverables
 __1. Should the Audubon society continue to collect weather data during the Christmas Bird Count?__

   Volunteers have to date:
   - Examined the weather data available in the cbc data for completeness and trends
   - Connected the cbc data with a source of weather data (NOAA ghcn_d database as provided by Google BigQuery) to determine the accuracy of weather data recorded by participants
   - Collected data on Elevation and Ecosystems for the cbc circles and the NOAA stations
   - Made a determination on if weather data provided by cbc participants is valuable to collect.

__2. (On Hold) What relationship, if any, exists between geographic, socioeconomic, or climatic correlates features and CBC participation and effort for the Christmas birdcounter?__

  Volunteers For this Research Question will produce descriptive analysis and predictive modeling to examine if a relationship can be determined.

Given the data types and research questions for the Participation Research Question, it would be beneficial to have volunteers design table shells for metrics that would help answer the research question and model designs they would like to see implemented. These shells and designs should include notes on any data aggregations or transformations that would be required by a tech side.

## Data

The data files are saved into google drive here: https://drive.google.com/drive/folders/1Nlj9Nq-_dPFTDbrSDf94XMritWYG6E2I

The raw Christmas Bird Count Data from the Audubon Socity is the file cbc_effort_weather_1900-2018.txt
Subsequent data files are named after the notebook that produced them.

### Onboarding

## Quick Start 

## Cleanest Volunteer Submitted Data
The file 1.0-rec-initial-data-cleaning.txt is the cleanest data to date and limits the scope to circles inside the United Stated and was produced by the 1.0-rec-initial-data-cleaning.ipynb file.  Always check to see if the files in Cloud Data have been updated since your last working session. 

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
 - [1.3-rec-connecting-fips-ecosystem-data.txt](1.3-rec-connecting-fips-ecosystem-data.txt)
   - The most up to date file containg cbc count weather data, noaa reference stations, elevation of cbc circles and noaa stations, ecosystem data for cbc circle and noaa reference stations. 
   - Each row is a cbc circle matched to a noaa reference station. A single cbc circle can be matched to multiple stations so a cbc count for a given year might appear multiple time (one for each noaa station they are matched to). 


**Note:  Attic is now a repository for old data**

## Quick Start and Contributing
### Quick Start
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
 - Work though the notebook [1.2-ijd-fetch-circle-elevations.ipynb](https://github.com/DataKind-DC/audubon-cbc/blob/master/notebooks/1.2-ijd-fetch-circle-elevations.ipynb "1.2-ijd-fetch-circle-elevations.ipynb") to understand the workflow of the notebooks.

### Before doing any work ... 
Use the example notebook [here](https://github.com/DataKind-DC/audubon-cbc/blob/master/notebooks/0.0-rec-example-notebook-with-header.ipynb) to set up your notebooks if you are creating a new notebook.  

This notebook will also provide an example of 1) How to structure your notebooks 2) Now to name your notebooks so they flow sequentially down the workflow and 3) how to name the output file. Output files will be named after the notebook that produced them.

If you are working on an issue, be sure to include the issue number in your commit messages. Example: "This is a commit message for issue #30". Using the #<Number> will autmatically tie your updates to the issue.

### Contributing
 - After you feel confident of your changes, head over to the [Pull Request](https://github.com/DataKind-DC/audubon-cbc/pulls) page
  and click on `New Pull Request`
 - A page will show up with two field boxes with an arrow pointing from the right box to the left; this indicates the branch you are
  attempting to merge (right field) into the desired branch (left field)
 - For the right field, pick your branch, make sure you push up your changes first (`git push `)
 - Follow the instructions and fill out the necessary information in the PR template
 - Tag the appropriate person to review your work, see the [Team Member](#team-members) if you are unsure
 - Your reviewer (should) provide feedback and you will make commits to your branch to reflect the necessary changes
 - If all goes well, your reviewer will accept the PR and merge into master, CONGRATS!

