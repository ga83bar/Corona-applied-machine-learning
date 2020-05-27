"""Entrypoint"""

import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sea
import sklearn as sk
import logging

import data_management
from parameter import Parameter

logging.basicConfig(level=logging.INFO)
Params = Parameter()


def main():

    logging.debug('numpy version {}'.format(np.__version__))
    logging.debug('pandas version {}'.format(pd.__version__))
    logging.debug('seaborn version {}'.format(sea.__version__))
    logging.debug('matplotlib version {}'.format(plt.__version__))
    logging.debug('scikit-learn version {}'.format(sk.__version__))

    our_data = data_management.Dataset()
    print(our_data)


if __name__ == '__main__':
    main()
