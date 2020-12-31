
import unittest,datetime,jwt
from datetime import datetime,timezone, timedelta
from keystore.keystore_manager import KeystoreManager
from keystore.keystore_status_enum import KeystoreStatusEnum

class KeystoreManagerTest(unittest.TestCase):

    
    def setUp(self):
        self.__stubKey=b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfX2ZpeGVkX2FjY291bnRfdG90YWwiOjEwLCJfX2R5bmFtaWNfYWNjb3VudF90b3RhbCI6MiwiX19rZXlfbWFuYWdlcl9lbWFpbCI6Inllbi5tcmtpZEBnbWFpbC5jb20iLCJfX3NlcnZpY2VfdHlwZSI6Imdsb2JhbCIsIl9fbm90ZSI6Im5vdGUgaGVyZSIsIl9fY3VzdG9tZXJfY29kZSI6IkExMjMiLCJfX2tleV90eXBlIjoidGVzdCIsImV4cCI6MTU0MTA4ODAwMH0.-rSjQfv-hlFNvQ6fF0xhPzCRU4FxWU7CKzBrgq13Rj0'
        self.__stubExpiredKey=b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfX2ZpeGVkX2FjY291bnRfdG90YWwiOjEwLCJfX2R5bmFtaWNfYWNjb3VudF90b3RhbCI6MiwiX19rZXlfbWFuYWdlcl9lbWFpbCI6Inllbi5tcmtpZEBnbWFpbC5jb20iLCJfX3NlcnZpY2VfdHlwZSI6Imdsb2JhbCIsIl9fbm90ZSI6Im5vdGUgaGVyZSIsIl9fY3VzdG9tZXJfY29kZSI6IkExMjMiLCJfX2tleV90eXBlIjoidGVzdCIsImV4cCI6MTUxMTk3MTIwMH0.rB0mCzwb0FqkCXVEoP5ZUAXJsXhakJf1zRDRDCmRKzM'
        
    def getTestKeyManager(self):
        """ generate default test keymanger instance"""
        fixed_account_total = 10
        dynamic_account_total = 2
        key_manager_email = "yen.mrkid@gmail.com"
        service_type = "global"
        start_edate = '2017-11-01T16:00:00.000Z'
        end_date = '2018-11-01T16:00:00.000Z'
        note ="note here"
        customer_id = 1
        key_type = "test"
        key_manager = KeystoreManager(
            start_edate
            , end_date
            , fixed_account_total
            , dynamic_account_total
            , key_manager_email
            , service_type
            , note
            , customer_id
            , key_type
        )
        return key_manager

    def getTestKeyManagerExpired(self):
        """ generate default test keymanger instance"""
        fixed_account_total = 10
        dynamic_account_total = 2
        key_manager_email = "yen.mrkid@gmail.com"
        service_type = "global"
        start_date = '2016-11-01T16:00:00.000Z'
        end_date = '2017-11-29T16:00:00.000Z'
        note ="note here"
        customer_id = 1
        key_type = "test"
        key_manager = KeystoreManager(
            start_date
            , end_date
            , fixed_account_total
            , dynamic_account_total
            , key_manager_email
            , service_type
            , note
            , customer_id
            , key_type
        )
        return key_manager
   
    def test_encrypt(self):
        keyManager = self.getTestKeyManager()
        result= keyManager.encrypt()

        self.assertNotEqual(result,'1'+ str(self.__stubKey))
        self.assertEqual(result,self.__stubKey)

    def test_decrypt(self):
        keyManager = self.getTestKeyManager()
        result = keyManager.decrypt(self.__stubKey)
        self.assertEqual(result['__key_manager_email'],"yen.mrkid@gmail.com")
    
    def test_encrypt_expired(self):
        keyManager = self.getTestKeyManagerExpired()
        result = keyManager.encrypt()
        self.assertEqual(result,self.__stubExpiredKey)
    
    def test_verify(self):
        keyManager = self.getTestKeyManagerExpired()
        result = keyManager.encrypt()
        self.assertEqual(KeystoreStatusEnum.EXPIRED,  keyManager.verify(result))
        self.assertEqual(KeystoreStatusEnum.INVALID,  keyManager.verify("1"+str(result)))

        keyManager = self.getTestKeyManager()
        result = keyManager.encrypt()
        self.assertEqual(KeystoreStatusEnum.VALID,  keyManager.verify(result))
    
    def test_decrypt_expired(self):
        keyManager = self.getTestKeyManagerExpired()
        self.assertRaises(jwt.ExpiredSignatureError, lambda : keyManager.decrypt(self.__stubExpiredKey))
        self.assertRaises(jwt.DecodeError, lambda : keyManager.decrypt('1'+str(self.__stubExpiredKey)))

if __name__ == '__main__':
    unittest.main()