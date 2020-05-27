"""provides the interface for data_management"""

from ..parameter import Parameter


class DatasetInterface():
    '''This interface defines the most important attributes and methods to load/get the raw dataset'''
    # DO NOT IMPLEMENT THIS
    # attributes
    m_parameter = Parameter.get_instance()

    # methods
    def __init__(self):
        pass

    def load_data(self):
        '''This method is an interface method for loading the data it is implemented inpreprocessing.py'''

    def more_functions_tb_implemented(self):
        '''This method is an interface method for loading the data it is implemented inpreprocessing.py'''


class PreprocessDataInterface():
    '''Edit doxy !!!'''

    def __init__(self):
        pass

    def set_scalinging_algo(self, algo):
        '''Edit doxy !!!'''

    def scale_data(self, data):
        '''Edit doxy !!!'''

    def dummy(self):
        '''Edit doxy !!!'''
