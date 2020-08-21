'''
File implemanting Extrem Learning Machine (ELM).
I tried to make this class scjíkit learn compatibel
(see :https://scikit-learn.org/stable/developers/develop.html)

How to use this class:
(1) Run fit before predict!
(2) The input for the fit method are the stacked time series data!
    As you get (for every attribute) from :
    x_train_test, y_train_test = elm.prepare_data(loaded_data['stock_automotive'])
'''
from pathlib import Path
from keras import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

# For scikitlearn cross validation
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

# Constants
TRAIN_WINDOW = 30

# Extreme Learning Class
class ExtremeLearningMachine(BaseEstimator, ClassifierMixin):
    '''
    Implementation of extreme Learning machine.
    As proposed in paper from Guang-Bin Huang.
    Can be used like any scikit learn predictor.
    '''

    def __init__(self, neurons=128, lambd=0.01):
        '''
        The params define the neural network!
        @param data : the dataset in sequential form
        @param layer : number of layers of the network
        @param neurons : number of neurons
        @param activation : activation function of the neurons
        @param train_window : number of inputs for the net
        @param error_measure : error measure e.g mse
        '''
        self.lambd = lambd
        self.neurons = neurons

    def fit(self, x_train, y_train):
        '''
        The weights of the Extreme Learning Readout
        are calculated in the following method.
        We fit a single data attribute! But with the same nn!
        '''
        # To be scikit learn comp we build the model outside the init method
        self.build_network()
        self.__measure = 'mse'

        transformed_features = self.model.predict(x_train)
        sol_eqs = np.linalg.lstsq(transformed_features, y_train, rcond=None)
        self.weights = sol_eqs[0]

    def score(self, x_test, y_test):
        '''
        Scoring method returns test error
        '''
        y_predict = self.predict(x_test)

        if self.__measure == 'mse':
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

    def build_network(self, neurons=128, layers=1, train_window=TRAIN_WINDOW,
                      activation='relu', metric='mean_squared_error'):
        '''error_measure
        Method that builds and compiles the model (network)
        '''
        # Init neural network
        self.model = Sequential()
        self.model.add(Dense(neurons,
                             activation=activation,
                             input_shape=(train_window,),
                             bias_initializer='glorot_uniform'))
        for _ in range(1, layers):
            self.model.add(Dense(neurons, activation=activation))
        self.model.compile(loss=metric, optimizer='adam')
        self.model._make_predict_function()

        # Regression part
        self.weights = None

    def prepare_data(self, data, train_window=TRAIN_WINDOW):
        '''
        Shifting method that generates a x and y like dataset
        out of a time series.
        @param data: 1-D List containing the data.
        '''
        x_train_test = []
        y_train_test = []

        for iterator in range(train_window, len(data)):
            x_vals = data[(iterator-train_window):iterator]
            x_train_test.append(x_vals)
            y_train_test.append(data[iterator])

        # cast this stuff to numpy
        x_train_test = np.array(x_train_test)
        y_train_test = np.array(y_train_test)

        return x_train_test, y_train_test
    # Error measure dependent things
    def get_error_measure(self):
        '''
        Getter method error measure
        '''
        return self.__measure

    def set_error_measure(self, error_measure):
        '''
        Setter method for error measure.
        @param error_measure : error measure e.g mse, mae
        @return : boolean value indicates if we seted the value or not
        '''
        if isinstance(__measure, str):
            if (__measure == 'mse' or __measure == 'mae'):
                self.__measure = error_measure
                return True
            else:
                print('{} is no valid Error measure for ELM'.format(error_measure))
                return False
        else:
            print('Your input is not even a string =(')
            return False

    def mse(self, y_real, y_predict):
        '''
        Calculate mean squared error
        '''
        difference_array = np. subtract(y_real, y_predict)
        squared_array = np. square(difference_array)
        mse = squared_array. mean()
        return mse

    def mae(self, y_real, y_predict):
        '''
        Calculate the Mean Absolute error
        '''
        error = np.sum(y_real -y_predict)
        return error

    # Prpoerties
    error_measure = property(get_error_measure, set_error_measure)


def test():
    ''' Test running sckikit learn cross validation'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'pipeline', 'scaled_corona_df.csv')
    loaded_data = pd.read_csv(dataset_path)
    elm = ExtremeLearningMachine()

    # Test if it works as expected
    my_train_attr = ['stock_automotive', 'stock_energy']
    for attr in my_train_attr:
        # First step prepare dat
        x_train_test, y_train_test = elm.prepare_data(loaded_data[attr])
        scores = cross_val_score(elm, x_train_test, y_train_test, cv=5)
        print('scores ELM:')
        print(scores)

def test_grid_search():
    ''' Test running sckikit learn cross validation'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'pipeline', 'scaled_corona_df.csv')
    loaded_data = pd.read_csv(dataset_path)
    elm = ExtremeLearningMachine()

    # Test if it works as expected
    my_train_attr = ['stock_automotive', 'stock_energy']
    for attr in my_train_attr:
        print(elm.get_params())

        # First step prepare dat
        x_train_test, y_train_test = elm.prepare_data(loaded_data[attr])
        # Set the parameters by cross-validation
        tuned_parameters = {'neurons': [1, 10, 20],
                            'lambd' : [0, 0.0001, 0.001, 0.01]},
        clf = GridSearchCV(
        ExtremeLearningMachine(), tuned_parameters)
        clf.fit(x_train_test, y_train_test)
        print(clf.best_params_)


if __name__ == '__main__':
    # test()
    test_grid_search()
