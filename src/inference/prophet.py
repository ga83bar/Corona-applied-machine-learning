'''
Strange method implemented by Facebook.
With your personal data you support such cool tools.
Thanks for this =)
'''
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from fbprophet import Prophet
import plotly.offline as py
py.init_notebook_mode()

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
        data['Date'] = data['Date'].apply(lambda x: x[:-15])
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
            # fig = plot_plotly(model, forecast)  # This returns a plotly Figure
            # py.iplot(fig)

        return forecast['yhat']

def test():
    '''
    Test function
    '''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'all_raw.csv')
    loaded_data = pd.read_csv(dataset_path)
    print(loaded_data.head())
    attr = 'AMZN'

    pro = MyProphet()
    pro.fit(data=loaded_data[['Date', attr]], do_plot=True)

if __name__ == '__main__':
    test()
