"""
Implementation of a Gaussian model for our dataset
"""
import os
import datetime as dt
import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense
import numpy as np
from matplotlib import pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

class GaussianModel():
    """
    Class contains the gaussian model and all of its pre and post
    training attributes.
    """
    def __init__(self, dataframe):
        """
        Constructor
        """
        self.dataframe = dataframe
        self.settings = {}
        self.history = None
        self.trained_model = None
        self.init_model = None

    def setup(self):
        """
        Model setup
        """

        self.init_model = model
        return self.init_model