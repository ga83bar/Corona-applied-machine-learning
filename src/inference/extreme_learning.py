'''
File implemanting Extrem Learning Machine (ELM)
'''
from keras import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np


# Extreme Learning Class
class ExtremeLearningMachine():
    '''
    Implementation of extreme Learning machine.
    As proposed in paper from Guang-Bin Huang.
    '''

    def __init__(self, layers=1, neurons=128, metric='mean_squared_error',
                 activation='relu', input_shape=30):
        '''
        The params define the neural network!
        @param data : the dataset in sequential form
        @param layer : number of layers of the network
        @param neurons : number of neurons
        @param activation : activation function of the neurons
        @param input_shape : number of inputs for the net
        '''
        self.input_shape = input_shape

        # Init neural network
        self.model = Sequential()
        self.model.add(Dense(neurons,
                             activation=activation,
                             input_shape=input_shape,
                             bias_initializer='glorot_uniform'))
        for _ in range(1, layers):
            self.model.add(Dense(neurons, activation=activation))
        self.model.compile(loss=metric, optimizer='adam')
        self.model._make_predict_function()

        # Regression part
        self.weights = None

    def prepare_data(self, data):
        '''
        Shifting method that generates a x and y like dataset
        out of a time series.
        '''

        print(data.head())
        x_train, y_train = pd.DataFrame()

        # TODO implement

        return (x_train, y_train)


    def fit(self, data):
        '''
        The weights of the Extreme Learning Readout
        are calculated in the following method.
        We fit a single data attribute! But with the same nn!
        '''
        train_x, train_y = self.prepare_data(data)

        transformed_features = self.model.predict(train_x)
        sol_eqs = np.linalg.lstsq(transformed_features, train_y, rcond=None)
        self.weights = sol_eqs[0]

    def predict(self, x_vals):
        '''
        Predict method
        '''

        if self.weights is None:
            raise Exception("Need to call fit() before predict()")
        features = self.model.predict(x_vals)
        return np.matmul(features, self.weights)

def get_prediction_err_and_std(y, y_hat):
    '''
    Calculate Error and std
    '''

    squared_pred_errs = np.square(y.flatten()-y_hat.flatten())
    return np.mean(squared_pred_errs), np.std(squared_pred_errs)


def test():
    ''' DUMMY'''

    data = pd.DataFrame()
    elm = ExtremeLearningMachine(data)

    # TODO
