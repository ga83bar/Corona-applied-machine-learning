"""
This class serves as the interface between the data selection CLI and the necessary
data collection APIS.
"""
import os
from datetime import timedelta as t_delta
import logging
from abc import ABCMeta, abstractmethod
import pandas as pd

from requests import get
from matplotlib import pyplot as plot
import matplotlib.dates as dates


# Date constants
DATE_SRT = '2020-02-01T00:00:00Z'
DATE_END = '2020-06-20T00:00:00Z'

# APIs https://api.covid19api.com/live/country/Poland/status/confirmed/date/2019-01-01T00:00:00Z
API_COVID_COUNTRY = 'https://api.covid19api.com/live/country/{}/status/confirmed/date/' + DATE_SRT
API_COVID_WORLD = 'https://corona-api.com/timeline'
API_COVID_DAY_ONE = 'https://api.covid19api.com/dayone/country/{}'  # need to add the country

# Top 60 Countries, Cases / 1M, Tot. Cases > 2000
# Whoever change these lists can pick up the beats from Michael Brandner ;-)
REGIONS = ['Europe', 'Asia', 'MiddleEast', 'Africa', 'SouthAmerica', 'NorthAmerica']
EUROPE = ['Poland', 'Italy', 'Turkey', 'Finland', 'Denmark', 'Czechia', 'Romania', 'Norway',
          'Serbia', 'Austria', 'Russia', 'Germany', 'Portugal', 'France', 'Switzerland',
          'Netherlands', 'Luxembourg', 'Armenia', 'Spain', 'Belarus', 'Sweden', 'Belgium',
          'Ireland', 'UK']  # , 'England'
ASIA = ['Singapore', 'China', 'Bangladesh']
MIDDLEEAST = ['Kazakhstan', 'Israel', 'Qatar', 'Bahrain', 'Kuwait', 'Oman', 'United Arab Emirates',
              'Saudi Arabia', 'Iran']
AFRICA = ['South Africa', 'Egypt', 'Ghana', 'Haiti', 'Senegal']
SOUTHAMERICA = ['Chile', 'Peru', 'Brazil', 'Ecuador', 'Bolivia', 'Colombia']
NORTHAMERICA = ['United States of America', 'Panama', 'Canada', 'Dominican Republic', 'Mexico', 'Honduras']


class DataCollection():
    """This class is responsible for collecting raw data from div databases or API`s"""

    def __init__(self, logging_level=logging.INFO):
        logging.basicConfig(filename='data_collection.log', level=logging_level)
        self.country_request_failed = 'REQUEST STATUS {}: {}'
        self.invalid_request = 'REQUEST INVALID'
        self.path = "./res/covid/raw/{}/covid19_{}.csv"

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
        world = "world"
        world_pd_frame = [self.__covid_request_world(world)]
        self.__handle_result(world_pd_frame, save_frame, do_plot)
        return world_pd_frame

    def __covid_request_world(self, world):
        """ Return time series of world data"""
        req = get(API_COVID_WORLD)
        if req.status_code == 200:
            frame = pd.read_json(req.text)
        else:
            loggign_str = self.country_request_failed.format(world, req.status_code)
            logging.error(loggign_str)
            raise Exception(self.invalid_request)
        return [world, frame]

    def __covid_request(self, country):
        """ Return Covid data for requested country"""
        covid_request = get(API_COVID_COUNTRY.format(country))
        if covid_request.status_code == 200:
            frame = pd.read_json(covid_request.text)
        else:
            loggign_str = self.country_request_failed.format(country, covid_request.status_code)
            logging.error(loggign_str)
            raise Exception(self.invalid_request)
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
                    _ = frame[1].to_csv((self.path).format(frame[0], frame[0]))
            logging.info('Saved raw covid data in folders')

        if do_plot:
            for frame in dataframes:
                if not frame[1].empty:
                    frame[1].plot(kind='line', title=frame[0], x='date', y=['Confirmed', 'Deaths', 'Active'])
                    plot.show()

    def __val_source_data(self):
        """ Validate raw Data for Completeness"""
        raise NotImplementedError


def __get_date_list():
    """ Gen list of all dates between start and end date"""
    date_list = [DATE_SRT + t_delta(days=x) for x in range(0, (DATE_END - DATE_SRT).days)]
    return date_list


