# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 00:21:36 2018

@author: Aleksandr
"""
import pandas as pd
import asyncio
import asyncpg

class db_connect:
    
    def __init__(self):
        
        
        self.DB_CONFIG = {
            'host': '127.0.0.1',
            'user': 'postgres',
            'password': '5004317',
            'port': 5433,
            'database': 'db_quik'
        }
        
        

    async def select(self,select):
        
        conn = await asyncpg.connect(**self.DB_CONFIG)
        
        row = await conn.fetch(select)
        
        return pd.DataFrame(row)




    
    def calling(self,selects):
        
        return asyncio.get_event_loop().run_until_complete(db_connect().select(selects))
    
















if __name__ == '__main__':
    
#    print(db_connect().select())
    #print(asyncio.get_event_loop().run_until_complete(db_connect().select()))
    
    print(db_connect().calling('''SELECT * FROM public.c_orders
                                  ORDER BY price DESC'''))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#==============================================================================
# #
# #    async def async_select(self):
# #        
# #        conn = await asyncpg.connect(**self.DB_CONFIG)
# #        
# #        row = await conn.fetch(
# #                
# #            '''SELECT * FROM public.current_options
# #    
# #               ORDER BY volume DESC ''')
# #        
# #        return pd.DataFrame(row)
# #    
# #    
# #    
#==============================================================================