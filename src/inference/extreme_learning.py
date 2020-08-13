'''
Extreme Learning Machine (ELM):
ELM is a machine Learning model key concept is that we ini a neural network random.
After that we put the data in the network and make a regression.
'''
import os
from pathlib import Path
import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense


class ExtremeLearningMachine():
    '''
    Extreme Learning Machine (ELM):
    The concept of an ELM is explained in detail in the documentation.
    '''
    def __init__(self, dataframe=None, input_shape=(30,), layer=1, neurons=200, activation='relu'):
        # data
        self.dataframe = dataframe
        self.input_shape = input_shape

        # neural network
        self.model = Sequential()
        self.model.add(Dense(neurons, activation=activation,
                             input_shape=input_shape,
                             bias_initializer='glorot_uniform'))
        print('Hallo')
        for _ in range(1, layer):
            self.model.add(Dense(neurons, activation=activation,
                                 bias_initializer='glorot_uniform'))

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model._make_predict_function()

        # regression
        self.weights = None

    def load_data(self, file=None):
        """
        Loads data
        """
        if file is None:
            path = Path(__file__).resolve().parent.parent.parent  # remove last one
            # path = os.path.join(path, 'data_management')
            path = os.path.join(path, 'res', 'all_raw.csv')
            print(path)
            self.dataframe = pd.read_csv(path)
            self.resample()

    def resample(self):
        """
        Resample data
        """
        # TODO
        data = self.dataframe['AMZN']
        my_frame = pd.DataFrame()
        for i in data:
            my_frame.append(data[[j + i for j in range((self.input_shape) + 1)]])
            if (i + ((self.input_shape) + 1) == len(data)):
                break
        print(my_frame.head())

    def fit(self, train_x, train_y):
        '''
        The transformed features and the trainY are stored as variables
        of the class such that the optimization functions have access to
        them without passing them as parameters to the function
        '''
        transformed_features = self.model.predict(train_x)
        sol_eqs = np.linalg.lstsq(transformed_features, train_y, rcond=None)
        self.weights = sol_eqs[0]

    def predict(self, inp):
        """
        Make predictions based on model
        """
        if self.weights is None:
            raise Exception("Need to call fit() before predict()")
        # put it in nn
        features = self.model.predict(inp)
        # calc linear combos
        return np.matmul(features, self.weights)


def get_prediction_err_and_std(y_in, y_hat):
    """
    Calculate MSE
    """
    squared_pred_errs = np.square(y_in.flatten()-y_hat.flatten())
    return np.mean(squared_pred_errs), np.std(squared_pred_errs)

# https://machinelearningmastery.com/time-series-forecasting/#:~:text=Making%20predictions%20about%20the%20future,handling%20of%20time%20series%20data.&text=Forecasting%20involves%20taking%20models%20fit,them%20to%20predict%20future%20observations.


# Example for elm
if __name__ == '__main__':
    '''
    (trainX, trainY), (testX, testY) = boston_housing.load_data()
    elm = ExtremeLearningMachine(2, 200,"relu", (trainX.shape[1],))

    elm.fit(trainX,trainY,elm.reg_fun)

    pred = elm.predict(testX)
    err, std = get_prediction_err_and_std(pred, testY)
    print("Error: " + str(err) + " +- " + str(std))
    '''
    ELM = ExtremeLearningMachine()
    ELM.load_data()