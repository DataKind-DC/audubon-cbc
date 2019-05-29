# audubon-cbc
"For the bird counters"

The general questions we are trying to answer are, "what are the geographic, socioeconomic, or climatic correlates of different types of CBC participation and effort? Is it possible to model and predict participation and effort?".  Keep in mind that some years, counts could be cancelled due to nasty weather. There will not be a record for that count during that year.  Field counters, parties, hours, and distances make up the largest chunks of effort and are the most interesting to us.

### Data

Data with columns in imperial and metric units avaiable here: 

[bird_count_cleaned_may_29_2019.csv](bird_count_cleaned_may_29_2019.csv)


All the numeric values appear to possible (perhaps with exception of the maximum number of hours for some tasks. 

Note that impossible values for derived columns with _imperial_ and _metric_ suffixes were replaced with NaN. The original column values were not replaced (e.g. max_wind wasn't replaced). 

Outliers remain.

Also note that missing values were not imputed. Depending upon the variable of interest and the analysis, missing values might want to be treated various ways.


### Resources
Read these brief pages for background:
https://www.audubon.org/conservation/join-christmas-bird-count
https://www.audubon.org/christmas-bird-count-compiler-resources
http://www.audubon.org/sites/default/files/documents/updated_compilers_manual_jan_2013.pdf

Some column descriptions here (not comprehensive):
http://www.audubon.org/sites/default/files/documents/cbc_report_field_definitions_2013.pdf

Note the weather columns are often not absolutes. Excerpt:

MIN_TEMP - Low temp of the count day to the nearest degree, in degrees F
MAX_TEMP - High temp of the count day to nearest degree in F
MIN_WIND - Representative lower range of wind speed on count day; this is not the minimum wind speed observed on the count day; stored in MPH
MAX_WIND - Representative upper range of wind speed on count day; this is not the max wind speed observed on the count day; stored in MPH
MIN_SNOW - Representative lower range for snow depth, reported to the nearest 0.25 inches; reported as 0 if there was no snow; stored in inches
MAX_SNOW - Representative upper range for snow depth, reported to the nearest 0.25 inches;
reported as 0 if there was no snow; stored in inches
