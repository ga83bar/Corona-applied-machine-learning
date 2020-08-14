"""
This module serves as the hub for the model evaluation and training
"""
import datetime as dt
from load_in import LoadIn
from online_fcn import OnlineFCN
#from extreme_learning import ExtremeLearningMachine
#from prophet import MyProphet
import calendar


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
        self.dataframes = self.loader.load_all(typ="pre")
        self.dataframe = self.loader.get_all()
        self.dataframe = month_and_day(self.dataframe)
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
        if "online_time_pred" in self.__algorithmen:
            output_frames["online_time_pred"] = self.online_pred_fit(frame)
        return output_frames

    def predict(self):
        """
        Predict values depending on
        """
        pass
    
    def online_pred_fit(self, frame):
        """
        Calc future trends based on past trends
        """
        return frame

    def nn_fit(self, frame):
        """
        Method fits the nn model
        """
        return frame

    def prophet_fit(self, frame):
        '''
        Method fits prophet
        '''
        attribute = ''
        proph = MyProphet()
        #for attribute in frame:
        proph.fit(frame['Date', attribute])


    def elm_fit(self, frame):
        """
        Method fits the elm model
        """
        #elm = ExtremeLearningMachine(self.dataframe)
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
            labels = self.dataframe[[lbl]].copy().pop(lbl)
            print(labels)
            online_fcn = OnlineFCN(corona_frame, labels, lbl)
            online_fcn.set_metric()
            online_fcn.setup_model()
            online_fcn.do_fitting()
            online_fcn.plot()
            self.models[f"online_fcn_{lbl}"] = online_fcn
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


def month_and_day(dataframe):
    """
    Get month and day from dates in dataframe.
    Append to dataframe.
    """
    dates = dataframe[["Date"]].copy().pop("Date")
    month = []
    day = []
    for date in dates:
        date = dt.datetime.strptime(date, '%Y-%m-%d')
        weekday = calendar.day_name[date.weekday()]
        month.append(date.strftime('%B'))
        day.append(weekday)
    dataframe["month"] = month
    dataframe["day"] = day
    return dataframe


if __name__ == '__main__':
    LABELS = ["ix_bitrate"]
    LABELS_1 = ["ix_bitrate",
              "youtube_viewchange",
              "youtube_views",
              "steam_users",
              "steam_ingame",
              "twitch_views",
              "twitch_channels",
              "twitch_viewtime",
              "twitch_streams",
              "ps_users",
              "stock_med",
              "stock_bank",
              "stock_energy",
              "stock_oil",
              "stock_steel",
              "stock_automotive",
              "stock_telecom",
              "stock_tech"]
    ALGORITHMS = ["online_time_pred"]
    DATASETS = ["covid"]
    EVALUATOR = Learning(ALGORITHMS, DATASETS)
    EVALUATOR.pipeline()


