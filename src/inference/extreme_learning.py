'''
File implemanting Extrem Learning Machine (ELM).
I tried to make this class scjíkit learn compatibel
(see :https://scikit-learn.org/stable/developers/develop.html)
'''
from pathlib import Path
from abc import ABCMeta, abstractmethod
from keras import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np

# For scikitlearn cross validation
from sklearn.model_selection import cross_val_score
from sklearn.base import BaseEstimator


# Base class for extreme learning machine implements
# scikit learn methods
class BaseModel(metaclass=ABCMeta):
    '''
    Base model class for extrem learning machine and hopfully also for the other classes.
    '''
    def __init__(self, error_measure, train_window):
        self.__error_measure = error_measure
        self.train_window = train_window

    @abstractmethod
    def fit(self, x_train, y_train):
        '''
        Scikit learn base method that trains the model.
        @param x_train : x values of the train data
        @param y_train : y values of the train data
        @return None
        '''
        raise NotImplementedError

    @abstractmethod
    def score(self, x_test, y_test):
        '''
        Scoreing method, that evaluates the test error and returns it!
        '''
        raise NotImplementedError

    # Error measure dependent things
    def get_error_measure(self):
        '''
        Getter method error measure
        '''
        return self.__error_measure

    def set_error_measure(self, error_measure):
        '''
        Setter method for error measure.
        @param error_measure : error measure e.g mse, mae
        @return : boolean value indicates if we seted the value or not
        '''
        if isinstance(error_measure, str):
            if (error_measure == 'mse' or error_measure == 'mae'):
                self.__error_measure = error_measure
                return True
            else:
                print('{} is no valid Error measure for ELM'.format(error_measure))
                return False
        else:
            print('Your input is not even a string =(')
            return False

    def prepare_data(self, data):
        '''
        Shifting method that generates a x and y like dataset
        out of a time series.
        @param data: 1-D List containing the data.
        '''
        x_train_test = []
        y_train_test = []

        for iterator in range(self.train_window, len(data)):
            x_train_test.append(data[iterator-self.train_window:iterator])
            y_train_test.append(data[iterator])

        return(x_train_test, y_train_test)

    def mse(self, y_real, y_predict):
        '''
        Calculate mean squared error
        '''
        error = np.square(y_real - y_predict)
        return error

    def mae(self, y_real, y_predict):
        '''
        Calculate the Mean Absolute error
        '''
        error = np.sum(y_real -y_predict)
        return error

    # Prpoerties
    error_measure = property(get_error_measure, set_error_measure)


# Extreme Learning Class
class ExtremeLearningMachine(BaseModel, BaseEstimator):
    '''
    Implementation of extreme Learning machine.
    As proposed in paper from Guang-Bin Huang.
    '''


    def __init__(self, layers=1, neurons=128, metric='mean_squared_error',
                 activation='relu', error_measure='mse', test_train_split=0.66, train_window=30):
        '''
        The params define the neural network!
        @param data : the dataset in sequential form
        @param layer : number of layers of the network
        @param neurons : number of neurons
        @param activation : activation function of the neurons
        @param train_window : number of inputs for the net
        @param error_measure : error measure e.g mse
        '''

        # Call parent Constructor
        super(ExtremeLearningMachine, self).__init__(error_measure=error_measure,
                                                     train_window=train_window)

        self.alph = 0.001
        self.neurons = neurons

        self.train_window = train_window
        self.train_test_split = test_train_split

        # Init neural network
        self.model = Sequential()
        self.model.add(Dense(neurons,
                             activation=activation,
                             input_shape=(train_window, ),
                             bias_initializer='glorot_uniform'))
        for _ in range(1, layers):
            self.model.add(Dense(neurons, activation=activation))
        self.model.compile(loss=metric, optimizer='adam')
        self.model._make_predict_function()

        # Regression part
        self.weights = None

    def fit(self, x_train, y_train):
        '''
        The weights of the Extreme Learning Readout
        are calculated in the following method.
        We fit a single data attribute! But with the same nn!
        '''
        transformed_features = self.model.predict(x_train)
        sol_eqs = np.linalg.lstsq(transformed_features, y_train, rcond=None)
        self.weights = sol_eqs[0]

    def score(self, x_test, y_test):
        '''
        Scoring method returns test error
        '''
        y_predict = self.predict(x_test)

        if self.__error_measure == 'mse':
            error = self.mse(y_predict, y_test)
        # Default value == MSE
        else:
            error = self.mse(y_predict, y_test)

        return error

    def predict(self, x_vals):
        '''
        Predict method
        '''
        if self.weights is None:
            raise Exception("Need to call fit() before predict()")
        features = self.model.predict(x_vals)
        return np.matmul(features, self.weights)


def test():
    ''' DUMMY'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'pipeline', 'scaled_corona_df.csv')
    loaded_data = pd.read_csv(dataset_path)

    elm = ExtremeLearningMachine()

    x_train_test, y_train_test = elm.prepare_data(loaded_data['stock_automotive'])

    scores = cross_val_score(elm, x_train_test, y_train_test, cv=5)
    print('scores ELM:')
    print(scores)


if __name__ == '__main__':
    test()
