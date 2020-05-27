"""everythin related to preprocessing - might be extended to a whole package if required"""

from .interface import PreprocessDataInterface


class DataPreprocessor(PreprocessDataInterface):
    '''Here the magic happens. We load the data in this class
    '''

    def __init__(self):
        super(DataPreprocessor, self).__init__()
        print('Dataset is not implemented')

    # TODO implement
    def set_scalinging_algo(self, algo):
        '''Edit doxy !!!'''
        print('much work do do here')

    def scale_data(self, data):
        '''Edit doxy !!!'''
        print('much work do do here')

    def dummy(self):
        '''Edit doxy !!!'''
        print('dummyfunction')
