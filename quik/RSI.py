# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 21:51:19 2018

@author: Aleksandr
"""

import math
from option_data import option,moex_option_table
import numpy as np
import datetime
import py2database








class RVI_odl:
    
    def __init__(self):
        
        self.moex_opt_table = moex_option_table('RI').moex_option_table_load()
        print(self.moex_opt_table)
        self.T365 = 365/365                                     # 30 дней в долях от календарного года (год = 365 дней);
        self.T30 = 30/365                                       # 365 дней в долях от календарного года; 
        self.T1 = (float(self.moex_opt_table[4][1]))/365        # Время до даты экспирации ближайшей серии опционов включительно в долях от календарного года; 
        self.T2 = (float(self.moex_opt_table[4][2]))/365        # Время до даты экспирации следующей серии опционов включительно в долях от календарного года; 
        self.now = datetime.datetime.now()
        #self.sigma_1 = sigma_1                                  # Дисперсия ближайшей серии опционов; 
        #self.sigma_2 = sigma_2                                  # Дисперсия следующей серии опционов.
        
        
    def option_selection(self):
        
        self.obj = py2database.db_connect().calling(''' SELECT sec_name, strike, fee  FROM current_options
                                                        WHERE und_code LIKE '%RI%'
                                                        AND sec_name NOT LIKE '%A'
                                                        AND sec_name NOT LIKE '%B'
                                                        AND sec_name NOT LIKE '%C'
                                                        AND sec_name NOT LIKE '%D'
                                                        
                                                        AND expiry IN (SELECT DISTINCT expiry FROM (
                                                        	
                                                        				SELECT * FROM current_options
                                                        				WHERE und_code LIKE '%RI%'
                                                        				AND sec_name NOT LIKE '%A'
                                                        				AND sec_name NOT LIKE '%B'
                                                        				AND sec_name NOT LIKE '%C'
                                                        				AND sec_name NOT LIKE '%D') a
                                                        				ORDER BY expiry 
                                                        				fetch first 2 rows only)
                                                        				
                                                        AND strike > (SELECT last_price FROM dim_securities
                                                        				WHERE id LIKE 'RTS-%'
                                                        				ORDER BY volume DESC
                                                        				fetch first 1 rows only)
                                                        ORDER BY fee DESC, und_code, strike''')      
        
        
        
        
    def sigma_calc1(self):


        opt_table = self.moex_opt_table[2]
        print(opt_table)
        F = int(np.array(self.moex_opt_table[0]['Last Price']))
        dK = opt_table['Strike'][1] - opt_table['Strike'][0]        
        #==============================================================================
        K0 = np.array(opt_table['Strike']).flat[np.abs(np.array(opt_table['Strike']) - F).argmin()] 
        #==============================================================================     
        calls = opt_table.iloc[:,:5][['Strike','Calculated Price (CALL)']].sort_values(by=['Strike'])
        calls['Type'] = 'CALL'
        K0_index_call = calls[calls['Strike'] == K0].index.tolist()[0]
        K0_index = calls[calls['Strike'] == K0]
        calls = calls[K0_index_call-8:K0_index_call-1].values # 7 опционов Call «вне денег»; 
        #==============================================================================
        puts = opt_table.iloc[:,4:][['Strike','Calculated Price (PUT)']].sort_values(by=['Strike'])   
        puts['Type'] = 'PUT'
        K0_index_put = puts[puts['Strike'] == K0].index.tolist()[0]
        puts = puts[K0_index_put+1:K0_index_put+8].values # 7 опционов Put «вне денег»;
        
        
        array = np.vstack([puts,K0_index.values,calls])
        sigma1 = []        
                
        for x in range(0,len(array)):
            
            sigma1.append(((dK/ array[x][0]**2) * array[x][1]) - ((1/self.T1) * ((F/K0) - 1)**2))
            
        return (2/self.T1) * sum(sigma1)
        

    
    
    def sigma_calc2(self):
        
        opt_table = self.moex_opt_table[3] # Номер опционной серия        
        F = self.moex_opt_table[0]
        F = int(np.array(F['Last Price']))
        dK = opt_table['Strike'][1] - opt_table['Strike'][0]
        
        #==============================================================================
        K0 = np.array(opt_table['Strike']).flat[np.abs(np.array(opt_table['Strike']) - F).argmin()] 
        
        #==============================================================================
        calls = opt_table.iloc[:,:5][['Strike','Calculated Price (CALL)']].sort_values(by=['Strike'])
        calls['Type'] = 'CALL'
        K0_index_call = calls[calls['Strike'] == K0].index.tolist()[0]
        K0_index = calls[calls['Strike'] == K0]
        calls = calls[K0_index_call-8:K0_index_call-1].values # 7 опционов Call «вне денег»; 
     
        #==============================================================================
        puts = opt_table.iloc[:,4:][['Strike','Calculated Price (PUT)']].sort_values(by=['Strike'])   
        puts['Type'] = 'PUT'
        K0_index_put = puts[puts['Strike'] == K0].index.tolist()[0]
        puts = puts[K0_index_put+1:K0_index_put+8].values # 7 опционов Put «вне денег»;           
        
        array = np.vstack([puts,K0_index.values,calls])   

        sigma2 = []
        
        for x in range(0,len(array)):
            
            sigma2.append(((dK/ array[x][0]**2) * array[x][1]) - ((1/self.T2) * ((F/K0) - 1)**2))
    
        return (2/self.T2) * sum(sigma2)
    



    def RVI_calc(self,sigma1,sigma2):
        
        
        RVI = math.sqrt((self.T365 / self.T30) * math.fabs((self.T1 * sigma1 *((self.T2 - self.T30)/(self.T2 - self.T1)) + self.T2 * sigma2 * ((self.T30 - self.T1)/(self.T2 - self.T1)))))
        
        return RVI * 100
    
    
    
    
    
    
    
    
    

if __name__ == '__main__':
    
    
    RVI().option_selection()
#RSI = 100 * sqrt T365