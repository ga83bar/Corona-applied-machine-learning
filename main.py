import numpy as np 
import pandas as pd 
import matplotlib as plt
import seaborn as sea 
import sklearn as sk

from logger import clsLogger
from parameter import clsParameter
from dataset import proxyDataset

def main():
    # This class is a Singelton object it does not matter in with subclass you
    # execute ...getInstance you always get the same instance of an object thats great to store data 
    # so all classes etc have acces to the same values
    m_params = clsParameter.getInstance()

    # logger is also a singelton pleas youse logger just for errors
    m_logger = clsLogger.getInstance()

    # This is how you can log things
    m_logger.writeFile('Hallo')

    # and this way you can change the logfile name
    m_params.setLogfileName('test.log')
    m_logger.writeFile('main : error 123') 
    

    # check python versions
    print('numpy version {}'.format(np.__version__))
    print('pandas version {}'.format(pd.__version__))
    print('seaborn version {}'.format(sea.__version__))
    print('matplotlib version {}'.format(plt.__version__))
    print('scikit-learn version {}'.format(sk.__version__))

    
    # This is how I think we will get a well seperation
    pDataset = proxyDataset()
    data = pDataset.getData()
    # if we can execute this and have valid data we can think about our learning classes .... but I think that is to far away


    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # If you want I can send you my .vscode/launche and task.json for automatically debugging by pressing F5 
    # and also in this case we will activate and deactivate venv before and after executing the script
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

###########################
if __name__ == '__main__':
    main()
