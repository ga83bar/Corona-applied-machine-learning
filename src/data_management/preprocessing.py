"""everythin related to preprocessing - might be extended to a whole package if required"""
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from interface import PreprocessDataInterface   # pylint: disable=import-error


class CoronaPreprocessor(PreprocessDataInterface):
    '''
    CoronaPreprocessor (CP) preprocesses the corona data.
    We preprocess the data using pca to reduce the dimension.
    This class implements the PreprocessDataInterface!
    '''

    def __init__(self, scale_algo=2):
        '''
        Initialize CoronaPreprocessor (CP):
        @param saving_path : Path where the processed data should be stored.
        @param scale_algo : Selected scaling algo according to :
            PCA = 1
            STANDART_SCALING = 2
            Z_SCALING = 3
            Can also be set with set_scalinging_algorithm(algo)
        '''
        super(CoronaPreprocessor, self).__init__('covid', scale_algo)  # add also this!!
        print('Inittialized Corona preprocessor')

    def _pca(self, data, componenets=3):
        '''Abstract method. Implement PCA'''
        pca = PCA(n_components=componenets)
        preprocessed_data = pca.fit(data)
        return preprocessed_data

    def _standart_scaling(self, data):
        '''Abstract method. Implement standart scaling'''
        print('Not implemented. We just use pca for covid data')
        preprocessed_data = data
        return preprocessed_data

    def _min_max_scaling(self, data):
        '''Abstract method. Implement z scaling'''
        print('Not implemented. We just use pca for covid data')
        preprocessed_data = data
        return preprocessed_data

def standart_scale(data):
    '''
    Standart function standart scaler. If you want you can simply use this inside
    your _standart_scaling method. But you have to clean the data first (No date..)
    '''
    scaler = StandardScaler()
    scaler.fit(data)
    data = scaler.transform(data)
    return data

def min_max_scale(data):
    '''
    Standart function min_max_scaler. If you want you can simply use this inside 
    your _min_max_scaling method. But you have to clean the data first (No date..)
    '''
    scaler = MinMaxScaler()
    scaler.fit(data)
    data = scaler.transform(data)
    return data

# TODO info
# TODO remove
'''
INFO:
If you use this interface itmakes your live easier (I hope so).

For your class:
call in your __init__ method the parent constructor according to the covidPreprocessor
super('YOUR_class_name',self).__init__('folder_name', scaling_algo (1,2,3 see interface))

After that the data is loaded from this folder ....

You just have to implement the 3 methods 
(1) _min_max_scaling(self, data)
(2) _standart_scaling(self, data)
(3) _pca(self, data, componenets=3)

for 1 + 2 you can also use the predefined standarts  e.g.
def _min_max_scaling(....):
    return min_max_scale(data) BUT YOU HAVE TO CLEAN THE DATA FIRST (NO DATE ..)

'''
def tests():
    '''Dummy'''
    # add your classes in this style
    co_p = CoronaPreprocessor()

    frame_list = []

    col_list = [co_p]
    for col in col_list:
        frame_list.append(col.process())

    # at this step we should have all single frames in one list
    # merge them


if __name__ == '__main__':
    tests()
