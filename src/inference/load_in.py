import pandas as pd

DATA_FILE = "res/{}/{}/{}.csv"
DATA_DIRECTORY = "res/{}/{}"

class Load_in():
    """ 
    This class handles the loading and management of data for model training
    and model testing. Any and all functions that directly handle data for a learning
    task MUST go through here.
    """
    def __init__(self):
        """
        Constructor. Initaliaze a loading manager.
        """
        self.datasets={
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
        self.dataframes={}

    def get_set(self, strs=["cov"], typ="processed")
        """ Get dataframes for each dataset, load them """
        for dset in strs:
            self.dataframes[dset] = pd.read_csv(DATA_FILE.format(self.datasets[dset], typ, name))