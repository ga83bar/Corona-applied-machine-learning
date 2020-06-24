"""
This class serves as the interface between the data selection CLI and the necessary
data collection APIS.
"""
import os
from datetime import timedelta as t_delta
import logging
import pandas as pd

from requests import get
from matplotlib import pyplot as plot

# Error Codes
COUNTRY_REQUEST_FAILED = 'REQUEST STATUS {}: {}'
INVALID_REQUEST = 'REQUEST INVALID'

# Date constants
DATE_SRT = '2019-01-01T00:00:00Z'
DATE_END = '2020-06-20T00:00:00Z'

# APIs
API_COVID_COUNTRY = 'https://api.covid19api.com/live/country/{}/status/confirmed/date/' + DATE_SRT
API_COVID_WORLD = 'https://api.covid19api.com/world?from=' + DATE_SRT + '&to=' + DATE_END

# Top 60 Countries, Cases / 1M, Tot. Cases > 2000
REGIONS = ['Europe', 'Asia', 'MiddleEast', 'Africa', 'SouthAmerica', 'NorthAmerica']
EUROPE = ['Poland', 'Italy', 'Turkey', 'Finland', 'Denmark', 'Czechia', 'Romania', 'Norway',
          'Serbia', 'Austria', 'Russia', 'Germany', 'Portugal', 'France', 'Switzerland',
          'Netherlands', 'Luxembourg', 'Armenia', 'Spain', 'Belarus', 'Sweden', 'Belgium',
          'Ireland', 'UK', 'England']
ASIA = ['Singapore', 'China', 'Bangladesh']
MIDDLEEAST = ['Kasakhstan', 'Israel', 'Quatar', 'Bahrain', 'Kuwait', 'Oman', 'UAE',
              'Saudi Arabia', 'Iran']
AFRICA = ['South Africa', 'Egypt', 'Ghana', 'Haiti', 'Senegal']
SOUTHAMERICA = ['Chile', 'Peru', 'Brazil', 'Ecuador', 'Bolivia', 'Colombia']
NORTHAMERICA = ['USA', 'Panama', 'Canada', 'Dominican Republic', 'Mexico', 'Honduras']


class DataCollection():
    """This class is responsible for collecting raw data from div databases or API`s"""

    def __init__(self, logging_level=logging.INFO):
        self.get_covid_data(EUROPE)
        logging.basicConfig(filename='data_collection.log', level=logging_level)

    def get_all_data(self):
        """ Returns all Data"""

    def get_covid_data(self, countries, save_frame=True, do_plot=False):
        """ Return only Covid Data"""
        country_pd_frames = [self.__covid_request(country) for country in countries]
        self.__handle_result(country_pd_frames, save_frame, do_plot)
        return country_pd_frames

    def get_covid_data_all(self, save_frame=True, do_plot=False):
        """ Generate list of all countries and fetch data"""
        countries = EUROPE + ASIA + MIDDLEEAST + AFRICA + NORTHAMERICA + SOUTHAMERICA + NORTHAMERICA
        country_pd_frames = [self.__covid_request(country) for country in countries]
        self.__handle_result(country_pd_frames, save_frame, do_plot)
        return country_pd_frames

    def get_covid_data_world(self, save_frame=True, do_plot=False):
        """ Fetch worldwide corona totals"""
        world = ["world"]
        world_pd_frame = [self.__covid_request(world)]
        self.__handle_result(world_pd_frame, save_frame, do_plot)
        return world_pd_frame

    def __covid_request(self, country):
        """ Return Covid data for requested country"""
        covid_request = get(API_COVID_COUNTRY.format(country))
        if covid_request.status_code == 200:
            frame = pd.read_json(covid_request.text)
        else:
            print(COUNTRY_REQUEST_FAILED.format(country, covid_request.status_code))
            raise Exception(INVALID_REQUEST)
        return [country, frame]

    def __handle_result(self, dataframes, save_frame=False, do_plot=False):
        """ Save and/or plot data as per user defined"""
        if save_frame:
            for frame in dataframes:
                if not frame[1].empty:
                    folder_path = ('./res/covid/raw/{}').format(frame[0])
                    if os.path.exists(folder_path):
                        pass
                    else:
                        os.makedirs(folder_path)

                    # _ = frame[1].to_pickle(("./res/covid/raw/{}/covid19_{}.pkl").format(frame[0], frame[0]))
                    _ = frame[1].to_csv(("./res/covid/raw/{}/covid19_{}.csv").format(frame[0], frame[0]))
            logging.info('Saved raw covid data in folders')

        if do_plot:
            for frame in dataframes:
                if not frame[1].empty:
                    frame[1].plot(kind='line', title=frame[0], x='Date', y=['Confirmed', 'Deaths', 'Active'])
                    plot.show()

    def __val_source_data(self):
        """ Validate raw Data for Completeness"""
        raise NotImplementedError

    def __get_date_list(self):
        """ Gen list of all dates between start and end date"""
        date_list = [DATE_SRT + t_delta(days=x) for x in range(0, (DATE_END - DATE_SRT).days)]
        return date_list


