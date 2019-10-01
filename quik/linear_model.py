# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:26:14 2019

@author: Aleksandr
"""
from quik import prices
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk
from sklearn.linear_model import LinearRegression,BayesianRidge,LogisticRegression   
from sklearn.model_selection import train_test_split 
from sklearn import metrics



def lin_model(size = 20000,shift = 10,is_plot = True):
    
    
    X = np.array(prices.get_price_end(size)['close'])[:-shift].reshape(-1,1)
    
    y = np.array(prices.get_price_end(size)['close'])[shift:].reshape(-1,1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0,shuffle=False)
    print('X',pd.DataFrame(X),'y',pd.DataFrame(y))
    regressor = LogisticRegression() 
    
    regressor.fit(X_train, y_train) #training the algorithm    
    #To retrieve the intercept:
    y_pred = regressor.predict(X_test)
    
    if is_plot == True:
        
        plt.scatter(X_test, y_test,  color='gray')
        plt.plot(X_test, y_pred, color='red', linewidth=3)
        plt.show()
        
        print(regressor.intercept_)
    #For retrieving the slope:
        print(regressor.coef_)
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
        
        plt.plot(y_pred,color='red',linewidth=1.2)
        plt.plot(y_test,color='gray')
        
        
        
    return y_pred



def lin_model_run(size = 87060,shift = 2,is_plot = False):
    
    X = np.array(prices.v_orders_first_data_test(size-shift)).reshape(-1,1)
    
    y = np.array(prices.v_orders_first_data_test(size))[shift:].reshape(-1,1)
    #print('X',pd.DataFrame(X),'y',pd.DataFrame(y))
    data = np.array(prices.v_orders_second_data_test(500)).reshape(-1,1)
    
    
    regressor = LinearRegression()  
    regressor.fit(X, y) #training the algorithm    

    y_pred = regressor.predict(data)
    
    return y_pred

if __name__ == "__main__":
    
    lin_model()
    
    #plt.plot(prices.v_orders_second_data_test(500))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    