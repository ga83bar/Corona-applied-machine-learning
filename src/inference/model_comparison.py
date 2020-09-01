"""
Compares the performance of simple regression models on a common dataset using cross-validation.
Performance is judged based on the MSE of each model.
"""
# from fbprophet import Prophet
from pathlib import Path, PurePath

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

import extreme_learning as EM
import prophet as pro
import online_models as onl
import model_evaluation as eva
from load_in import LoadIn
import joblib






def get_model_list():
    """returns a list containing available regressors for model comparison"""
    model_list = [('DecisionTree', DecisionTreeRegressor()), ('NeuralNetwork', MLPRegressor(shuffle=False)),
                  ('LinearModel', LinearRegression()), ('PolyLinearModel', LinearRegression())]  
    return model_list


def load_models():
    ELM = EM.ExtremeLearningMachine()
    Prophet = pro.MyProphet()
    #online = onl.OnlineDense()
    model_dict = {"ELM": ELM, "Prophet": Prophet}
    return model_dict


def get_params(df, ELM= False):
    """
    performs grid search
    {'growth': 'linear', 'changepoint_prior_scale': 0.10499999999999995, 'interval_width': 0.8, 'seasonality_mode': 'additive', 'metric': 0.0011843675774291197}
    """
    param_dict ={}
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
        #prophet.load_best_param(attr)
        changepoint_prior_scale = np.arange(0.03, 0.2, 0.005)
        parameters = {'growth': ['linear', 'logistic'],
                'changepoint_prior_scale': changepoint_prior_scale,
                'interval_width': [0.8],
                'seasonality_mode': ['additive', 'multiplicative']}
        best_params = prophet.gridsearchcv(parameters, dataframe =  prophet_attr_df_pre, safe=True )
        param_dict[label] = best_params
        print(best_params)
        print(param_dict)
    print(param_dict)
    
    if ELM == True:
        # ELM 
        param_dict = {}
        lambdalst = []
        lambdalst = [0.001,0.005, 0.01,0.025, 0.05,0.075, 0.1, 0.25, 0.5, 0.75,1]
        neuronlst = [20,40,60,80,100,120,140,150]
        lmbd = 0
        neuron = 20
        
        for attribute in df:
            if attribute == "Unnamed: 0":
                continue
            if attribute == 'corona_deaths':
                break
            print(attribute)
            ELM_param_grid = {'neurons':neuronlst,
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
    predicted_df = prophet.predict(do_plot=False, label=label)

    scaler_path = f"GIT/group11/res/pipeline/scaler_{label}.save"
    ix_mean_var_path = "GIT/group11/res/pipeline/ix_mean_var.csv"

    scaler = joblib.load(scaler_path)
    print(scaler)
    print(predicted_df)
    predicted_df = scaler.inverse_transform(predicted_df)
    prophet_attr_df_post[label] = scaler.inverse_transform(prophet_attr_df_post[label])
    prophet_attr_df_pre[label] = scaler.inverse_transform(prophet_attr_df_pre[label])

    print(predicted_df)
    
    if label == "ix_bitrate":
        print("a")
        
        mean = 976.122858594206
        var = 16558.93738199964
        factor = 1000000000.0

        predicted_df = predicted_df * var
        predicted_df =predicted_df * mean
        predicted_df = predicted_df * factor
        
        prophet_attr_df_post[label] = prophet_attr_df_post[label] *var
        prophet_attr_df_post[label] = prophet_attr_df_pre[label] *var
        prophet_attr_df_post[label] = prophet_attr_df_post[label] * factor

        prophet_attr_df_post[label] = prophet_attr_df_post[label] *mean
        prophet_attr_df_pre[label] = prophet_attr_df_pre[label] *mean
        prophet_attr_df_pre[label] = prophet_attr_df_pre[label] *factor


    print(predicted_df)
    return predicted_df, prophet_attr_df_post,  prophet_attr_df_pre

def compare_models(model_dict, dataframe, plotting = True):
    """compares the performance of given models using the provided dataframe by performing cross validation"""
    prophet_dataframes = LoadIn().load_all(typ='pre')
    ELM_dataframe = dataframe
    score_dict = dict()
    data_table = np.array(df.index.values.reshape(-1, 1))
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
        attr_dict={}
        
        #ELM
        
        ELM_dataframe.fillna(method='backfill', inplace=True)
        train, test = train_test_split(ELM_dataframe[attr], test_size=0.2)
        
        x_train_test, y_train_test = ELM.prepare_data(ELM_dataframe[attr])
        scores = cross_validate(ELM, x_train_test, y_train_test)
        attr_dict["ELM"] = sum(abs(scores['test_score']))/len(scores['test_score'])
        score_dict[attr] = attr_dict
        
        
        #PRophet
        prophet.load_best_param(attr)
        
        prophet_attr_df = prophet_dataframes[["Date", attr]]
        prophet_attr_df = prophet_attr_df.dropna()
        
        
        scores = cross_validate(estimator=prophet, X=prophet_attr_df['Date'], y=prophet_attr_df[attr])
        attr_dict["Prophet"] = sum(abs(scores['test_score']))/len(scores['test_score'])
        
        if attr_dict["Prophet"] > attr_dict["ELM"]:
            best_model_dict[attr] = "Prophet"
        else:
            best_model_dict[attr] = "ELM"
        
        #plots 
        if plotting == True:
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
            predictions = elm.predict_next_days(regu='no', train_win=TRAIN_WINDOW, do_plot=False,
                                                lambd=0.01, num_neurons=128, days=days_to_predict,
                                                data=train_data)
            
            x_values = range(len(loaded_data))
            plt.title('No name')
            plt.plot(x_values[:train_size], train_data, label='Train data')
            plt.plot(x_values[train_size:], predictions, label='Prediction')
            plt.plot(x_values[train_size:], test_data, label='Test data')
            plt.legend()
            plt.savefig("ELM predictions")
            
            
            """
            prophet = pro.MyProphet()
            #prophet.load_best_param(attr)
            changepoint_prior_scale = np.arange(0.03, 0.2, 0.005)
            parameters = {'growth': ['linear', 'logistic'],
                  'changepoint_prior_scale': changepoint_prior_scale,
                  'interval_width': [0.8],
                  'seasonality_mode': ['additive', 'multiplicative']}
            loaded_param = prophet.gridsearchcv(parameters, dataframe = prophet_attr_df, safe=True )
            print(attr)
            print(loaded_param)
            prophet.set_model( self.set_model(growth=loaded_param['growth'], changepoint_prior_scale=loaded_param['changepoint_prior_scale'],
                       interval_width=loaded_param['interval_width'], seasonality_mode=loaded_param['seasonality_mode']))
            prophet.fit(prophet_attr_df['Date'], prophet_attr_df[attr])
            y_pred = prophet.predict(do_plot=True, label=attr)
            print(y_pred)
            """
            

            
            #mse = mean_squared_error(test_dataframes[attr].values, y_pred.values)
        

        
        
    return score_dict, best_model_dict



if __name__ == '__main__':
    #PATH = Path().absolute().joinpath('GIT','group11','res', 'pipeline', 'scaled_pre_corona_df.csv')
    #df = pd.read_csv(PATH)
    #start_time = time.time()
    #get_params(df)
    #length = time.time()-start_time
    #print(length)
    #print(param_lst)
    
    """model_lst = load_models()
    score_lst, best_model_dict = compare_models(model_lst, df)
    print(best_model_dict)"""
    get_predict_data("twitch_streams")
  
    
  
