"""
Compares the performance of simple regression models
on a common dataset using cross-validation.
Performance is judged based on the MSE of each model.
"""
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt

import joblib

from src.inference import extreme_learning as EM
from src.inference import prophet as pro
from src.inference.load_in import LoadIn


def get_model_list():
    """returns a list containing available regressors for model comparison"""
    model_list = [('DecisionTree', DecisionTreeRegressor()),
                  ('NeuralNetwork', MLPRegressor(shuffle=False)),
                  ('LinearModel', LinearRegression()),
                  ('PolyLinearModel', LinearRegression())]

    return model_list


def load_models():
    ELM = EM.ExtremeLearningMachine()
    Prophet = pro.MyProphet()
    model_dict = {"ELM": ELM, "Prophet": Prophet}
    return model_dict


def get_params(df, ELM=False, prophet=False):
    """
    performs grid search
    """
    if prophet is True:
        param_dict = {}
        prophet_dataframes_pre = LoadIn().load_all(typ='pre')
        for label in prophet_dataframes_pre:

            if label == "Unnamed: 0":
                continue
            if label == 'corona_deaths':
                break
            print(label)
            prophet_attr_df_pre = prophet_dataframes_pre[["Date", label]]
            prophet_attr_df_pre = prophet_attr_df_pre.dropna()
            prophet = pro.MyProphet()

            changepoint_prior_scale = np.arange(0.03, 0.2, 0.005)
            parameters = {'growth': ['linear', 'logistic'],
                          'changepoint_prior_scale': changepoint_prior_scale,
                          'interval_width': [0.8],
                          'seasonality_mode': ['additive', 'multiplicative']}
            best_params = prophet.gridsearchcv(parameters,
                                               dataframe=prophet_attr_df_pre,
                                               safe=True)
            param_dict[label] = best_params
    if ELM is True:
        # ELM
        param_dict = {}
        lambdalst = []
        lambdalst = [0.001, 0.005, 0.01, 0.025, 0.05,
                     0.075, 0.1, 0.25, 0.5, 0.75, 1]
        neuronlst = [20, 40, 60, 80, 100, 120, 140, 150]

        for attribute in df:
            if attribute == "Unnamed: 0":
                continue
            if attribute == 'corona_deaths':
                break
            print(attribute)
            ELM_param_grid = {'neurons': neuronlst,
                              'lambd': lambdalst,
                              'regu': ['no', 'L1', 'L2']},
            elm = EM.ExtremeLearningMachine()
            df[attribute].fillna(method='backfill', inplace=True)
            X, y = elm.prepare_data(df[attribute])
            search = GridSearchCV(EM.ExtremeLearningMachine(), ELM_param_grid)
            search.fit(X, y)
            param_dict[attribute] = search.best_params_

            break
        print(param_dict)
    return 0


def get_predict_data(label):
    """
    Loads dataframes and Predicts data,  outputs predicted points as df
    Input label of attribute to predict, for example ix_bitrate in str format
    Output: all full n pre and post raw dataframes
            dataframes with attribute and date without NaN
            prediction datframe starting at teh first of January
    """
    prophet_dataframes_pre = LoadIn().load_all(typ='pre')
    prophet_dataframes_post = LoadIn().load_all(typ='post')
    prophet_attr_df_pre = prophet_dataframes_pre[["Date", label]]
    prophet_attr_df_pre = prophet_attr_df_pre.dropna()
    prophet_attr_df_post = prophet_dataframes_post[["Date", label]]
    prophet_attr_df_post = prophet_attr_df_post.dropna()

    prophet = pro.MyProphet()
    prophet.fit(prophet_attr_df_pre['Date'], prophet_attr_df_pre[label])
    prophet_output = prophet.predict(do_plot=False, label=label)
    predicted_df = prophet_output["yhat"]
    lower_bound_df = prophet_output["yhat_lower"]
    upper_bound_df = prophet_output["yhat_upper"]

    pipeline_path = Path(__file__).parent.parent.parent.joinpath('res',
                                                                 'pipeline')
    scaler_path = pipeline_path.joinpath('scaler_'+label+'.save')

    scaler = joblib.load(scaler_path)

    predicted_df = scaler.inverse_transform(predicted_df)

    prophet_attr_df_post[label] = scaler.inverse_transform(
                                    prophet_attr_df_post[label])
    prophet_attr_df_pre[label] = scaler.inverse_transform(
                                    prophet_attr_df_pre[label])

    lower_bound_df = scaler.inverse_transform(lower_bound_df)
    upper_bound_df = scaler.inverse_transform(lower_bound_df)

    if label == "ix_bitrate":
        # factor for ix  dataset inverse transform
        mean = 5370.573816155988
        var = 337.82851880230834
        factor = 1000000000.0

        predicted_df = predicted_df * var
        print(predicted_df.min())
        predicted_df = predicted_df + mean
        predicted_df = predicted_df * factor

        prophet_attr_df_post[label] = prophet_attr_df_post[label] * var
        print(prophet_attr_df_post[label].min())
        prophet_attr_df_post[label] = prophet_attr_df_post[label] + mean
        prophet_attr_df_post[label] = prophet_attr_df_post[label] * factor

        prophet_attr_df_pre[label] = prophet_attr_df_pre[label] * var
        print(prophet_attr_df_pre[label].min())
        prophet_attr_df_pre[label] = prophet_attr_df_pre[label] + mean
        prophet_attr_df_pre[label] = prophet_attr_df_pre[label] * factor

        lower_bound_df = lower_bound_df * var
        lower_bound_df = lower_bound_df + mean
        lower_bound_df = lower_bound_df * factor

        print(lower_bound_df)

        upper_bound_df = upper_bound_df * var
        upper_bound_df = upper_bound_df + mean
        upper_bound_df = upper_bound_df * factor

    return predicted_df, prophet_attr_df_post,  prophet_attr_df_pre
