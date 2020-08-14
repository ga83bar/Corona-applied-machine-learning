from fbprophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def get_model_list():
    model_list = [('LinearModel', LinearRegression())]  # ('Prophet', Prophet())
    return model_list

def compare_models(model_list, df):
    score_list = list()
    for model in model_list:
        score_dict = dict()
        df['stock_tech'].fillna(method='backfill', inplace=True)
        score = cross_validate(model[1], df.index.values.reshape(-1, 1), df['stock_tech'], return_estimator=True)
        score_dict['model_name'] = model[0]
        print(score['test_score'])
        score_dict['MSE'] = sum(score['test_score'])/len(score['test_score'])
        score_dict['estimator'] = score['estimator']
        score_list.append(score_dict)
    return score_list

if __name__ == '__main__':
    PATH = Path().absolute().parent.parent.joinpath('res', 'pipeline', 'scaled_pre_corona_df.csv')
    df = pd.read_csv(PATH)
    model_list = get_model_list()
    score_list = compare_models(model_list, df)
    least_mse = np.inf
    best_model = ''
    for score_dict in score_list:
        if score_dict['MSE'] < least_mse:
            least_mse = score_dict['MSE']
            best_model = score_dict['model_name']
    print('The best model with 5-fold cross validation was {} with an MSE of {}'.format(best_model, least_mse))
    plt.plot(df.index.values, df['stock_tech'])
