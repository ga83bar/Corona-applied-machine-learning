"""Entrypoint"""
import logging
import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sea
import sklearn as sk


from src.data_management.preprocessing import DataPreprocessor
from src.parameter import Parameter

logging.basicConfig(level=logging.INFO)
PARAMS = Parameter.get_instance()


def main():
    '''Main function'''
    # test
    data = [
        1, 2,
        3, 4
    ]
    test = DataPreprocessor()
    test.scale_data(data)

    logging.debug('numpy version %s', np.__version__)
    logging.debug('pandas version %s', pd.__version__)
    logging.debug('seaborn version %s', sea.__version__)
    logging.debug('matplotlib version %s', plt.__version__)
    logging.debug('scikit-learn version %s', sk.__version__)


if __name__ == '__main__':
    main()
