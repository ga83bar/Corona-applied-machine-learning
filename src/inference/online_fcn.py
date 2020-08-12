"""
Implementation of an online fcn model for our dataset
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
from creme import compose
from creme import datasets
from creme import linear_model
from creme import metrics
from creme import preprocessing

class OnlineFCN():
    """
    Class contains an online linear model and all of its pre and post
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
        self.metric = None

    def setup(self):
        """
        Model setup
        """
        model = compose.Pipeline(
            preprocessing.StandardScaler(),
            linear_model.LogisticRegression()
        )
        self.init_model = model
        self.trained_model = model
        return self.init_model

    def set_metric(self, metric="Accuracy"):
        """
        Set the desired performance metric
        """
        self.metric = metrics.Accuracy()
        return self.metric

    def do_training(self):
        """
        Train the model
        """
        for x, lbl in self.dataframe:
            prediction = self.trained_model.predict_one()
            metric = self.metric.update(lbl, prediction)
            self.trained_model = self.trained_model.fit_one(x, lbl)
        print(metric)