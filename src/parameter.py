"""Module docstring"""

# from requests import get
# import datetime as dt
import os


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
            Parameter.__instance.__singelton_init()

        return Parameter.__instance

    def __singelton_init(self):
        # INIT YOUR VARS HERE !!!!!
        '''
        This is the singelton init function if you want to init attributes do it here
        '''
        self.working_directory = os.path.dirname(os.path.abspath(__file__))
        self.logfile_path = os.path.join(self.working_directory, 'documentation', 'logfiles', 'aml_log.log')

    def __init__(self):
        # DO NOT CHANGE THIS METHOD
        """ Virtually private constructor."""
        if Parameter.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Parameter.__instance = self
            self.__singelton_init()

    def get_working_directory(self):
        """returns current working directory"""
        return self.working_directory

    def get_logfile_path(self):
        """returns file path"""
        filepath = self.__logfile_path
        return filepath
