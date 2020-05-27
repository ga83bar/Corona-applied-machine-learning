"""Entrypoint"""

import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sea
import sklearn as sk
import logging

from src.data_management.preprocessing import DataPreprocessor
from src.parameter import Parameter

logging.basicConfig(level=logging.INFO)
Params = Parameter.getInstance()


def main():

    #test
    data=[
        1, 2,
        3, 4
    ]
    test = DataPreprocessor()
    test.scale_data(data)
    

    logging.debug('numpy version {}'.format(np.__version__))
    logging.debug('pandas version {}'.format(pd.__version__))
    logging.debug('seaborn version {}'.format(sea.__version__))
    logging.debug('matplotlib version {}'.format(plt.__version__))
    logging.debug('scikit-learn version {}'.format(sk.__version__))


if __name__ == '__main__':
    main()
