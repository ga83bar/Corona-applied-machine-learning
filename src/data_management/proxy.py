"""here goes the proxy"""

from preprocessing import DataPreprocessor
from data_collection import DataCollection


class Proxy():
    '''handles dataset access and makes the decision if we load the
    data from www or if we just load data from disk (may during test and debug phases)'''
    # we init clsDataset just if we really need it e.g. when we load the data from the web!!!

    # ATTRIBUTES
    # PLEASE READ THIS!!!!!
    __boolLoadProcessedDataFromFile = None      # load the whole dataset load rawdata + preprocessing
    __boolLoadRawFromFile = None    # load raw data from file and process it check param.DEBUG + filePath

    __pathRawData = None
    __pathProcessedData = None
    __processedDataName = None
    __rawDataName = None

    def __init__(self):
        # set Bool values names and paths
        self.__boolLoadAllNew = True
        self.__boolLoadRawFromFile = False
        # TODO set filenames ....

    # THIS IS the method we use to get the data
    def getData(self):
        ''' Method handles the accesst to the dataset please just use this method from other classes to get the data'''
        if (self.__boolLoadProcessedDataFromFile):
            print('load processed dat from file {}')
            data = [1, 2, 43, 5, 5]
            return data

        else:
            # TODO
            # get Raw data
            if (self.__boolLoadRawFromFile):
                # load rawData from file
                print('load raw data from cached file')
            else:
                # load rawData from file
                data_collector = DataCollection()
                rawData = data_collector.getRawData()

                dataProcessor = DataPreprocessor()

                
                rawData = our_data.loadData()
                print('load raw data from web')
                del Dataset

            # process it
            dataHandler = DataPreprocessor()
            data = dataHandler.handleMissingData(rawData)
            del rawData

            data = dataHandler.scaleData(data)
            data = dataHandler.transformeData(data)

            # return it
            return data
