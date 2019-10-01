# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 22:15:24 2019

@author: Aleksandr
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from quik import prices
import pandas as pd
import numpy as np
import backtrader as bt
from datetime import datetime
import backtrader as bt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo





class SmaCross(bt.SignalStrategy):
	params = (('pfast', 50), ('pslow', 70  ),)
	def __init__(self):
		sma1, sma2 = bt.ind.SMA(period=self.p.pfast), bt.ind.SMA(period=self.p.pslow)
		self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma1, sma2))





# Create a data feed
df = prices.Tickers('M')
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)





if __name__ == "__main__":
    
    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    cerebro.run()

    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    cerebro.plot(b)


























































'''
# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=20,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position



cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
df = prices.Tickers('M')

df['datetime'] = pd.to_datetime(df['datetime'])
df.info()
df.set_index('datetime', inplace=True)
print(df)


data = bt.feeds.PandasData(dataname=df)
cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=15)

print(data)


cerebro.adddata(data)

# Run over everything
cerebro.run()

# Plot the result
#cerebro.plot()

cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(SmaCross ) # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot(style='candlestick',subplot=False) 


 # and plot it with a single command'''
 