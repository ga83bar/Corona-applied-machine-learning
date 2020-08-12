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
import pickle

class OnlineFCN():
    """
    Class contains an online linear model and all of its pre and post
    training attributes.
    """
    def __init__(self, dataframe,dset):
        """
        Constructor
        """
        self.dataframe = dataframe
        self.settings = {}
        self.history = None
        self.trained_model = None
        self.init_model = None
        self.metric = None
        self.dset = dset

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
            prediction = self.trained_model.predict_one(x)
            metric = self.metric.update(lbl, prediction)
            self.trained_model = self.trained_model.fit_one(x, lbl)
        print(metric)

    def save_model(self):
        """
        Saves a model
        """
        with open(f"onln_fcn_{self.dset}_{dt.time}.pkl", 'wb') as f:
            pickle.dump(self.trained_model, f)
            return self.trained_model

    def load_model(self, time):
        """
        Loads a pretrained model
        """
        with open(f"onln_fcn_{self.dset}_{time}.pkl", 'rb') as f:
            model = pickle.load(f)
            return model