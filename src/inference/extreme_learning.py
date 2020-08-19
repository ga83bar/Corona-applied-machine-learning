'''
File implemanting Extrem Learning Machine (ELM)
'''
from pathlib import Path
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
                 activation='relu', error_measure='mse', test_train_split=0.66, input_shape=30):
        '''
        The params define the neural network!
        @param data : the dataset in sequential form
        @param layer : number of layers of the network
        @param neurons : number of neurons
        @param activation : activation function of the neurons
        @param input_shape : number of inputs for the net
        @param error_measure : error measure e.g mse
        '''
        self.input_shape = input_shape
        self.train_test_split = test_train_split
        self.error_measure = error_measure

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

        # Data dependent things
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        # Regression part
        self.weights = None

    def prepare_data(self, data):
        '''
        Shifting method that generates a x and y like dataset
        out of a time series.
        @param data: 1-D List containing the data.
        '''
        train_samples = int(len(data) * self.train_test_split)
        test_samples = len(data) - train_samples
        print('The number of train samples is {} and test samples {}'.format(train_samples, test_samples))

        for iterator in range(self.input_shape, len(data)):
            if iterator < train_samples:
                self.x_train.append(data[iterator-self.input_shape:iterator])
                self.y_train.append(data[iterator])
            else:
                self.x_test.append(data[iterator-self.input_shape:iterator])
                self.y_test.append(data[iterator])

    def fit(self, data):
        '''
        The weights of the Extreme Learning Readout
        are calculated in the following method.
        We fit a single data attribute! But with the same nn!
        '''
        self.prepare_data(data)

        transformed_features = self.model.predict(self.x_train)
        sol_eqs = np.linalg.lstsq(transformed_features, self.y_train, rcond=None)
        self.weights = sol_eqs[0]

        y_predict = self.predict(self.x_test)

        if self.error_measure == 'mse':
            error = self.mse(y_predict)
        # Default value == MSE
        else:
            error = self.mse(y_predict)

        print('Error (type: {}) value {}'.format(self.error_measure, error))
        return error

    def predict(self, x_vals):
        '''
        Predict method
        '''

        if self.weights is None:
            raise Exception("Need to call fit() before predict()")
        features = self.model.predict(x_vals)
        return np.matmul(features, self.weights)

    def mse(self, y_predict):
        '''
        Calculate mean squared error
        '''
        error = np.square(self.y_test - y_predict.flatten())
        return error


def test():
    ''' DUMMY'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'all_raw.csv')
    loaded_data = pd.read_csv(dataset_path)
    attr = 'AMZN'
    elm = ExtremeLearningMachine()
    elm.fit(loaded_data[attr])


if __name__ == '__main__':
    test()
