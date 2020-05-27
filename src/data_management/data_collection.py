"""collects data"""


class DataCollection():
    '''This class is responsible for collecting raw data from div databases or API`s'''

    def return_raw_data(self):
        '''Most important method of cls DataCollection returns the raw data as pandas frame'''
        raise NotImplementedError

    def parse_data_from_online_source(self):
        '''Most important method of cls DataCollection returns the raw data as pandas frame'''
        raise NotImplementedError
