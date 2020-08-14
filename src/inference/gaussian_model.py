"""
Implementation of a Gaussian model for our dataset
"""
import os
from pathlib import Path
import datetime as dt
import numpy as np
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import GridSearchCV
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, RationalQuadratic, ExpSineSquared

class GaussianModel():
    """
    Class contains the gaussian model and all of its pre and post
    training attributes.
    """
    def __init__(self, dataframe=None):
        """
        Constructor
        """
        self.dataframe = dataframe
        self.settings = {}
        self.history = None
        self.trained_model = None
        self.init_model = None
        self.gp_kernel = "kernel"

    def load_data(self, file=None):
        """
        loads data
        """
        # temporary path
        path = "GIT/group11/src/inference/all_raw.csv"
        self.dataframe = pd.read_csv(path)
        self.dataframe = self.dataframe.set_index("Date")
        label_df = self.dataframe["NDAQ"]
        input_df = self.dataframe["confirmed"]
        self.dataframe = pd.concat([label_df, input_df], axis=1).dropna() 
        # covid Data
        # Label Data

    def train(self):
        # create Kernel
        self.X = self.dataframe["confirmed"].to_numpy().reshape(-1, 1)
        self.y = self.dataframe["NDAQ"].to_numpy().reshape(-1, 1)
        self.gpr = GaussianProcessRegressor(kernel=self.gp_kernel)
        self.gpr.fit(self.X, self.y)

    def predict(self):
        self.output_gpr = self.gpr.predict(self.X, return_std=False)
        return self.output_gpr

    def plot(self):
        plt.figure(figsize=(10, 5))

        plt.scatter(self.X, self.y, c='k', label='data')
        plt.plot(self.X, self.output_gpr)
       
        plt.xlabel('data')
        plt.ylabel('target')
        plt.show()
        return 0
        
    def create_kernel(self):
        k1 = 66.0**2 * RBF(length_scale=67.0)  # long term smooth rising trend
        k2 = 2.4**2 * RBF(length_scale=90.0) \
            * ExpSineSquared(length_scale=1.3, periodicity=1.0) 
        k3 = 0.66**2 \
            * RationalQuadratic(length_scale=1.2, alpha=0.78)
        k4 = 0.18**2 * RBF(length_scale=0.134) \
            + WhiteKernel(noise_level=0.19**2)  # noise terms
        self.gp_kernel  = ExpSineSquared(1.0, 5.0) \
    + WhiteKernel(1e-1)    

GM = GaussianModel()
GM.create_kernel()
GM.load_data()
GM.train()
GM.predict()
GM.plot()
