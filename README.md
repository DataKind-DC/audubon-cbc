# audubon-cbc
"For the bird counters"

The general questions we are trying to answer are, "what are the geographic, socioeconomic, or climatic correlates of different types of CBC participation and effort? Is it possible to model and predict participation and effort?".  Keep in mind that some years, counts could be cancelled due to nasty weather. There will not be a record for that count during that year.  Field counters, parties, hours, and distances make up the largest chunks of effort and are the most interesting to us.

# Research Questions: 
__1. What relationship, if any, exsists between geographic, socioeconomic, or climatic correlates features and CBC participation and effort for the chirstmas birdcouter?__

  Volenteers For this Research Question will produce descriptive anaylsis and predictive modeling to examine if a relationship can be determined.
  
 __2. Should the Audubon society continue to collect weather data during the Christmas Bird Count?__ 
 
   Volenteers will 1) Examine the weather data avilible in the cbc data for completness and trends, 2) connected with a source of weather data (NOAA has been suggested) to determine the past accuraccy of weather data recorded by particpants, 3) make a determination on if weather data provided by cbc participants is valuble to collect. 


## Volenteer Quick Start for June 13th 
1) Access the Most Current Data Here:
[bird_count_cleaned_may_29_2019.csv](bird_count_cleaned_may_29_2019.csv)
Data Dictonary: 
http://www.audubon.org/sites/default/files/documents/cbc_report_field_definitions_2013.pdf

2) If a python user, Clone and branch your own copy of the ipython notebook used to clean the data:
https://github.com/DataKind-DC/audubon-cbc/blob/master/audubon_eda.ipynb (audubon_eda.ipynb)

### Progress So Far
DataKind has collected data from the Audobon Socity and did a pass at cleaning the data. The cleaned Data can be found here:

[bird_count_cleaned_may_29_2019.csv](bird_count_cleaned_may_29_2019.csv)
Notes from Data Cleaning: 
- All the numeric values appear to possible (perhaps with exception of the maximum number of hours for some tasks. 
- Note that impossible values for derived columns with _imperial_ and _metric_ suffixes were replaced with NaN. The original column values were not replaced (e.g. max_wind wasn't replaced). 
- Outliers remain.
- Also note that missing values were not imputed. Depending upon the variable of interest and the analysis, missing values might want to be treated various ways.

# Known Next Steps 
### - Data Cleaning 
The previous Team of Volenteers has left a todo list to finish cleaning the cbc data
  TODOS:
  
  - Numeric data (temperature, snow, wind, distance):
    - Convert to same unit
    - Impute missing values
    - Standardize/normalize
  
  - For categorical data:
    - Encode appropriately
    - Composites -> if no 4 then take average and treat as new category, 4 trumps all
  - Age of circles - older circles are more numerous
    - Any outliers for these
  
  - Open Questions:
    - what does snow_unit stand for?
    - What should we do with outliers for snow
    - what is wind unit? direction?
    - Suggestion: remove large outliers?
    - What are temperature units

###  - Weather Data API 
  For the weather data, DataKind needs to understand what weather data is avilible for the past based on lat long data (that we have from the cbc data file)
  
  It would be benificall to have volenteers research NOAA data and build an example of how to get temprature, percpipation? Parcipitation? (rain and snow data) and wind data via API and save that info in a ipython notebook or script. 
  
### - Decriptive and Model Design 
Given the data types and research questions for the Particpation Research Question, it would be benifical to have volenteers design table shells for metrics that would help answer the research question and model designs they would like to see implemented. These shells and designs should include notes on any data aggrgations or transformations that would be required by a tech side. 
  


# Most Current Data

Data with columns in imperial and metric units avaiable here: 

[bird_count_cleaned_may_29_2019.csv](bird_count_cleaned_may_29_2019.csv)

Data Dictonary: 
http://www.audubon.org/sites/default/files/documents/cbc_report_field_definitions_2013.pdf

- All the numeric values appear to possible (perhaps with exception of the maximum number of hours for some tasks. 
- Note that impossible values for derived columns with _imperial_ and _metric_ suffixes were replaced with NaN. The original column values were not replaced (e.g. max_wind wasn't replaced). 
- Outliers remain.
- Also note that missing values were not imputed. Depending upon the variable of interest and the analysis, missing values might want to be treated various ways.


# Resources
Read these brief pages for background:

https://www.audubon.org/conservation/join-christmas-bird-count

https://www.audubon.org/christmas-bird-count-compiler-resources

http://www.audubon.org/sites/default/files/documents/updated_compilers_manual_jan_2013.pdf

Some column descriptions here (not comprehensive):
http://www.audubon.org/sites/default/files/documents/cbc_report_field_definitions_2013.pdf

Note the weather columns are often not absolutes. Excerpt:

- MIN_TEMP - Low temp of the count day to the nearest degree, in degrees F
- MAX_TEMP - High temp of the count day to nearest degree in F
- MIN_WIND - Representative lower range of wind speed on count day; this is not the minimum wind speed observed on the count day; stored in MPH
- MAX_WIND - Representative upper range of wind speed on count day; this is not the max wind speed observed on the count day; stored in MPH
- MIN_SNOW - Representative lower range for snow depth, reported to the nearest 0.25 inches; reported as 0 if there was no snow; stored in inches
-MAX_SNOW - Representative upper range for snow depth, reported to the nearest 0.25 inches;
reported as 0 if there was no snow; stored in inches
