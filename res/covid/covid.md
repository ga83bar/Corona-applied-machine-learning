# README FOR COVID DATASET

## DATA ORIGIN
This data is loaded by the API api.covid19api.com (loaded on: 23.june 2020 ) it contains the data for each country. (see [countrylist](/src/datamanagement/datacollection.py) The attributes attributes of the raw data are Country, CountryCode, Province, City, CityCode, Lat, Lon ,Confirmed, Deaths, Recovered, Active and Date. From this data we just want to keep and preprocess the att. Confirmed, Deaths, Recovered, Active and Date.

## CODE FOR OBTAINING AND PREPROCESSING
[CovidCollector](/./src/data_management/data_collection.py)


