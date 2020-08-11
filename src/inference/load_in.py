"""
This module handles the loading and management of data for model training
and model testing. Any and all functions that directly handle data for a learning
task MUST go through here.
"""

import os
import pandas as pd

DATA_FILE = "res/{}/{}/{}.csv"
DATA_DIRECTORY = "res/{}/{}"

class LoadIn():
    """
    This class handles imports and persistent storage of datasets
    """
    def __init__(self):
        """
        Constructor. Initaliaze a loading manager.
        """
        self.datasets = {
            "app": "apple-mobility",
            "cov": "covid",
            "dec": "de-cix",
            "fin": "finance",
            "ggm": "google_mobility",
            "ggt": "google_trends",
            "iex": "ix",
            "pip": "pipeline",
            "pla": "playstation",
            "soc": "socialblade",
            "ste": "steam",
            "twi": "twitch"
        }
        self.dataframes = {}

    def get_set(self, strs, typ="processed"):
        """ Get dataframes for each dataset, load them """
        dataframes = {}
        for dset in strs:
            for file in os.listdir(DATA_DIRECTORY.format(self.datasets[dset], typ)):
                if file.endswith(".csv") and not self.dataframes[file]:
                    self.dataframes[file] = pd.read_csv(DATA_FILE.format(self.datasets[dset], typ, file))
                    dataframes[file] = pd.read_csv(DATA_FILE.format(self.datasets[dset], typ, file))
                if self.dataframes[file]:
                    dataframes[file] = self.dataframes[file]
        return dataframes
