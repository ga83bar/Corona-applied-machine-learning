"""everythin related to preprocessing - might be extended to a whole package if required"""

from interface import PreprocessDataInterface # pylint: disable=import-error


class DataPreprocessor(PreprocessDataInterface):
    '''Here the magic happens. We load the data in this class
    '''

    def __init__(self):
        print('Dataset is not implemented')

   #TODO implement
    def set_scalinging_algorithm(self, algo):
        """these functions only serve the purpose of providing an example"""
        raise NotImplementedError

    def scale_data(self, data):
        """feel free to replace them with something that actually makes sense"""
        raise NotImplementedError
