"""provides the interface for data_management"""

import sys
from .. import parameter

class DatasetInterface():
    '''This interface defines the most important attributes and methods to load/get the raw dataset'''
    # DO NOT IMPLEMENT THIS
    # attributes
    m_parameter = Parameter.getInstance()

    # methods
    def __init__(self):
        raise NotImplementedError

    def load_data(self):
        '''This method is an interface method for loading the data it is implemented inpreprocessing.py'''
        raise NotImplementedError

    def more_functions_tb_implemented(self):
        '''This method is an interface method for loading the data it is implemented inpreprocessing.py'''
        raise NotImplementedError
