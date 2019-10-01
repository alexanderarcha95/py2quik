# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 18:26:03 2018

@author: Aleksandr
"""

import math
#from option_data import option,moex_option_table
import numpy as np
import datetime
import py2database



class RVI:
    
    def __init__(self):
        
        self.obj_First = py2database.db_connect().calling('''SELECT * FROM v_rvi_desk_first''')
        
        self.obj_Second = py2database.db_connect().calling('''SELECT * FROM v_rvi_desk_second''')#.format(str(self.option_selected[1]).encode('utf-8')))
                                                        
        self.T365 = 365/365                                     # 30 дней в долях от календарного года (год = 365 дней);

        self.T30 = 30/365                                       # 365 дней в долях от календарного года; 

        self.T1 = float(py2database.db_connect().calling('''SELECT DISTINCT (expiry - current_date)::float /365 FROM v_rvi_desk_first''').values) #min(set(np.array(self.obj_First[11])))/365    # Время до даты экспирации ближайшей серии опционов включительно в долях от календарного года; 
                
        self.T2 = float(py2database.db_connect().calling('''SELECT DISTINCT (expiry - current_date)::float /365 FROM v_rvi_desk_second''').values) #max(set(np.array(self.obj_Second[11])))/365   # Время до даты экспирации следующей серии опционов включительно в долях от календарного года; 

        self.now = datetime.datetime.now()

        self.und_asset_first = str(np.array(self.obj_First[[11,0]].sort_values(by=[11])[:1:][0]))[2:11]   # Базовый актив для ближайшей серии опционов 

        self.und_asset_second = str(np.array(self.obj_Second[[11,0]].sort_values(by=[11])[-1::][0]))[2:11] # Базовый актив для следующей серии опционов

        self.F_first  = float(py2database.db_connect().calling('''SELECT last_price FROM dim_securities
                                                           WHERE id LIKE '{0}%' '''.format(self.und_asset_first)).values)
        self.F_second = float(py2database.db_connect().calling('''SELECT last_price FROM dim_securities
                                                           WHERE id LIKE '{0}%' '''.format(self.und_asset_second)).values)

        self.dK = float(self.obj_Second[4][1:2]) - float(self.obj_Second[4][:1])
        if float(self.obj_Second[4][1:2]) - float(self.obj_Second[4][:1]) != float(self.obj_First[4][1:2]) - float(self.obj_First[4][:1]):
            raise ValueError('Дельта различается.')
        

            




    def sigma_First(self):
        
        # Номер опционной серии 1
        dK = self.dK
        F = self.F_first
        K0 = np.array(self.obj_First[4]).flat[np.abs(np.array(self.obj_First[4]) - F).argmin()]
        array = np.matrix(self.obj_First[[4,16]])
        sigma1_arr = []
        
        for x in range(len(array)):
            
            sigma1_arr.append((2/self.T1)*((dK/ array[x,0]**2) * array[x,1]) - ((1/self.T1) * ((F/K0) - 1)**2))
 
        return sum(sigma1_arr)
    
    
    
    
    def sigma_Second(self):
        
        # Номер опционной серии 2
        dK = self.dK
        F = self.F_second
        K0 = np.array(self.obj_Second[4]).flat[np.abs(np.array(self.obj_Second[4]) - F).argmin()]
        array = np.matrix(self.obj_Second[[4,16]])
        sigma2_arr = []
        
        for x in range(len(array)):
           
            sigma2_arr.append((2/self.T2)*((dK/ array[x,0]**2) * array[x,1]) - ((1/self.T2) * ((F/K0) - 1)**2))

        return sum(sigma2_arr)
    
    
    
                                               
    def RVI_calc(self,sigma1,sigma2):
        
        RVI = math.sqrt((self.T365 / self.T30) * math.fabs((self.T1 * sigma1 * ((self.T2 - self.T30)/(self.T2 - self.T1)) + self.T2 * sigma2 * ((self.T30 - self.T1)/(self.T2 - self.T1)))))
        
        return RVI * 100
    

if __name__ == "__main__":
    
    RVI = RVI()
    sigma1 = RVI.sigma_First()
    sigma2 = RVI.sigma_Second()
    print(sigma1,sigma2)
    print(RVI.RVI_calc(sigma1,sigma2))
    
    