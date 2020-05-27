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
    def getInstance():
        """ Static access method.
        Use instead of Parameter(). So you get everytime the same instance of the object.
        """
        if Parameter.__instance is None:
            Parameter()
            Parameter.__instance.__singeltonInit()

        return Parameter.__instance

    def __singeltonInit(self):
        # INIT YOUR VARS HERE !!!!!
        '''
        This is the singelton init function if you want to init attributes do it here
        '''
        self.__CWD = os.path.dirname(os.path.abspath(__file__))
        self.__logfile_path = os.path.join(self.__CWD, 'documentation', 'logfiles', 'aml_log.log')

    def __init__(self):
        # DO NOT CHANGE THIS METHOD
        """ Virtually private constructor."""
        if Parameter.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Parameter.__instance = self
            self.__singeltonInit()

    def getCWD(self):
        return self.__CWD

    def getLogfilePath(self):
        filepath = self.__logfile_path
        return filepath

    def setLogfileName(self, filename):
        if isinstance(filename, str):
            if (filename.endswith('.txt') or filename.endswith('.log')):
                self.__logfile_path = os.path.join(self.__CWD, 'documentation', 'logfiles', filename)
            else:
                raise Exception('No valid Logfile ending (.txt or .log)')
        else:
            raise Exception('No valid Logfile name')
