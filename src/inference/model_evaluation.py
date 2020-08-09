'''
File ...
'''
import os
import pandas as pd
import datetime as dt

# classs ...#
# (1) load data from ...
# (2) cut of values bigger 1.1.2020
# (3) x/y split ??
# (4) train test split


class Learning():
    '''
    No time - learning
    '''
    # ML algos
    NN = 1
    ELM = 2
    LSTM = 3
    LINEAR = 4

    # Constructor
    def __init__(self, algorithem):
        self.__algorithem = algorithem

    # HEAVY STUFF!!
    def load_data(self):
        '''
        Loads the preprocessed data from csv, or if this does not exist
        we start the preprocess pipline.
        '''
        # TODO Martin ???
        file_path = 'some path'

        if os.path.exists(file_path):
            frame = pd.read_csv(file_path)

        else:
            try:
                # TODO Martin start pipline
                frame = pd.DataFrame()
            except Exception as ex_er:
                print('Error occured during preprocess pipline')
                print(ex_er)

        return frame

    def split_before_after(self, frame, split_date=None):
        '''
        Splits data in two frames the one before and the one after corona.
        We define after corona as after 1.1.2020.
        '''
        if split_date is None:
            date = dt.datetime(2020, 1, 1)
        else:
            date = split_date

        before = frame.loc[frame.Date < date]
        after = frame.loc[frame.Date >= date]
        return (before, after)

    def fit(self, frame):
        '''
        Predict the futre data 
        from    1.1.2020
        to      1.6.2020
        @param frame : Pandas frame containing the data till 31.12.2019
        @return Pandas frame containing the predicted data
        '''
        if self.__algorithem == Learning.NN:
            frame = self.nn_fit(frame)

        elif self.__algorithem == Learning.ELM:
            frame = self.elm_fit(frame)

        elif self.__algorithem == Learning.LSTM:
            frame = self.lstm_fit(frame)

        elif self.__algorithem == Learning.LINEAR:
            frame = self.linear_fit(frame)

        return frame

    # TODO section
    def nn_fit(self, frame):
        '''
        Method that implements ...
        '''
        return frame

    def elm_fit(self, frame):
        '''
        Method that implements ...
        '''
        return frame

    def lstm_fit(self, frame):
        '''
        Method that implements ...
        '''
        return frame

    def linear_fit(self, frame):
        '''
        Method that implements ...
        '''
        # print or even return score or we write it in a file??!
        return frame

    def calculate_difference(self, frame_predict, frame_real):
        '''
        Method calculating the difference between the real and the predicted data
        '''
        return frame_real - frame_predict

    def pipeline(self):
        frame = self.load_data()
        frame_before_corona, frame_after_corona = self.split_before_after(frame)
        # make the prediction accoring to precorona data

        self.fit(frame_before_corona)

        frame_predict = self.predict(frame_before_corona)

        # calculate the difference between real and prediction
        diff_frame = self.calculate_difference(frame_predict, frame_after_corona)

        # plot the diff or something like that

    def predict(self):
        '''
        Predict values depending on
        '''
        pass

    # GETTER AND SETTER
    def set_algorithem(self, algorithem):
        '''
        Setter method ML-Algorithem
        '''
        if is_algo_valid(algorithem):
            self.__algorithem = algorithem
        else:
            raise Exception('Select a valid Algorithem!!')

    def get_algorithem(self):
        '''
        Getter method ML-Algorithem
        '''
        return self.__algorithem

    # PROPERTIES
    algorithem = property(get_algorithem, set_algorithem)

# Helping functions
def is_algo_valid(algo):
    '''
    No time - check if algo is valid
    '''
    if algo == Learning.NN:
        return True
    elif algo == Learning.LSTM:
        return True
    elif algo == Learning.ELM:
        return True
    else:
        return False
