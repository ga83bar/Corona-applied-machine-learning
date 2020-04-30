# imports
import pandas as pd 
import numpy as np 
import os

from parameter import clsParameter
from dataHandler import clsDataHandler

########################################################################################################
#####                                    THIS IS THE : DATASET INTERFACE                           #####
########################################################################################################
class iDataset():
    '''This interface defines the most important attributes and methods to load/get the raw dataset'''
    #DO NOT IMPLEMENT THIS
    #attributes
    m_parameter = clsParameter.getInstance()

    # methods
    def __init__(self):
        raise NotImplementedError


    def loadData(self):
        raise NotImplementedError


    def thereWillBeMoreFunctionsInFuture(self):
        print('We will get more interface functions')



########################################################################################################
#####                                    THIS IS CLASS : DATASET                                   #####
########################################################################################################
class clsDataset(iDataset):
    '''Here the magic happens. We load the data in this class
    '''
    def __init__(self):
        print('Dataset is not implemented')

    def loadData(self):
        #TODO implement
        print('Until now load data does not do many things but it returns data (I think it would be good if this is a pandas frame')
        data = [1,2,3,4,5,6]
        return data



########################################################################################################
#####                                    THIS IS THE : DATASET PROXY                               #####
########################################################################################################
class proxyDataset():
    '''proxyDataset handles the access to the dataset and makes the decision if we load the data from www or if we just load data
    from an file (may during test and debug phases)'''
    # we init clsDataset just if we really need it e.g. when we load the data from the web!!!

    # ATTRIBUTES
    # PLEASE READ THIS!!!!!
    __boolLoadProcessedDataFromFile = None      # all hopefully is clear load the whole dataset load rawdata + preprocess it
    __boolLoadRawFromFile = None    # load raw data from file and process it check param.DEBUG + filePath .. or some other logic 

    __pathRawData = None
    __pathProcessedData = None
    __processedDataName = None
    __rawDataName = None


    def __init__(self):
        #set Bool values names and paths
        self.__boolLoadAllNew = True
        self.__boolLoadRawFromFile = False
        #TODO set filenames ....


    ## THIS IS the method we use to get the data
    def getData(self): 
        #TODO
        ''' Method handles the accesst to the dataset please just use this method from other classes to get the data'''
        if (self.__boolLoadProcessedDataFromFile):
            print('load processed dat from file {}')
            data= [1,2,43,5,5]
            return data
        
        else:
            #TODO
            # get Raw data
            if (self.__boolLoadRawFromFile):
                # load rawData from file
                print('load raw data from file')
            else:
                # load rawData from file
                Dataset = clsDataset()
                rawData = Dataset.loadData()
                print('load raw data from web')
                del Dataset

            # process it 
            dataHandler = clsDataHandler()
            data = dataHandler.handleMissingData(rawData)
            del rawData

            data = dataHandler.scaleData(data)
            data = dataHandler.transformeData(data)
                
            # return it
            return data



