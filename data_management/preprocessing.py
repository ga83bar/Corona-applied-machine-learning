"""everythin related to preprocessing - might be extended to a whole package if required"""

from interface import DatasetInterface

class Dataset(DatasetInterface):
    '''Here the magic happens. We load the data in this class
    '''
    def __init__(self):
        print('Dataset is not implemented')

    def load_data(self):
        """ load function
            todo: implement!
        """
        # Until now load data does not do many things but it returns data
        data = [1, 2, 3, 4, 5, 6]
        return data