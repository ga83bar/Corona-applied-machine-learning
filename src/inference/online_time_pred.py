"""
This module predicts time series utilizing an online
learning scheme coupled with a simple ensemble linear
regression system.
"""

from Creme import compose
from Creme import linear_model
from Creme import preprocessing
from Creme import metrics
from matplotlib.pyplot import plot as plt

class OnTimePred():
    """
    Utilizes the Creme TimeSeries library and online
    functionality to succinctly predict time series
    """
    def __init__(self, dataframe):
        """
        Init
        """
        self.dataframe = dataframe
        self.predictions = None
        self.prediction_frame = None
        self.metric = None
        self.model = None

    def init_model(self):
        """
        Initialize model
        """
        model = compose.Pipeline(
            ('scale', preprocessing.StandardScaler()),
            ('lin_reg', linear_model.LinearRegression()))
        self.model = model
        self.metric = metrics.Rolling(metrics.MAE(), 12)

    def fit_model(self):
        """
        Fit the model given the data
        """
        for inp, lbl in stream.iter_pandas(self.dataframe, self.output):
            