import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from quik import py2database


cols = ['time','fut_name','close','amount','action','id','date','datetime']
cols_tickers = ['datetime','open','close','low','high','volume','openinterest']






def get_information(length = None, order = 'DESC'):
    
    
    if length == None:
        
        result = py2database.db_connect().calling('''SELECT dt_si,buy_si,sell_si,price_si,price_rts, coalesce(buy_rts,0) as buy_rts,coalesce(sell_rts,0) as sell_rts
                                                        from v_si_joined
                                                        INNER join v_rts_joined
                                                        on v_si_joined.dt_si = v_rts_joined.dt_rts
														ORDER BY dt_si {0}'''.format(order))
    else:  
        result = py2database.db_connect().calling('''SELECT dt_si,buy_si,sell_si,price_si,price_rts, coalesce(buy_rts,0) as buy_rts,coalesce(sell_rts,0) as sell_rts
                                                        from v_si_joined
                                                        INNER join v_rts_joined
                                                        on v_si_joined.dt_si = v_rts_joined.dt_rts
														ORDER BY dt_si  {0}
														FETCH FIRST {1} ROWS ONLY'''.format(order,length))
        
    result.columns = ['datetime','buy_si','sell_si','price_si','price_rts','buy_rts','sell_rts']
    
    
    return result









def training_data(lag,length = None):
    
    
    if length == None:
        
        result = py2database.db_connect().calling('''SELECT buy_si,sell_si,price_si,price_rts, coalesce(buy_rts,0),coalesce(sell_rts,0),
                                                        lag(price_rts, {0}) over (order by v_si_joined.dt_si) as new_value
                                                        from v_si_joined
                                                        left join v_rts_joined
                                                        on v_si_joined.dt_si = v_rts_joined.dt_rts
                                                        '''.format(lag))
      
    else:
        
        result = py2database.db_connect().calling('''SELECT buy_si,sell_si,price_si,price_rts, coalesce(buy_rts,0),coalesce(sell_rts,0),
                                                        lag(price_rts, {0}) over (order by v_si_joined.dt_si) as new_value
                                                        from v_si_joined
                                                        left join v_rts_joined
                                                        on v_si_joined.dt_si = v_rts_joined.dt_rts
                                                        FETCH FIRST {1} ROWS ONLY
                                                        '''.format(lag,length))
        
           
    result.columns = ['buy_si','sell_si','price_si','price_rts','buy_rts','sell_rts','future']
    
    
    result['future'].fillna(method='ffill', inplace=True)
    result['price_rts'].fillna(method='ffill', inplace=True)

    if lag != 0:
        
        result = result[lag:-lag]
    

    
    return result



def get_price_begin(length = None):
    
    
    if length == None:
        
        result = py2database.db_connect().calling('''SELECT * FROM v_orders''')
        
    else:
        
        result = py2database.db_connect().calling('''SELECT * FROM v_orders FETCH FIRST {0} ROWS ONLY'''.format(length))

        
    result.columns = cols
    
    return result


def get_price_end(length = None):
    
    
    if length == None: 
        
        result = py2database.db_connect().calling('''SELECT * FROM v_orders''')
        
    else:
        
        result = py2database.db_connect().calling('''SELECT * FROM (SELECT * FROM v_orders ORDER BY time DESC, id DESC LIMIT {0}) a ORDER BY time,id'''.format(length))
    
    result.columns = cols     
    
    return result




def returns(ts,plots=False):
    
    
    df = pd.DataFrame(ts)
    
    df['Log_Ret']  = np.log(df['Close'] / df['Close'].shift(6))
    
    if plots:
        
        df[['Close', 'Log_Ret']].plot(subplots=True,figsize=(15,8))
    
    return df['Log_Ret']

def volatilty(ts,plots=False):
    
    
    df = pd.DataFrame(ts)
    
    df['Log_Ret']  = np.log(df['Close'] / df['Close'].shift(1))
    
    df['Volatility'] = pd.rolling_std(df['Log_Ret'], window=252) * np.sqrt(252)
    
    if plots:
        
        df[['Close', 'Volatility']].plot(subplots=True,figsize=(15,8))
    
    return df['Volatility']

def Tickers(length = 'M'):
    
    if length == 'M': 
        
        result = py2database.db_connect().calling('''SELECT * FROM minutes''')
        
    if length == 'S':
        
        result = py2database.db_connect().calling('''SELECT * FROM minutes''')
    
    result.columns = cols_tickers
        
    return result




if __name__ == "__main__":
    
    
    df= training_data(100)
    
    #plt.plot(df['price'])
    
    print(df)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #print(returns(get_price_end(5000),plots=True))
    #plt.plot(Tickers('M')['close'])
    
    


    
    #plt.figure(figsize=(15,5))
    #plt.plot(Tickers('M')[])
    '''
    
SELECT * FROM (    select time+date,
 sum(case 
 	when action = 'Купля' then amount
	when action = 'Продажа' then amount * (-1)
 end) as balance,
 avg(price) as price
from c_orders where 
fut_name = 'Si-9.19 [FORTS]' AND 
date = (now()::date-1)
group by time+date
order by time+date) Si

FULL JOIN

    (select time+date,
 sum(case 
 	when action = 'Купля' then amount
	when action = 'Продажа' then amount * (-1)
 end) as balance,
 avg(price) as price
from c_orders where 
fut_name = 'BR-11.19 [FORTS]' AND 
date = (now()::date-1)
group by time+date
order by time+date) BR

ON Si.time+Si.date = BR.time+BR.date
    
    
    
    
    
    
    
    
    
    
    plt.figure(figsize=(15,5))
    plt.plot(get_price_begin()[2])
    
    plt.figure(figsize=(15,5))
    plt.plot( returns(get_price_begin()[2]))
    
    plt.figure(figsize=(15,5))
    plt.plot(volatilty(get_price_begin()[2]))'''