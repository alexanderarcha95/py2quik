# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 17:55:06 2018

@author: Aleksandr
"""
import ctypes
import os
import pandas as pd
#==============================================================================
# reply = {
#     "TRANS2QUIK_SUCCESS":0,
#     "TRANS2QUIK_FAILED":1,
#     "TRANS2QUIK_QUIK_TERMINAL_NOT_FOUND":2,
#     "TRANS2QUIK_DLL_VERSION_NOT_SUPPORTED":3,
#     "TRANS2QUIK_ALREADY_CONNECTED_TO_QUIK":4,
#     "TRANS2QUIK_WRONG_SYNTAX":5,
#     "TRANS2QUIK_QUIK_NOT_CONNECTED":6,
#     "TRANS2QUIK_DLL_NOT_CONNECTED":7,
#     "TRANS2QUIK_QUIK_CONNECTED":8,
#     "TRANS2QUIK_QUIK_DISCONNECTED":9,
#     "TRANS2QUIK_DLL_CONNECTED":10,
#     "TRANS2QUIK_DLL_DISCONNECTED":11,
#     "TRANS2QUIK_MEMORY_ALLOCATION_ERROR":12,
#     "TRANS2QUIK_WRONG_CONNECTION_HANDLE":13,
#     "TRANS2QUIK_WRONG_INPUT_PARAMS":14
# }
#==============================================================================


class trans2quik:
    
    def __init__(self,dll):      
#==============================================================================
#         Инициализация
#==============================================================================
        self.dll = dll        
        self.lpcstrConnectionParamsString = ctypes.create_string_buffer(b"C:\Open_Broker_QUIK_Junior")
        self.pnExtendedErrorCode = ctypes.byref(ctypes.c_long(10))
        self.lpstrErrorMessage = ctypes.c_char_p()
        self.dwErrorMessageSize = ctypes.c_long(10)
        
        '''Sending sync transactions'''
        
        self.pnReplyCode = ctypes.c_long()
        self.pdwTransId = ctypes.c_long() 
        self.pdOrderNum = ctypes.c_double()
        self.lpstrResultMessage = ctypes.c_char()
        self.dwResultMessageSize = ctypes.c_long(10)
        
        
        '''TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK'''
        self.nTransactionResult = ctypes.c_long()
        self.nTransactionExtendedErrorCode = ctypes.c_long()
        self.nTransactionReplyCode = ctypes.c_long()
        self.dwTransId = ctypes.c_long()
        #self.dOrderNum = ctypes.c_char_p()
        self.lpstrTransactionReplyMessage = ctypes.c_uint()
        self.transReplyDescriptor = ctypes.c_size_t()
        
        self.nConnectionEvent = ctypes.c_long()
        
        #self.lpstrClassCode
        #self.lpstrSeccodes
        
        
    def call_back(self):
        pass
        
        
        
             
        
    def TRANS2QUIK_CONNECT(self):
        
        return self.dll.TRANS2QUIK_CONNECT(self.lpcstrConnectionParamsString,
                                           
                                           self.pnExtendedErrorCode,
                                           
                                           self.lpstrErrorMessage,
                                           
                                           self.dwErrorMessageSize)
                            
        
    
    def TRANS2QUIK_DISCONNECT(self):
        
        return self.dll.TRANS2QUIK_DISCONNECT(self.pnExtendedErrorCode,
                                              
                                              self.lpstrErrorMessage,
                                              
                                              self.dwErrorMessageSize)
                                

    
    
    def TRANS2QUIK_IS_QUIK_CONNECTED(self):
           
         return self.dll.TRANS2QUIK_IS_QUIK_CONNECTED(self.pnExtendedErrorCode,
                                                      
                                                      self.lpstrErrorMessage,
                                                      
                                                      self.dwErrorMessageSize)
    
    
    def TRANS2QUIK_IS_DLL_CONNECTED(self):
        
        return self.dll.TRANS2QUIK_IS_DLL_CONNECTED(self.pnExtendedErrorCode,
                                                    
                                                    self.lpstrErrorMessage,
                                                    
                                                    self.dwErrorMessageSize)
        
        



        
    def TRANS2QUIK_SEND_SYNC_TRANSACTION(self,lpstrTransactionString):
        
        pnExtendedErrorCode = ctypes.c_long()
        
        lpstrErrorMessage = ctypes.c_long()
        
        sync = self.dll.TRANS2QUIK_SEND_SYNC_TRANSACTION(lpstrTransactionString,
                                                         
                                                         ctypes.byref(self.pnReplyCode),
                                                         
                                                         ctypes.byref(self.pdwTransId),
                                                         
                                                         ctypes.byref(self.pdOrderNum),
                                                         
                                                         ctypes.byref(self.lpstrResultMessage),
                                                         
                                                         self.dwResultMessageSize,
                                                         
                                                         ctypes.byref(pnExtendedErrorCode),
                                                         
                                                         ctypes.byref(self.lpstrErrorMessage),
                                                                     
                                                         self.dwErrorMessageSize)
        
        
        pdwTransId_value = ctypes.pointer(self.pdwTransId).contents.value
        pnReplyCode_value = ctypes.pointer(self.pnReplyCode).contents.value
        pdOrderNum_value = ctypes.pointer(self.pdOrderNum).contents.value
        lpstrResultMessage_value = list(ctypes.pointer(self.lpstrResultMessage).contents.value)
        dwResultMessageSize_value = ctypes.pointer(self.dwResultMessageSize).contents.value
        pnExtendedErrorCode_value = ctypes.pointer(pnExtendedErrorCode).contents.value                                                 
        lpstrErrorMessage_value = ctypes.pointer(lpstrErrorMessage).contents.value
        dwErrorMessageSize_value = ctypes.pointer(self.dwErrorMessageSize).contents.value

        
        print(pd.DataFrame({
              'pdwTransId_value:': pdwTransId_value,
              'pnReplyCode_value':pnReplyCode_value,
              'pdOrderNum_value':pdOrderNum_value,
              'lpstrResultMessage_value':lpstrResultMessage_value,
              'dwResultMessageSize_value':dwResultMessageSize_value,
              'pnExtendedErrorCode_value':pnExtendedErrorCode_value,
              'lpstrErrorMessage_value':lpstrErrorMessage_value,
              'dwErrorMessageSize_value':dwErrorMessageSize_value
              }))
        
        return sync
        
                    
    
    def TRANS2QUIK_SEND_ASYNC_TRANSACTION(self,lpstrTransactionString):
        
        return self.dll.TRANS2QUIK_SEND_ASYNC_TRANSACTION(lpstrTransactionString,
                                                          
                                                          self.pnExtendedErrorCode,
                                                          
                                                          ctypes.byref(self.lpstrErrorMessage),
                                                          
                                                          self.dwErrorMessageSize)
            
    
    def TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK(self):
                
        return self.dll.TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK(self.nTransactionResult,
                                                               
                                                               self.nTransactionExtendedErrorCode,
                                                               
                                                               self.nTransactionReplyCode,
                                                               
                                                               self.dwTransId,
                                                               
                                                               self.dOrderNum,
                                                               
                                                               self.lpstrTransactionReplyMessage,
                                                               
                                                               self.transReplyDescriptor)
            
          
    def TRANS2QUIK_CONNECTION_STATUS_CALLBACK(self):
                
        return self.dll.TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK(self.nConnectionEvent,
                                                               
                                                               self.pnExtendedErrorCode,
                                                               
                                                               self.lpstrErrorMessage)
        
        
    def TRANS2QUIK_SUBSCRIBE_TRADES(self):
                
        return self.dll.TRANS2QUIK_SUBSCRIBE_TRADES(self.nConnectionEvent,
                                                               self.pnExtendedErrorCode,
                                                               
                                                               self.lpstrErrorMessage)

def main():
    
    pass




if __name__ == '__main__':
    pass
        
     
     
    dll = trans2quik(ctypes.cdll.LoadLibrary(os.path.abspath('C://Open_Broker_QUIK_Junior//trans2quik.dll')))

    
    transaction =b'ACCOUNT=SPBFUTJRd11;TRANS_ID=9134;CLASSCODE=SPBFUT;SECCODE=RIZ8;ACTION=KILL_ALL_STOP_ORDERS;'

    print(dll.TRANS2QUIK_DISCONNECT())                  #0
    print(dll.TRANS2QUIK_CONNECT())                     #0
    print(dll.TRANS2QUIK_IS_QUIK_CONNECTED())           #8
    print(dll.TRANS2QUIK_IS_DLL_CONNECTED())            #10
    print(dll.TRANS2QUIK_SEND_SYNC_TRANSACTION(transaction))
    
    #print(dll.TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK())
    #print(dll.TRANS2QUIK_CONNECTION_STATUS_CALLBACK())
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
ACTION=NEW_STOP_ORDER; ACCOUNT= SPBFUTJRd11; TRANS_ID=1321141;CLASSCODE=SPBFUT; SECCODE=HYDR; OPERATION=S; QUANTITY=100;CLIENT_CODE=467; STOPPRICE=7.3; PRICE=7.0; EXPIRY_DATE=20110519;

    tr ='ACCOUNT=SPBFUTJRd11; TRANS_ID=1; CLASSCODE=SPBFUT; SECCODE=RIZ8; ACTION=NEW_STOP_ORDER; OPERATION=B; PRICE=100940; QUANTITY=1;STOPPRICE=110940;'
'''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    print(dll.TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK(transaction,nTransactionResult = ctypes.c_long(100),
#                                                        nTransactionExtendedErrorCode = ctypes.c_long(100),
#                                                        nTransactionReplyCode = ctypes.c_long(100),
#                                                        dwTransId = ctypes.c_long(100),
#                                                        dOrderNum = ctypes.c_char_p(),
#                                                        lpstrTransactionReplyMessage = ctypes.c_uint(),
#                                                        transReplyDescriptor = ctypes.c_size_t(10)))
    
    #print(dll.TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK())

    #print(dll.TRANS2QUIK_CONNECTION_STATUS_CALLBACK(ctypes.c_long(100)))
    
    
    

























#TRANS2QUIK_CONNECTION_STATUS_

#c = trans2quik(ctypes.cdll.LoadLibrary(os.path.abspath('C://Open_Broker_QUIK_Junior//trans2quik.dll')))
#TRANS2QUIK_CONNECTION_STATUS_CALLBACK 
 
#TRANS2QUIK_SUBSCRIBE_TRADES







#
#
#print(dll.TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK(nTransactionResult = ctypes.c_long(100),
#                                                        nTransactionExtendedErrorCode = ctypes.c_long(100),
#                                                        nTransactionReplyCode = ctypes.c_long(100),
#                                                        dwTransId = ctypes.c_long(100),
#                                                        dOrderNum = ctypes.c_char_p(),
#                                                        lpstrTransactionReplyMessage = ctypes.c_uint(),
#                                                        transReplyDescriptor = ctypes.c_size_t(10)))
#     
#     #TRANS2QUIK_TRANSACTIONS_REPLY_CALLBACK 
    
    

    
    
     



















#    TransStr =" ACCOUNT=SPBFUTJReAY; TYPE=L; TRANS_ID=1; CLASSCODE=SPBFUT; SECCODE=SiU8; ACTION=NEW_ORDER; OPERATION=B; PRICE=67300; QUANTITY=1;"
#    trans = trans2quik(ctypes.cdll.LoadLibrary("C:/Open_Broker_QUIK_Junior/trans2quik.dll"),
#            ctypes.create_string_buffer(b'C:/Open_Broker_QUIK_Junior'),
#            ctypes.c_long(),
#            ctypes.c_char(),
#            ctypes.c_long(),TransStr)
#    
#    
    
    
    


    

    #print(trans.send_async_trans())
