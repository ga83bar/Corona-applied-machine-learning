"""
This module predicts time series utilizing an online
learning scheme coupled with a simple ensemble linear
regression system.
"""

import numpy as np
from Creme import compose
from Creme import linear_model
from Creme import preprocessing
from Creme import metrics
from Creme import stream
from Creme import stats
from Creme import time_series
from creme import optim
from matplotlib.pyplot import plot as plt

class OnTimePred():
    """
    Utilizes the Creme TimeSeries library and online
    functionality to succinctly predict time series
    """
    def __init__(self, dataframe, output, label):
        """
        Init
        """
        self.dataframe = dataframe
        self.output = output
        self.predictions = []
        self.prediction_frame = None
        self.metric = None
        self.model = None
        self.label = label

    def init_model(self):
        """
        Initialize model
        """
        model = compose.Pipeline(
            ('features', compose.TransformerUnion(
                ('weekday', self.get_weekday()),
                ('month', self.get_month()),)),
            ('scale', preprocessing.StandardScaler()),
            ('lin_reg', linear_model.LinearRegression(intercept_lr=0,
                                                      optimizer=optim.SGD(0.03)))
        )
        model = time_series.Detrender(regressor=model, window_size=12)
        self.model = model
        self.metric = metrics.Rolling(metrics.MAE(), 12)

    def fit_model(self):
        """
        Fit the model given the data
        """
        for inp, lbl in stream.iter_pandas(self.dataframe, self.output):
            prediction = self.model.predict_one(inp)
            self.predictions.append(prediction)
            self.model.fit_one(inp, lbl)
            self.metric.update(lbl, prediction)

    def plot_model(self):
        """
        Plot the result
        """
        x_ax = np.arange(0, len(self.predictions), 1)
        plt.ylabel(self.label)
        plt.plot(x_ax, self.predictions, label="Predictions")
        plt.plot(x_ax, self.output, label="Outputs")
        plt.show()

    def get_month(self):
        """
        Gets the months
        """
        months = self.dataframe[["month"]].copy().pop("month")
        return months

    def get_weekday(self):
        """
        gets the weekdays
        """
        weekdays = self.dataframe[["day"]].copy().pop("day")
        return weekdays
