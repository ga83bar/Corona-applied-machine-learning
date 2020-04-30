import datetime
import os
from parameter import clsParameter


class clsLogger(): # s because it is a Singelton
    '''Simple singelton logger class logfile-filename is defined in clsParameter. 
    USE .getInstance instead of clsLogger'''
    __instance = None
    __param = None

    @staticmethod 
    def getInstance():
        """ Static access method. USE clsLogger.getInstance() INSTEAD of clsLogger(). So you get everytime the same instance of the object  """
        if clsLogger.__instance == None:
            clsLogger()
            clsLogger.__instance.__singelton_init()
        return clsLogger.__instance


    def __singelton_init(self):
        '''Init function for Singelton object is executed only once(after creation)'''
        # This function is only executed once after creation!!
        self.__param = clsParameter.getInstance()




    def __init__(self):
        # Do not change this method make inits in __singelton_init!!!!
        """ Virtually private constructor. """
        if clsLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            clsLogger.__instance = self


    def writeFile(self, str_to_write, TAG = '', error_level = 0):
        # we have to check if the file exists 
        logfile = self.__param.getLogfilePath()

        if os.path.exists(logfile):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        f = open(logfile,append_write)
        f.write("{0}\t{1}\t{2} \n".format(datetime.datetime.now(),error_level, str_to_write))
        f.close()


    def __checkFileSize(self):
        maxSize = 100000 # some number 
        fileSize = os.path.getsize(self.__param.getLogfilePath())
        if fileSize > maxSize:
            self.__zipAndDelet(self.__param.getLogfilePath())


    def __zipAndDelet(self, filepath):
        '''Because we do not want to crush the system by a logfile that just appendes data after a while
        we zip the actual logfile and delet the old zip. This should happen automatically depending on the filesize'''
        zipFile = os.path.join(self.__param.getLogfilePath(), '.zip')

        raise NotImplementedError
        

        