# upper_bound_df, lower_bound_df


def compare_models(model_dict, dataframe, plotting=False):
    """compares the performance of given models using the
    provided dataframe by performing cross validation"""
    prophet_dataframes = LoadIn().load_all(typ='pre')
    ELM_dataframe = dataframe
    score_dict = dict()

    best_model_dict = {}
    for attr in dataframe:
        if attr == "Unnamed: 0":
            continue
        if attr == 'corona_deaths':
            break

        model_dict = load_models()
        ELM = model_dict["ELM"]
        prophet = model_dict["Prophet"]

        print("Attribute: ", attr)
        print("\n\n\n")
        attr_dict = {}

        # ELM
        ELM_dataframe.fillna(method='backfill', inplace=True)
        train, test = train_test_split(ELM_dataframe[attr], test_size=0.2)
        x_train_test, y_train_test = ELM.prepare_data(ELM_dataframe[attr])
        scores = cross_validate(ELM, x_train_test, y_train_test)
        attr_dict["ELM"] = sum(abs(scores['test_score']))/len(
            scores['test_score'])
        score_dict[attr] = attr_dict

        # PRophet
        prophet.load_best_param(attr)

        prophet_attr_df = prophet_dataframes[["Date", attr]]
        prophet_attr_df = prophet_attr_df.dropna()

        scores = cross_validate(estimator=prophet, X=prophet_attr_df['Date'],
                                y=prophet_attr_df[attr])
        attr_dict["Prophet"] = sum(abs(scores['test_score']))/len(
            scores['test_score'])

        if attr_dict["Prophet"] > attr_dict["ELM"]:
            best_model_dict[attr] = "Prophet"
        else:
            best_model_dict[attr] = "ELM"

        # plots
        if plotting is True:
            model_dict = load_models()
            ELM = model_dict["ELM"]
            prophet = model_dict["Prophet"]

            days_to_predict = 60
            TRAIN_WINDOW = 30
            elm = EM.ExtremeLearningMachine()

            loaded_data = dataframe
            train_size = len(loaded_data) - days_to_predict
            train_data = loaded_data[attr][:train_size]
            test_data = loaded_data[attr][train_size:]
            predictions = elm.predict_next_days(regu='no',
                                                train_win=TRAIN_WINDOW,
                                                do_plot=False,
                                                lambd=0.01,
                                                num_neurons=128,
                                                days=days_to_predict,
                                                data=train_data)

            x_values = range(len(loaded_data))
            plt.title('No name')
            plt.plot(x_values[:train_size], train_data, label='Train data')
            plt.plot(x_values[train_size:], predictions, label='Prediction')
            plt.plot(x_values[train_size:], test_data, label='Test data')
            plt.legend()
            plt.savefig("ELM predictions")

            prophet = pro.MyProphet()
            # prophet.load_best_param(attr)
            changepoint_prior_scale = np.arange(0.03, 0.2, 0.005)
            parameters = {'growth': ['linear', 'logistic'],
                          'changepoint_prior_scale': changepoint_prior_scale,
                          'interval_width': [0.8],
                          'seasonality_mode': ['additive', 'multiplicative']}
            loaded_param = prophet.gridsearchcv(parameters,
                                                dataframe=prophet_attr_df,
                                                safe=True)
            print(attr)
            print(loaded_param)
            prior_scale = loaded_param['changepoint_prior_scale']
            seasonality = loaded_param['seasonality_mode']
            interval_width_param = loaded_param['interval_width']
            growth_param = loaded_param['growth']
            prophet.set_model(prophet.set_model(growth=growth_param,
                              changepoint_prior_scale=prior_scale,
                              interval_width=interval_width_param,
                              seasonality_mode=seasonality))
            prophet.fit(prophet_attr_df['Date'], prophet_attr_df[attr])
            y_pred = prophet.predict(do_plot=True, label=attr)
            print(y_pred)

    return score_dict, best_model_dict


if __name__ == '__main__':
    a, b, c = get_predict_data("ix_bitrate")