class CovidDataCollection:
    '''This class is responsible for Covid data collection.
    It loads the data from This data is loaded by the API api.covid19api.com.
    it contains the data for each country of our worldlist
    (see [countrylist](/src/datamanagement/datacollection.py).
    The attributes attributes of the raw data are:
    Country, CountryCode, Province, City, CityCode, Lat, Lon ,
    Confirmed, Deaths, Recovered, Active and Date.
    From this data we just want to keep and preprocess the att. Confirmed, Deaths, Recovered, Active and Date.'''

    def __init__(self, logging_level=logging.INFO):
        logging.basicConfig(filename='data_collection.log', level=logging_level)

    def __load_covid(self, countries, save_frame=True, do_plot=False):
        """ Return only Covid Data"""
        country_pd_frames = [self.__covid_request(country) for country in countries]
        self.__handle_result(country_pd_frames, save_frame, do_plot)
        return country_pd_frames

    def __load_covid_all(self, save_frame=True, do_plot=False):
        """ Generate list of all countries and fetch data"""
        countries = EUROPE + ASIA + MIDDLEEAST + AFRICA + NORTHAMERICA + SOUTHAMERICA + NORTHAMERICA
        country_pd_frames = [self.__covid_request(country) for country in countries]
        self.__handle_result(country_pd_frames, save_frame, do_plot)
        return country_pd_frames

    def get_covid_data_world(self, save_frame=True, do_plot=False):
        """ Fetch worldwide corona totals"""
        world = ["world"]
        world_pd_frame = [self.__covid_request(world)]
        self.__handle_result(world_pd_frame, save_frame, do_plot)
        return world_pd_frame

    def __covid_request(self, country):
        """ Return Covid data for requested country"""
        covid_request = get(API_COVID_COUNTRY.format(country))
        if covid_request.status_code == 200:
            frame = pd.read_json(covid_request.text)
        else:
            print(COUNTRY_REQUEST_FAILED.format(country, covid_request.status_code))
            raise Exception(INVALID_REQUEST)
        return [country, frame]

    def __handle_result(self, dataframes, save_frame=False, do_plot=False):
        """ Save and/or plot data as per user defined. This method also drops unimportant data."""
        if save_frame:
            for frame in dataframes:
                if not frame[1].empty:
                    raw_folder_path = os.path.join('.', 'res', 'covid', 'raw', str(frame[0]))
                    proc_folder_path = os.path.join('.', 'res', 'covid', 'processed', str(frame[0]))
                    # pandas does not create these folders check if they exist
                    if os.path.exists(raw_folder_path):
                        pass
                    else:
                        os.makedirs(raw_folder_path)

                    if os.path.exists(proc_folder_path):
                        pass
                    else:
                        os.makedirs(proc_folder_path)

                    # _ = frame[1].to_pickle(("./res/covid/raw/{}/covid19_{}.pkl").format(frame[0], frame[0]))
                    path_raw = os.path.join(raw_folder_path, 'covid19_{}.csv'.format(frame[0]))
                    path_processed = os.path.join(proc_folder_path, 'covid19_{}.csv'.format(frame[0]))

                    _ = frame[1].to_csv(path_raw)
                    # get the country code of the country
                    if not frame[1].empty:
                        country_code = frame[1]['CountryCode'][0]
                    # erase unimportant data
                    reduced_frame = frame[1].drop(columns=['Country', 'CountryCode', 'Province',
                                                           'City', 'CityCode', 'Lat', 'Lon'])
                    # rename the collumns (important if we merge these frames in one big frame)
                    reduced_frame.columns = ['{}_Confirmed'.format(country_code),
                                             '{}_Deaths'.format(country_code),
                                             '{}_Recovered'.format(country_code),
                                             '{}_Active'.format(country_code),
                                             'Date']

                    _ = reduced_frame.to_csv(path_processed)
            logging.info('Saved raw and processedcovid data in folders')

        if do_plot:
            for frame in dataframes:
                if not frame[1].empty:
                    frame[1].plot(kind='line', title=frame[0], x='Date', y=['Confirmed', 'Deaths', 'Active'])
                    plot.show()

    def get_covid_data(self, reload=False):
        '''
        Method loads processed data stored in ./res/covid/processed in one frame.
        '''
        if reload:
            self.__load_covid_all()

        root_directory = os.path.join('.', 'res', 'covid', 'processed')

        # implement some wired stuff where we iterate over the folders
        df_covid = pd.DataFrame()
        df_tmp = pd.DataFrame()
        for subdir, _, files in os.walk(root_directory):
            for file in files:
                path_to_single_country = os.path.join(subdir, file)
                logging.debug(path_to_single_country)

                if df_covid.empty:
                    df_covid = pd.read_csv(path_to_single_country)
                    df_covid = df_covid.set_index('Date')
                    # print(df_covid)
                else:
                    df_tmp = pd.read_csv(path_to_single_country)
                    df_tmp = df_tmp.set_index('Date')

                # merge the two frames
                if not df_tmp.empty:
                    df_covid = df_covid.merge(df_tmp)

        path_all = os.path.join('.', 'res', 'covid', 'all.csv')
        df_covid.to_csv(path_all)
        return df_covid


COVIDCOL = CovidDataCollection()
COVIDCOL.get_covid_data(reload=True)
