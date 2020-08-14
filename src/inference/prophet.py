'''
Strange method implemented by Facebook.
With your personal data you support such cool tools.
Thanks for this =)
'''

import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt

class MyProphet:
    ''' 
    Prophet class for handling forecasts.
    '''

    def __init__(self):
        '''
        Input data must be a dataframe containing a Date and a target value.
        '''
        self.cols = ['ds', 'y']

    def fit(self, data, do_plot=False):
        '''
        Data must be a pd frame in the form Date | y
        '''
        name = data.columns[1]
        print('Predict ' + str(name))
        data.columns = self.cols
        model = Prophet()
        model.fit(data)

        future = model.make_future_dataframe(periods=65)

        forecast = model.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

        if do_plot:
            fig1 = model.plot(forecast)
            fig2 = model.plot_components(forecast)
            plt.show()
