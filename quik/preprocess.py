import numpy as np
import pandas as pd
from sklearn import preprocessing as prep
from sklearn.preprocessing import MinMaxScaler
from collections import deque
from quik import prices 
import random


def classify(current,future,thres = 100): # Returns 0 when price less than before.   
    
    diff = (float(future) - float(current))
    if diff >= 0:
        if diff > thres:
            return 2
        else:
            return 1
    if diff < 0:
        if diff < -thres:
            return -2
        else:
            return -1

def classify_binary(current,future): # Returns 0 when price less than before. 
    if float(future) > float(current):
        return 1
    else:
        return 0

def preprocessing(df, SEQ_LEN = 500):
    
    df = df.reset_index()
    
	# Drop future values and targets
    df = df.drop("future",1)
    target = df["target"] # Assigning target to another pd.Series before droping
    df = df.drop("target",1)
    print('Dropping is done')
    
	# Data as a changes
    df = df + 1
    df = df.pct_change()
    print('Data as a changes')
    
	# Scale from 0 to 1
    min_max_scaler = MinMaxScaler()
    df = min_max_scaler.fit_transform(df)
    print('Scaled from 0 to 1')
    
	# Adding target to rescaled DataFrame 
    df = pd.DataFrame(df)
    df["target"] = target
    df = df.dropna()
    print("Added target to rescaled DataFrame")
    
	# Creating sequences 
    sequential_data = []

	#Filling list with sequential data
    for i in range(0,len(df)):
        if (i + SEQ_LEN) < len(df):
            print(i,i+SEQ_LEN)
            sequential_data.append([np.array(df.iloc[:,0:6][i:i+SEQ_LEN]), df["target"][i+SEQ_LEN-1:i+SEQ_LEN].values])
    print("Filled sequential data")

	#Data is shuffled
    random.shuffle(sequential_data)
    
	#Separating X and y
    X,y = [],[]  
    for seq, target in sequential_data:
    
        X.append(seq)
        y.append(target)
    print("All is done")
    

    return np.array(X), np.array(y)

def get_training_data(lag=500,size = None):

	df = prices.training_data(lag = lag)[:size] # Run function
	df['target'] = list(map(classify_binary, df['price_rts'], df['future']))

	return preprocessing(df) # Returns X and y




if __name__ == "__main__":
	X,y = get_training_data(lag = 500)

	print(X,y)






























