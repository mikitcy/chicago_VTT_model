**Model instructions**
-
This Project consists of the following contents:

1. Input JSON files
- Input JSON files for social externalities and private costs (see SI for sources)

2. Functions files

- Cost: Functions to calculation for TNC and transit externalities
- Google_search: Functions to search transit route through API. Please add your API key here.
- Tools: Basic functions for running models
- Trip_data_clean: Functions to clean the raw data downloaded from Chicago Data Portal and add analysis

3. Workspace files (Please run the model here)

- 01 Preparation: Clean the downloaded file and sample trips for the further analysis
- 02 Direction data: Run Google Directions API and obtain transit direction related data
- 03 Analysis: Run the analysis to get the breakeven value of traveltime and externalities
- 04 Plotting: Further plotting used in the published paper

**Raw Data**
- 
The following data is downloaded from external data portal and used in this model as csv files.

- TNC trip data: Downloaded from Chicago Data Portal
  - URL: https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips-2023-/n26f-ihde/about_data
- Community Area income data: Downloaded from Census Stats Data Portal. It was downloaded in census tract level data, and we calculated CA level values by getting weighted average of census tract population
  - URL: https://data.census.gov/
- Weather data: Downloaded from NOAA Storm Events Database (https://www.ncdc.noaa.gov/stormevents/)