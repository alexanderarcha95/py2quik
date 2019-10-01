# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 17:01:33 2018

@author: Aleksandr
"""

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
#          }
#==============================================================================


#==============================================================================
# «0» – транзакция отправлена серверу;
# «1» – транзакция получена на сервер QUIK от клиента;
# «2» – ошибка при передаче транзакции в торговую систему,поскольку отсутствует подключение шлюза Московской Биржи,повторно транзакция не отправляется;
# «3» – транзакция выполнена;
# «4» – транзакция не выполнена торговой системой, код ошибкиторговой системы будет указан в поле «DESCRIPTION»;
# «5» – транзакция не прошла проверку сервера QUIK по каким-либокритериям. Например, проверку на наличие прав у пользователя наотправку транзакции данного типа;
# «6» – транзакция не прошла проверку лимитов сервера QUIK;
# «10» – транзакция не поддерживается торговой системой.К примеру, попытка отправить «ACTION = MOVE_ORDERS»на Московской Бирже;
# «11» – транзакция не прошла проверку правильности электроннойподписи. К примеру, если ключи, зарегистрированные на сервере,не соответствуют подписи отправленной транзакции;
# «12» – не удалось дождаться ответа на транзакцию, т.к. истек таймаут ожидания. Может возникнуть при подаче транзакций из QPILE;
# «13» – транзакция отвергнута, т.к. ее выполнение могло привести кросс-сделке (т.е. сделке с тем же самым клиентским счетом);
# «14» – транзакция не прошла контроль дополнительных ограничений;
# «15» – транзакция принята после нарушения дополнительных ограничений;
# «16» – транзакция отменена пользователем в ходе проверки дополнительных ограничений
#==============================================================================



class trans2quik:
    
    def __init__(self,dll):      
#==============================================================================
#         Инициализация
#==============================================================================
        self.dll = dll        
        self.lpcstrConnectionParamsString = ctypes.create_string_buffer(b"C:\Open_Broker_QUIK_Junior")
        self.pnExtendedErrorCode = ctypes.byref(ctypes.c_long())
        self.lpstrErrorMessage = ctypes.c_char() #c_char_p
        self.dwErrorMessageSize = ctypes.c_long()
        
        '''Sending sync transactions'''
        
        self.pnReplyCode = ctypes.c_long()
        self.pdwTransId = ctypes.c_long() 
        self.pdOrderNum = ctypes.c_double()
        self.lpstrResultMessage = ctypes.c_char()
        self.dwResultMessageSize = ctypes.c_long(2)
            
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
                                                         
                                                         ctypes.pointer(self.pnReplyCode),
                                                         
                                                         ctypes.pointer(self.pdwTransId),
                                                         
                                                         ctypes.pointer(self.pdOrderNum),
                                                         
                                                         ctypes.pointer(self.lpstrResultMessage),
                                                         
                                                         self.dwResultMessageSize,
                                                         
                                                         ctypes.pointer(pnExtendedErrorCode),
                                                         
                                                         ctypes.pointer(lpstrErrorMessage),
                                                                     
                                                         self.dwErrorMessageSize)
        
        
        pdwTransId_value = ctypes.pointer(self.pdwTransId).contents.value
        pnReplyCode_value = ctypes.pointer(self.pnReplyCode).contents.value
        pdOrderNum_value = ctypes.pointer(self.pdOrderNum).contents.value
        lpstrResultMessage_value = list(ctypes.pointer(self.lpstrResultMessage).contents.value)
        dwResultMessageSize_value = ctypes.pointer(self.dwResultMessageSize).contents.value
        pnExtendedErrorCode_value = ctypes.pointer(pnExtendedErrorCode).contents.value                                                 
        lpstrErrorMessage_value = ctypes.pointer(lpstrErrorMessage).contents.value
        dwErrorMessageSize_value = ctypes.pointer(self.dwErrorMessageSize).contents.value

        
        df = pd.DataFrame({
                          'pdwTransId_value:': pdwTransId_value,
                          'pnReplyCode_value':pnReplyCode_value,
                          'pdOrderNum_value':pdOrderNum_value,
                          'lpstrResultMessage_value':lpstrResultMessage_value,
                          'dwResultMessageSize_value':dwResultMessageSize_value,
                          'pnExtendedErrorCode_value':pnExtendedErrorCode_value,
                          'lpstrErrorMessage_value':lpstrErrorMessage_value,
                          'dwErrorMessageSize_value':dwErrorMessageSize_value
                          })
        print(df.T)
        
        return sync


     
                    
    
    def TRANS2QUIK_SEND_ASYNC_TRANSACTION(self,lpstrTransactionString):
                
        pnExtendedErrorCode = ctypes.c_long()
        
        lpstrErrorMessage = ctypes.c_long()
        
        wasync = self.dll.TRANS2QUIK_SEND_ASYNC_TRANSACTION(lpstrTransactionString,
                                                          
                                                          ctypes.pointer(pnExtendedErrorCode),
                                                          
                                                          ctypes.pointer(lpstrErrorMessage),
                                                          
                                                          self.dwErrorMessageSize)



        pnExtendedErrorCode_value = ctypes.pointer(pnExtendedErrorCode).contents.value                                                 
        lpstrErrorMessage_value = ctypes.pointer(lpstrErrorMessage).contents.value
        dwErrorMessageSize_value = ctypes.pointer(self.dwErrorMessageSize).contents.value

        
        df = pd.DataFrame({
                          'pnExtendedErrorCode_value':[pnExtendedErrorCode_value],
                          'lpstrErrorMessage_value':lpstrErrorMessage_value,
                          'dwErrorMessageSize_value':dwErrorMessageSize_value
                          })
        
        print(df.T)

        

        
        return wasync
            
    
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

    
    transaction   = 'ACCOUNT=SPBFUTJRd11;TRANS_ID=934;CLASSCODE=SPBFUT;SECCODE=RIZ8;ACTION=KILL_ALL_STOP_ORDERS;'
    
    transaction_2 = 'ACTION=KILL_ALL_STOP_ORDERS; ACCOUNT= L01-00000F00; TRANS_ID=1; CLASSCODE=TQBR;'

    t3 = 'ACCOUNT= L01-00000F00; CLASSCODE=SBERCC;PRICE=100.00;CLIENT_CODE=52709;ACTION=NEW_ORDER;OPERATION=B;SECCODE=SBER;TRANS_ID=1;QUANTITY=1;'
    
    print('DISCONNECTED: ', dll.TRANS2QUIK_DISCONNECT())                   #0
    print('CONNECTED: ',dll.TRANS2QUIK_CONNECT())                          #0
    print('QUIK CONNECTED: ',dll.TRANS2QUIK_IS_QUIK_CONNECTED())           #8
    print('DLL CONNECTED: ',dll.TRANS2QUIK_IS_DLL_CONNECTED())  


           #10
    for x in range(3):
        
        transaction_3 = 'ACTION=NEW_STOP_ORDER; ACCOUNT= L01-00000F00; TRANS_ID=8; CLASSCODE=TQBR; SECCODE=SBER; OPERATION=B; QUANTITY=1; STOPPRICE=199.{0}0; PRICE=200;'.format(x)

        dll.TRANS2QUIK_SEND_SYNC_TRANSACTION(str.encode(transaction_2))
        
        
        
        
        
        
        
        
        
        
        
        