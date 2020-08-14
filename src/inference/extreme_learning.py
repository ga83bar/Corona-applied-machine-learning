import keras
from keras import Sequential
from keras.layers import Dense
from keras.datasets import boston_housing
import numpy as np

# Extreme Learning Class 
class ExtremeLearningMachine():
    '''
    Implementation of extreme Learning machine.
    As proposed in paper from Guang-Bin Huang.
    '''

    def __init__(self, data, layers=1, neurons=128, metric='mean_squared_error',
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
        for layer in range(1, layer):
            self.model.add(Dense(neurons, activation=activation))
        self.model.compile(loss=metric ,optimizer='adam')
        self.model._make_predict_function()

        # Regression part
        self.weights = None

        # dataset
        self.x_train = None
        self.y_train = None

        self.x_test = None
        self.y_test = None

    def prepare_data(self, data):
        '''
        Shifting method that generates a x and y like dataset
        out of a time series.
        '''
        try:
            print('Hallo')
        except expression as identifier:
            pass

    def fit(self, data):
        '''
        The weights of the Extreme Learning Readout
        are calculated in the following method.
        We fit a single data attribute! But with the same nn!
        '''
        train_x, train_y = self.prepare_data(data)

        transformed_features = self.model.predict(train_x)
        sol_eqs = np.linalg.lstsq(transformed_features,train_y,rcond=None)
        self.weights = sol_eqs[0]

    def predict(self,X):
        '''
        Predict method 
        '''

        if self.weights is None:
            raise Exception("Need to call fit() before predict()")
        features = self.model.predict(X)
        return np.matmul(features,self.weights)

def get_prediction_err_and_std(y,y_hat):
    '''
    Calculate Error and std
    '''
    squared_pred_errs = np.square(y.flatten()-y_hat.flatten())
    return np.mean(squared_pred_errs), np.std(squared_pred_errs)

# Hyperparameters
num_layers = 2
num_neurons = 200
activation = "relu"
# ---

# Load the data
(x_train, y_train), (x_test, y_test) = boston_housing.load_data()

# Optional: Preprocess the data (e.g. using the StandardScaler or the MinMaxScaler from scikit-learn)

# First approach: Using Extreme Learning Machines
elm = ExtremeLearningMachine(num_layers,num_neurons,activation,(x_train.shape[1],))

elm.fit(x_train,y_train)
elm_mean_err, elm_std_err = get_prediction_err_and_std(y_test,elm.predict(x_test))
print("Extreme Learning Test Error: " + str(elm_mean_err) + " +- " + str(elm_std_err))

# Second: Train the neural network 
nn = Sequential()
nn.add(Dense(num_neurons,activation=activation,input_shape=(x_train.shape[1],),bias_initializer='glorot_uniform'))
for i in range(1,num_layers):
    nn.add(Dense(num_neurons,activation=activation))
nn.add(Dense(1))
# The loss you define in the next line is used for training - i.e. if you want to incorporate special losses, you'll need to define a new loss function
# Alternatively you can use the keras regularizers: https://keras.io/regularizers/
nn.compile(loss='mean_squared_error',optimizer='adam')
nn.fit(x_train,y_train)
nn_mean_err, nn_std_err = get_prediction_err_and_std(y_test,nn.predict(x_test))
print("Neural Network Test Error: " + str(nn_mean_err) + " +- " + str(nn_std_err))