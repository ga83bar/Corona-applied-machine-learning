
########################################################################################################
#####                                    THIS IS THE : DATA INTERFACE                              #####
########################################################################################################
# DO NOT IMPLEMENT THE INTERFACE
class iDataHandler():
    '''This Interface defines the basic methods for the data class.
    The main task of this class is to handle data specific operations like 
        - scaling
        - transforming
        - handle missing data
    '''
    # attributes for different ALGOS
    HMD_MEAN = 1        #HMD == handle missing data ..
    HMD_MEDIAN = 2
    HMD_DELET_ROW = 3
    __handelMissingDataAlgo = None

    #TODO for other methods and algos...


    #def __init__(self):
    #    raise NotImplementedError

    def handleMissingData(self, p_data):# p for parameter
        raise NotImplementedError

    def transformeData(self, p_data):
        raise NotImplementedError

    def scaleData(self, p_data):
        raise NotImplementedError

    def setMissingDataAlgo(self, algorithem):
        raise NotImplementedError
    # this is the interface until now we surely will get more functions =



########################################################################################################
#####                                    THIS IS THE : DATA Class                                  #####
########################################################################################################
# Implement this stuff !!!!!!!!!!!!!!!!
class clsDataHandler(iDataHandler):
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
    