class CovidCollector():
    '''This class is responsible for Covid data collection.
    It loads the data from the API api.covid19api.com.
    it contains the data for each country of our worldlist
    (see [countrylist](/src/datamanagement/datacollection.py).
    The attributesof the raw data are:
    Country, CountryCode, Province, City, CityCode, Lat, Lon ,
    Confirmed, Deaths, Recovered, Active and Date.
    From this data we just want to keep and preprocess the att. Confirmed, Deaths, Recovered, Active and Date.
    '''

    def __init__(self, logging_level=logging.INFO):
        logfile_path = os.path.join('.', 'res', 'covid', 'data_collection.log')
        logging.basicConfig(filename=logfile_path, level=logging_level)
        self.keep = 'dummy'
        self.invalid_request = 'REQUEST INVALID'
        self.country_request_failed = 'REQUEST STATUS {}: {}'

    def __load_covid_countries(self, countries, save_frame=True, do_plot=False):
        """ Return only Covid Data"""
        for country in countries:
            self.__covid_request(country, save_frame=save_frame, do_plot=do_plot)

    def __load_covid_all(self, save_frame=True, do_plot=False):
        """ Generate list of all countries and fetch data"""
        countries = EUROPE + ASIA + MIDDLEEAST + AFRICA + NORTHAMERICA + SOUTHAMERICA + NORTHAMERICA
        for country in countries:
            self.__covid_request(country, save_frame=save_frame, do_plot=do_plot)

    def __covid_request(self, country, save_frame=True, do_plot=False):
        """ Return Covid data for requested country"""
        # covid_request = get(API_COVID_COUNTRY.format(country))
        request_str = API_COVID_DAY_ONE.format(country)
        covid_request = get(request_str)
        if covid_request.status_code == 200:
            frame = pd.read_json(covid_request.text)
        else:
            raise Exception(self.invalid_request)
        self.__handle_result([country, frame], save_frame=save_frame, do_plot=do_plot)

    def __handle_result(self, frame, save_frame=True, do_plot=False):
        """ Save and/or plot data as per user defined. This method also drops unimportant data."""
        if save_frame:

            if not frame[1].empty:
                # replace space with underscore for files
                frame[0] = frame[0].replace(' ', '_')
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
            self.plot_country_frame(frame[1])

    def get_covid_data(self, reload=False):
        '''
        Method loads processed data stored in ./res/covid/processed in one frame containing all countries.
        Input: if reload is true we reload the data from API
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
                else:
                    df_tmp = pd.read_csv(path_to_single_country)
                    df_tmp = df_tmp.set_index('Date')

                # merge the two frames
                if not df_tmp.empty:
                    df_covid = pd.merge(df_covid, df_tmp)

        path_all = os.path.join('.', 'res', 'covid', 'all.csv')
        df_covid.to_csv(path_all)
        return df_covid

    def get_covid_data_country(self, country, reload=False):
        '''
        Method loads processed data stored in ./res/covid/processed in pandas frame.
        Attention: check spelling of the Country (like in res/covid/countryname)
        '''
        if reload:
            self.__load_covid_countries(country)

        country_file = os.path.join('.', 'res', 'covid', 'processed', str(country), 'covid19_{}.csv'.format(country))

        if os.path.exists(country_file):
            df_covid = pd.read_csv(country_file)
            df_covid = df_covid.set_index('Date')
        else:
            raise Exception('Country is not valid {}'.format(country))

        return df_covid

    def plot_country_frame(self, frame):
        '''
        Plots the most important covid data (Confirmed, Deaths, Recovered, Active)over time.
        Input is the dataframe loaded with get_covid_data_country('Country')
        '''
        self.keep = "plot_keeper"
        if not frame.empty:
            frame.plot(x_compat=True, kind='line', title='Covid data single country')
            plot.gca().xaxis.set_major_locator(dates.DayLocator())
            plot.gca().xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))
            plot.show()


class ICollector(metaclass=ABCMeta):
    '''
    Simple interface to define basic functions.
    '''
    def __init__(self, path_name):
        self.source = None
        self.path_to_raw = None
        self.path_to_processed = None
        self.csv_name = None
        self.name = path_name
        _ = self.__get_paths(path_name)

    def __get_paths(self, name):
        '''
        Sets the paths to the raw and processed folders.
        Input should be a string similar to the naming in the res folder e.g 'pornhub'
        '''
        # check if name object is string
        if isinstance(name, str):
            path_to_res = os.path.join('.', 'res')
            self.path_to_raw = os.path.join(path_to_res, str(name), 'raw')
            self.path_to_processed = os.path.join(path_to_res, str(name), 'processed')

            # create folders if they does not exist
            if not os.path.exists(self.path_to_raw):
                os.makedirs(self.path_to_raw)
            if not os.path.exists(self.path_to_processed):
                os.makedirs(self.path_to_processed)

        else:
            raise Exception('ICollector : get_paths name is no valid string')

        return (self.path_to_raw, self.path_to_processed)

    def __load_data(self):
        '''
        Method loads the data from the raw folder if this fil does not exist we can download the file from the internet.
        '''
        # first we try to download the data
        if not os.path.exists(self.path_to_raw):
            self.download_data()

        if not os.path.exists(self.path_to_raw):
            raise Exception('{} : load_data there is no raw data'.format(self.__class__.__name__))  # # noqa: F821

        if os.path.exists(self.path_to_raw):
            frame = pd.read_csv(self.path_to_raw)
            frame = self.process_data(frame)
            frame.to_csv(self.path_to_processed)

        else:
            raise Exception('There is no{}'.format(self.path_to_raw))

    def get_data(self):
        '''
        Method returns the processed frame saved in res/'name'/processed/???.csv
        '''
        # first check if raw exist and processed not and handle this
        if ((not os.path.exists(self.path_to_processed)) and os.path.exists(self.path_to_raw)):
            self.__load_data()
            steam_frame = pd.read_csv(self.path_to_processed)

        # if the processed file exist we read it
        elif os.path.exists(self.path_to_processed):
            steam_frame = pd.read_csv(self.path_to_processed)

        else:
            raise Exception('There is no processed or raw file {} in  folder {}'.format(self.csv_name, self.name))

        return steam_frame

    def plot(self, frame):
        '''
        Method plots the data to get a first impression
        '''
        if not frame.empty:
            frame.plot(x_compat=True, kind='line', title=self.name)
            plot.gca().xaxis.set_major_locator(dates.DayLocator())
            plot.gca().xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))
            plot.show()

        else:
            raise Exception('plot frame is empty')

    @abstractmethod
    def download_data(self):
        '''
        Method for downloading the data from the internet.
        Load from source save to path_to_raw (NOT IMPLEMENTET)
        '''
        raise NotImplementedError

    @abstractmethod
    def process_data(self, frame_raw):
        '''
        This is an abstract method!!
        Simple processing of the raw data e.g drop null values.
        Returns the processed dataframe.
        '''
        raise NotImplementedError


class SteamCollector(ICollector):
    '''
    Class handles the datacollection of the worldwide Steam data.
    Example sage:
    STEAM = SteamCollector()
    stframe = STEAM.get_data()
    STEAM.plot(stframe)
    '''
    def __init__(self):
        ICollector.__init__(self, 'steam')  # add arguements if req
        self.source = None
        self.csv_name = 'steam_user_3y.csv'

        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        '''
        Simple preprocessing of the steam dataset. Drop null values and set Date as index.
        '''
        # set index
        frame_raw.columns = ['Date', 'Users', 'In-Game']
        frame_raw = frame_raw.set_index('Date')

        # drop rows with no entry
        frame_raw.dropna(subset=['Users', 'In-Game'], inplace=True)
        return frame_raw


class PornhubCollector(ICollector):
    '''
    This Colector handles the collection, and simple preprocessing of the pornhub dataset.

    Example usage:
    PORN = PornhubCollector()
    frame = PORN.get_data()
    PORN.plot(frame)
    PORN.show()
    '''
    def __init__(self):
        ICollector.__init__(self, 'pornhub')  # add arguements if req
        self.source = 'http://www.pornhub.com/insights/coronavirus-update'
        self.csv_name = 'World.csv'
        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        '''
        Preprocessing of the pornhub dataset.transformation of 10% -> 0.1.
        Set Date as Index.
        Input is the raw data as pandas frame.
        Returns the preprocessed dataset as pandas frame.
        '''
        frame_raw.columns = ['Date', 'Traffic_inc']
        frame_raw = frame_raw.set_index('Date')

        # convert 10% to 0.1
        frame_raw['Traffic_inc'] = frame_raw['Traffic_inc'].str.rstrip('%').astype('float') / 100.0
        return frame_raw


class PSCollector(ICollector):
    '''
    This Colector handles the collection of Playstation data.

    Example usage :
    PS = PSCollector()
    ps_frame = PS.get_data()
    PS.plot(ps_frame)
    '''
    def __init__(self):
        ICollector.__init__(self, 'playstation')
        self.source = ''
        self.csv_name = 'ps_players.csv'

        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        '''
        Processing the Playstation data.
        Input is the raw data as pandas frame.
        Returns the preprocessed dataset as pandas frame.
        '''
        frame_raw.columns = ['Date', 'PS3', 'PS4', 'Vita']
        frame_raw = frame_raw.set_index('Date')

        return frame_raw
