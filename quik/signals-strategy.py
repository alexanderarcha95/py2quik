# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 22:07:38 2019

@author: Aleksandr
"""
from quik import prices
import pandas as pd
import numpy as np
import backtrader as bt
from datetime import datetime
import hurst
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk

series = np.array(prices.get_price_end()['close'])# create a random walk from random changes
#series = prices.Tickers('M')['cLose']
plt.plot(series)

# Evaluate Hurst equation
H, c, data = compute_Hc(series, kind='price', simplified=True)

# Plot
f, ax = plt.subplots()
ax.plot(data[0], c*data[0]**H, color="deepskyblue")
ax.scatter(data[0], data[1], color="purple")
ax.set_xscale('log') 
ax.set_yscale('log')
ax.set_xlabel('Time interval')
ax.set_ylabel('R/S ratio')
ax.grid(True)
plt.show()

print("H={:.4f}, c={:.4f}".format(H,c))
