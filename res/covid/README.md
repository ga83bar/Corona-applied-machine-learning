# README for the Covid dataset

## Data origin
This data is loaded by the API api.covid19api.com (loaded on: 23.june 2020 ) it contains the data for each country (see [countrylist](/src/data_management/data_collection.py). The attributes of the raw data are Country, CountryCode, Province, City, CityCode, Lat, Lon ,Confirmed, Deaths, Recovered, Active and Date. From this data we just want to keep and preprocess the attributes Confirmed, Deaths, Recovered, Active and Date.

## Code for obtaining and preprocessing
All code can be found in the [CovidCollector](/src/data_management/data_collection.py) class.


