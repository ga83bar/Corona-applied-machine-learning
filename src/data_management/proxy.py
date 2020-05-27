"""here goes the proxy"""

from .preprocessing import DataPreprocessor
from .data_collection import DataCollection


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
            data_collector = DataCollection()
            raw_data = data_collector.get_raw_data()
            print(raw_data)

            data_processor = DataPreprocessor()
            print(data_processor)

        return data

    def dummy_method(self):
        """implement here"""
        raise NotImplementedError
