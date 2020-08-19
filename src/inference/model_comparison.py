"""
Compares the performance of simple regression models on a common dataset using cross-validation.
Performance is judged based on the MSE of each model.
"""
# from fbprophet import Prophet
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import cross_validate

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def get_model_list():
    """returns a list containing available regressors for model comparison"""
    model_list = [('DecisionTree', DecisionTreeRegressor()), ('NeuralNetwork', MLPRegressor(shuffle=False)),
                  ('LinearModel', LinearRegression()), ('PolyLinearModel', LinearRegression())]  
    return model_list

def compare_models(model_list, dataframe):
    """compares the performance of given models using the provided dataframe by performing cross validation"""
    score_list = list()
    data_table = np.array(df.index.values.reshape(-1, 1))
    for model in model_list:
        score_dict = dict()
        df['stock_tech'].fillna(method='backfill', inplace=True)
        score = cross_validate(model[1], data_table, dataframe['stock_tech'], return_estimator=True)
        score_dict['model_name'] = model[0]
        score_dict['MSE'] = sum(abs(score['test_score']))/len(score['test_score'])
        score_dict['estimator'] = score['estimator']
        score_list.append(score_dict)
    return score_list


if __name__ == '__main__':
    PATH = Path().absolute().parent.parent.joinpath('res', 'pipeline', 'scaled_pre_corona_df.csv')
    df = pd.read_csv(PATH)
    model_lst = get_model_list()
    score_lst = compare_models(model_lst, df)
    least_mse = np.inf
    BEST_MODEL = ''
    for score_dct in score_lst:
        if score_dct['MSE'] < least_mse:
            least_mse = score_dct['MSE']
            BEST_MODEL = score_dct['model_name']
    print('The best model with 5-fold cross validation was {} with an MSE of {}'.format(best_model, least_mse))
    plt.plot(df.index.values, df['stock_tech'])
