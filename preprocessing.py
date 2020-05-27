"""module responsible for preprocessing and everything related
"""


class InterfacePreprocessing():
    '''This Interface defines the basic methods for the data class.
       The main task of this class is to handle data specific operations like
        - scaling
        - transforming
        - handle missing data
    '''

    # TODO for other methods and algorithms...

    def handleMissingData(self, p_data):   # p for parameter
        raise NotImplementedError("Hey, Don't forget to implement it!")

    def transformeData(self, p_data):
        raise NotImplementedError("Hey, Don't forget to implement it!")

    def scaleData(self, p_data):
        raise NotImplementedError("Hey, Don't forget to implement it!")

    def setMissingDataAlgo(self, algorithem):
        raise NotImplementedError("Hey, Don't forget to implement it!")
    # this is the interface until now we surely will get more functions =


class DataPreprocessing(InterfacePreprocessing):
    def __init__(self):
        self.__handelMissingDataAlgo = self.HMD_DELET_ROW
        print('selected Algo for handling missing data {}'.format(self.__handelMissingDataAlgo))
        print('A few things tot do here init ')

    def handleMissingData(self, p_data):
        print(' we now handle missing data')
        return p_data

    def transformeData(self, p_data):
        print('transform data')
        return p_data

    def scaleData(self, p_data):
        print('scale data')
        return p_data
