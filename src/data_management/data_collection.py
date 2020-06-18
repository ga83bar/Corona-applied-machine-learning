"""
This class serves as the interface between the data selection CLI and the necessary
data collection APIS.
"""
from datetime import timedelta as t_delta
from requests import get
import pandas as pd
from matplotlib import pyplot as plot

# Error Codes
COUNTRY_REQUEST_FAILED = 'REQUEST STATUS {}: {}'
INVALID_REQUEST = 'REQUEST INVALID'

# Date constants
DATE_SRT = '2019-04-01T00:00:00Z'
DATE_END = '2020-05-01T00:00:00Z'

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

    def __init__(self):
        self.get_covid_data(EUROPE, do_plot=True)

    def get_all_data(self):
        """ Returns all Data"""

    def val_source_data(self):
        """ Validate raw Data for Completeness"""
        raise NotImplementedError

    def get_covid_data(self, countries, save_frame=False, do_plot=False):
        """ Return only Covid Data"""
        country_pd_frames = [self.covid_request(country) for country in countries]
        self.handle_result(countries, save_frame, do_plot)
        return country_pd_frames

    def get_date_list(self):
        """ Gen list of all dates between start and end date"""
        date_list = [DATE_SRT + t_delta(days=x) for x in range(0, (DATE_END - DATE_SRT).days)]
        return date_list

    def covid_request(self, country):
        """ Return Covid data for requested country"""
        covid_request = get(API_COVID_COUNTRY.format(country))
        if covid_request.status_code == 200:
            frame = pd.read_json(covid_request.text)
        else:
            print(COUNTRY_REQUEST_FAILED.format(country, covid_request.status_code))
            raise Exception(INVALID_REQUEST)
        return [country, frame]

    def handle_result(self, dataframes, save_frame=False, do_plot=False):
        '''
        Here we define what we want to do with the data
        '''
        if save_frame:
            for frame in dataframes:
                _ = [frame[1].to_pickle(("./res/{}/covid19_{}.pkl").format(frame[0], frame[0])) for frame in dataframes]

        if do_plot:
            for frame in dataframes:
                frame[1].plot(kind='line', title=frame[0], x='Date', y=['Confirmed', 'Deaths', 'Active'])
                plot.show()


DATA_COLLECTOR = DataCollection()
