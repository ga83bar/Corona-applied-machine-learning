"""
This module serves as the hub for the model evaluation and training
"""
import datetime as dt
from load_in import LoadIn
from online_fcn import OnlineFCN


class Learning():
    """
    Initiate model fitting. Alternatively, display performance.
    """
    def __init__(self, algorithmen, datasets):
        self.__algorithmen = algorithmen
        self.loader = LoadIn()
        self.models = {}
        self.datasets = datasets
        self.dataframes = None
        self.dataframe = None
        self.frames_prior = None
        self.frames_post = None
        self.models = {}

    def pipeline(self):
        """
        This function represents the pipeline for the ml portion
        """
        self.dataframes = self.loader.load_all(self.datasets)
        self.dataframe = self.loader.get_all()
        self.fit(self.dataframe)

    def fit(self, frame):
        """
        Fit models based on past data. This function takes one frame,
        corresponding to one to-be-predicted dataset.
        Iterate this function for each desired dataset.
        """
        output_frames = {}
        if "nn" in self.__algorithmen:
            output_frames["nn"] = self.nn_fit(frame)
        if "elm" in self.__algorithmen:
            output_frames["elm"] = self.elm_fit(frame)
        if "linear" in self.__algorithmen:
            output_frames["linear"] = self.linear_fit(frame)
        if "online_fcn" in self.__algorithmen:
            output_frames["online_fcn"] = self.online_fcn_fit(frame, LABELS)
        if "gaussian" in self.__algorithmen:
            output_frames["gaussian"] = self.gaussian_fit(frame)
        return output_frames

    def predict(self):
        """
        Predict values depending on
        """
        pass

    def nn_fit(self, frame):
        """
        Method fits the nn model
        """
        return frame

    def elm_fit(self, frame):
        """
        Method fits the elm model
        """
        return frame

    def linear_fit(self, frame):
        """
        Method fits the linear model
        """
        return frame

    def online_fcn_fit(self, frame, labels):
        """
        Method fits the elm model
        """
        corona_frame = self.dataframe[["corona_deaths",
                                       "corona_confirmed",
                                       "corona_recovered",
                                       "corona_active",
                                       "new_confirmed",
                                       "corona_new_recovered"]].copy()
        for lbl in labels:
            labels = self.dataframe[[lbl]].values
            self.models[f"online_fcn_{lbl}"] = OnlineFCN(corona_frame, labels, lbl)
        return frame

    def gaussian_fit(self, frame):
        """
        Method fits the linear model
        """
        return frame

    def get_algorithms(self):
        """
        Getter method ML-Algorithem
        """
        return self.__algorithmen


def split_before_after(frames, split_date=dt.datetime(2020, 1, 1)):
    """
    Splits data in two frames the one before and the one after corona.
    We define after corona as after 1.1.2020.
    """
    frames_prior = {}
    frames_post = {}
    for frame in frames:
        frame_prior = frames[frame].loc[frame.Date < split_date]
        frame_post = frames[frame].loc[frame.Date >= split_date]
        frames_prior[frame] = (frame_prior)
        frames_post[frame] = (frame_post)
    return (frames_prior, frames_post)


if __name__ == '__main__':
    LABELS = ["stock_steel", "stock_automotive"]
    ALGORITHMS = ["online_fcn"]
    DATASETS = ["covid", ]
    evaluator = Learning(ALGORITHMS, DATASETS)
