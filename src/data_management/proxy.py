"""here goes the proxy"""

import os
import datetime as dt
import pandas as pd

from parameter import Parameter

class Proxy():
    '''handles dataset access and makes the decision if we load the
    data from www or if we just load data from disk (may during test and debug phases)'''
    # we init clsDataset just if we really need it e.g. when we load the data from the web!!!

    # ATTRIBUTES
    # PLEASE READ THIS!!!!!
    bool_load_processed_data_from_file = None      # load the whole dataset load rawdata + preprocessing
    bool_load_raw_from_file = None    # load raw data from file and process it check param.DEBUG + filePath

    path_raw_data = None
    path_processed_data = None
    processed_data_name = None
    raw_data_name = None

    def __init__(self):
        # set Bool values names and paths
        self.__bool_load_all_new = True
        self.__bool_load_raw_from_file = False
        # TODO set filenames ....

    # THIS IS the method we use to get the data

    def get_data(self):
        ''' Method handles the accesst to the dataset please just use this method from other classes to get the data'''
        if self.bool_load_processed_data_from_file:
            print('load processed dat from file {}')
            data = [
                1, 2,
                3, 5
                ]
            return data

        if self.bool_load_raw_from_file:
            # load rawData from file
            print('load raw data from cached file')

        else:
            # load rawData from file
            data_processor = DataPreprocessor()
            print(data_processor)

        return data

    def dummy_method(self):
        """implement here"""
        raise NotImplementedError


class DataMerger(object):
    '''Dummy doc sorry i do this after the exams'''
    def __init__(self):
        self.params = Parameter.get_instance()
        # make a list containing all paths to processed data
        folders = self.params.folders

        # join the paths structure ~ ./res/'folder_name'/processed
        path_to_res = os.path.join('.', 'res')
        self.path_to_processed = []

        for folder in folders:
            path = os.path.join(path_to_res, folder, 'processed')
            self.path_to_processed.append(path)

        # init other attributes
        self.frame = pd.DataFrame()

    def get_all_data(self, save_data=True):
        '''dummy
        '''
        start = self.params.start_date_data
        end = self.params.end_date_data
        self.frame = self.__get_date_frame(start, end)

        for folder in self.path_to_processed:
            dirs = os.listdir(folder)
            for file in dirs:
                if file.endswith('.csv'):
                    path_processed_data = os.path.join(folder, file)
                    df_tmp = pd.read_csv(path_processed_data)
                    df_tmp['Date'] = pd.to_datetime(df_tmp['Date'], utc=True)
                    self.frame = self.frame.merge(df_tmp, how='left')

        if save_data:
            path = os.path.join('.', 'res', 'all_raw.csv')
            self.frame.to_csv(path)

        return self.frame

    def __get_date_frame(self, start, end):
        """ Gen list of all dates between start and end date"""
        date_list = [start + dt.timedelta(days=x) for x in range(0, (end - start).days)]
        frame = pd.DataFrame(date_list)
        frame.columns = ['Date']
        frame['Date'] = pd.to_datetime(frame['Date'], utc=True)
        return frame


def test():
    '''Dummy'''
    da_me = DataMerger()
    da_me.get_all_data()

if __name__ == '__main__':
    test()
