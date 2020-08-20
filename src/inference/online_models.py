"""
Implementation of online models for our dataset
"""
import numpy as np
from matplotlib import pyplot as plt
from keras.layers import concatenate
from keras.layers import Dense
from keras.layers import Input
from keras.models import Model



class OnlineDense():
    """
    Class contains an online linear model and all of its pre and post
    training attributes.
    """
    def __init__(self, dataframe, output, dset, settings):
        """
        Constructor
        """
        self.dataframe = dataframe
        self.settings = self.init_settings(settings)
        self.predictions = []
        self.model = None
        self.dset = dset
        self.output = output
        self.metrics = ['mse']
        self.data_length = None

    def setup_model(self):
        """
        Model setup
        """
        neurons = self.settings["neurons"]
        input_a = Input(shape=(1,))
        input_b = Input(shape=(self.settings["in_dim"],))
        inp_a = Dense(4, activation="linear")(input_a)
        inp_b = Dense(12, activation=self.settings["lay_activ"])(input_b)
        for layer in range(1, self.settings["layers"]):
            inp_b = Dense(neurons[layer], activation=self.settings["lay_activ"])(inp_b)
        inp_b = Dense(1, activation=self.settings["out_activ"])(inp_b)
        combined = concatenate([inp_a.output, inp_b.output])
        out = Dense(2, activation="relu")(combined)
        out = Dense(1, activation="linear")(out)
        self.model = Model(inputs=[inp_a.input, inp_b.input], outputs=out)
        self.model.compile(loss=self.settings["loss"], optimizer='adam', metrics=self.metrics)
        return self.model

    def set_metric(self, metrics):
        """
        Set the desired performance metric
        """
        self.metrics = metrics
        return self.metrics


    def do_fitting(self):
        """
        Train the model
        """
        window = self.settings["window"]
        for itr in range(0, 1000):
            inp_a, inp_b, out = self.data_transform(itr + 1, itr + window)
            inp = np.hstack(inp_a, inp_b)
            self.model.fit(inp, out, epochs=1, batch_size=window)
            if itr == 0:
                self.predictions = self.model.predict()
            last = inp_b[-1]
            future_step = [(last[1]%12) + 1, (last[2]%7) +1]
            prediction = self.model.predict(future_step)
            self.predictions.append(prediction)
            if itr >= self.data_length:
                self.dataframe.append(future_step[1], future_step[2])
                self.output.append(prediction)
        return self.predictions

    def data_transform(self, start, end):
        """
        Pandas to Numpy
        """
        inp_a = range(start, end)
        inpt_b = self.dataframe[["month", "day"]].copy().to_numpy()
        inp_b = inpt_b[start:end, :]
        out = self.output[start:end]
        return inp_a, inp_b, out

    def plot(self):
        """
        Plot predictions against labels
        """

    def save_model(self):
        """
        Saves a model
        """

    def load_model(self, time):
        """
        Loads a pretrained model
        """

    def init_settings(self, settings):
        """
        Initialize settings
        """
        self.settings = {"in_dim":2,
                         "layers:":2,
                         "lay_activ":"relu",
                         "out_activ":"linear",
                         "neurons":[10, 8],
                         "loss":"mean_squared_error",
                         "window":365,
                         "end":1000}
        for setter in settings:
            self.settings[setter] = settings[setter]
        return self.settings
