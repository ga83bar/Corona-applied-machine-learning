"""Module docstring"""

# from requests import get
# import datetime as dt
import os
import datetime as dt


class Parameter:
    """This class contains parameters and methods to convert them.
    This is a Singleton object check for thread safety.
    Init with s = Parameter.getInstance()
    s = Parameter() will raise an exception.
    With each .getInstance you will get the same (id) object"""
    # public attributes THESE TWO SHOULD BE THE ONLY PUBLIC ATTRIBUTES !!!!
    DEBUG = True

    # private attributes PLEASE USE GETTER AND SETTER
    __instance = None
    __CWD = None
    __logfile_path = None

    @staticmethod
    def get_instance():
        """ Static access method.
        Use instead of Parameter(). So you get everytime the same instance of the object.
        """
        if Parameter.__instance is None:
            Parameter()
            Parameter.__instance.__singelton_init()   # pylint: disable=protected-access

        return Parameter.__instance

    def __singelton_init(self):
        # INIT YOUR VARS HERE !!!!!
        '''
        This is the singelton init function if you want to init attributes do it here
        '''
        self.working_directory = os.path.dirname(os.path.abspath(__file__))
        self.logfile_path = os.path.join(self.working_directory, 'documentation', 'logfiles', 'aml_log.log')
        self.__start_date_data = dt.datetime(2017, 1, 1)
        
        # TODO ALA
        self.__med_comp = []
        self.__oil_comp = ['CVX', 'XOM', 'PTR']
        self.__steel_comp = ['TKA', 'ARRD']
        self.__automotive_comp = ['TOM', 'GM', 'HYU']
        self.__telecom_comp = []
        self.__tec_comp = ['AAPL', 'AMZN', 'GOOGL']
        self.__finance_companies = (self.__med_comp + self.__oil_comp + self.__steel_comp +
                                    self.__automotive_comp + self.__telecom_comp +
                                    self.__tec_comp)

    def __init__(self):
        """ Virtual private constructor."""
        if Parameter.__instance is not None:
            raise Exception("This class is a singleton!")

        Parameter.__instance = self
        self.__singelton_init()

    def get_working_directory(self):
        """returns current working directory"""
        return self.working_directory

    def get_logfile_path(self):
        """returns file path"""
        filepath = self.__logfile_path
        return filepath

    @property
    def start_date_data(self):
        '''Getter method for start date of data collection'''
        return self.__start_date_data

    @start_date_data.setter
    def start_date_data(self, start_date):
        '''Setter method for start date of data collection'''
        if isinstance(start_date, dt):
            self.__start_date_data = start_date
        else:
            raise Exception('Your start date is no valid datetime object!')

    @property
    def stock_companies(self):
        '''Getter method for stock companies list'''
        return self.__finance_companies

    @stock_companies.setter
    def stock_companies(self, companies_list):
        '''Setter method for stock companies list'''
        self.__finance_companies = companies_list
