'''
File ...
'''
import os
import datetime as dt
import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense
from keras.datasets import boston_housing
from scipy.optimize import minimize


# TODO include in dependencies

class Learning():
    '''
    No time - learning
    '''
    # ML algos
    NN = 1
    ELM = 2
    LSTM = 3
    LINEAR = 4
    GP = 5

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

        # TODO
        # frame_predict = self.predict(frame_before_corona)

        # calculate the difference between real and prediction
       #  diff_frame = self.calculate_difference(frame_predict, frame_after_corona)

        # plot the diff or something like that

    def predict(self):
        '''
        Predict values depending on
        '''
        pass
        # load model


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

# Extrem eLearning machine
class ExtremeLearningMachine():
    def __init__(self, layer, neurons, activation, input_shape):
        self.model = Sequential()
        self.model.add(Dense(neurons, activation=activation, input_shape=input_shape, bias_initializer='glorot_uniform'))
        for i in range(1, layer):
            self.model.add(Dense(neurons, activation=activation, bias_initializer='glorot_uniform'))
        self.model.compile(loss='mean_squared_error',optimizer='adam')
        self.model._make_predict_function()

    # Definition of the regularization function (w are the weights of the readout - regularization on the hidden weights does not make sense as they are not trained)
    def reg_fun(self, w):
        # 2-Norm regularization just as an example
        return np.linalg.norm(w, ord=2)

    # Target function for the ELM training (Least-Squares Formula)
    def lstsq_target(self, w):
        return np.sum(np.square(np.matmul(self.transformed_features, w).flatten()-self.trainY.flatten()))

    # Combination of Least-Squares loss and regularization function
    def optim_fun(self, w):
        return self.lstsq_target(w) + self.reg_fun(w)

    def fit(self, trainX, trainY, regularization_fun):
        # The transformed features and the trainY are stored as variables of the class such that the optimization functions have access to them without passing them as parameters to the function
        self.transformed_features = self.model.predict(trainX)
        self.trainY = trainY.copy()
        # Use the scipy function for (numerical) optimization (using BFGS)
        res = minimize(self.optim_fun, np.zeros((self.transformed_features.shape[1],)))
        # Store the weights as usually
        self.weights = res.x

    def predict(self, X):
        if not hasattr(self,"weights"):
            raise Exception("Need to call fit() before predict()")
        features = self.model.predict(X)
        return np.matmul(features, self.weights)



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
    elif algo == Learning.GP:
        return True
    else:
        return False


def get_prediction_err_and_std(y,y_hat):
    squared_pred_errs = np.square(y.flatten()-y_hat.flatten())
    return np.mean(squared_pred_errs), np.std(squared_pred_errs)


# Example for elm

if __name__=='__main__':
    (trainX, trainY), (testX, testY) = boston_housing.load_data()
    elm = ExtremeLearningMachine(2,200,"relu",(trainX.shape[1],))

    elm.fit(trainX,trainY,elm.reg_fun)

    pred = elm.predict(testX)

    err, std = get_prediction_err_and_std(pred,testY)
    print("Error: " + str(err) + " +- " + str(std))