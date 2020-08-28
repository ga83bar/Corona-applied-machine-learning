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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import extreme_learning as EM
import prophet as pro
import online_models as onl
import model_evaluation as eva
from load_in import LoadIn



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


def get_params(df):
    """
    performs grid search
    """
    

    # ELM 
    param_dict = {}
    lambdalst = []
    lambdalst = [0.001,0.005, 0.01,0.025, 0.05,0.075, 0.1, 0.25, 0.5, 0.75,1]
    neuronlst = [20,40,60,80,100,120,140,150]
    lmbd = 0
    neuron = 20
    """
    for i in range(1000):
        lambdalst.append(lmbd)
        lmbd += 0.001 
        """
    
    print(neuronlst)

    
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

        print(search.best_params_)

        break
    print(param_dict)
    return param_dict



def compare_models(model_dict, dataframe, plotting = False):
    """compares the performance of given models using the provided dataframe by performing cross validation"""
    prophet_dataframes = LoadIn().load_all(typ='pre')
    test_dataframes = LoadIn().load_all(typ='after')
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
        print(ELM_dataframe[attr])
        print(train)
        x_train_test, y_train_test = ELM.prepare_data(ELM_dataframe[attr])
        

        scores = cross_validate(ELM, x_train_test, y_train_test)
        attr_dict["ELM"] = sum(abs(scores['test_score']))/len(scores['test_score'])
        score_dict[attr] = attr_dict
        

        #PRophet
        prophet.load_best_param(attr)
        prophet_dataframes[attr].fillna(method='backfill', inplace=True)
        scores = cross_validate(estimator=prophet, X=prophet_dataframes['Date'], y=prophet_dataframes[attr])
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
            
            
            ELM.fit(x_train_test, y_train_test)
            y_pred = ELM.predict(x_train_test)
            mse = mean_squared_error(y_train_test, y_pred)

            prophet = pro.MyProphet()
            prophet.load_best_param(attr)
            prophet.fit(prophet_dataframes['Date'], prophet_dataframes[attr])
            y_pred = prophet.predict(do_plot=True, label=attr)
            print(y_pred)
            print(test_dataframes[attr])
            

            
            #mse = mean_squared_error(test_dataframes[attr].values, y_pred.values)
        

        
        
    return score_dict, best_model_dict



if __name__ == '__main__':
    PATH = Path().absolute().joinpath('GIT','group11','res', 'pipeline', 'scaled_pre_corona_df.csv')
    df = pd.read_csv(PATH)
    
    

    #param_lst = get_params(df)
    #print(param_lst)
    
    model_lst = load_models()
    score_lst, best_model_dict = compare_models(model_lst, df)
    print(best_model_dict)
  
    
    #print('The best model with 5-fold cross validation was {} with an MSE of {}'.format(best_model, least_mse))
    #plt.plot(df.index.values, df['stock_tech'])
