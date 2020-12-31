
import unittest,datetime,jwt,pathlib,yaml
from datetime import datetime,timezone, timedelta
from aiomysql.sa import create_engine
from app.services.user_service import UserService
from app.config.settings import SETTINGS
class UserServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.__stubKey=b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfX2ZpeGVkX2FjY291bnRfdG90YWwiOjEwLCJfX2R5bmFtaWNfYWNjb3VudF90b3RhbCI6MiwiX19rZXlfbWFuYWdlcl9lbWFpbCI6Inllbi5tcmtpZEBnbWFpbC5jb20iLCJfX3NlcnZpY2VfdHlwZSI6Imdsb2JhbCIsIl9fbm90ZSI6Im5vdGUgaGVyZSIsIl9fY3VzdG9tZXJfY29kZSI6IkExMjMiLCJfX2tleV90eXBlIjoidGVzdCIsImV4cCI6MTU0MTA4ODAwMH0.-rSjQfv-hlFNvQ6fF0xhPzCRU4FxWU7CKzBrgq13Rj0'
        self.__stubExpiredKey=b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfX2ZpeGVkX2FjY291bnRfdG90YWwiOjEwLCJfX2R5bmFtaWNfYWNjb3VudF90b3RhbCI6MiwiX19rZXlfbWFuYWdlcl9lbWFpbCI6Inllbi5tcmtpZEBnbWFpbC5jb20iLCJfX3NlcnZpY2VfdHlwZSI6Imdsb2JhbCIsIl9fbm90ZSI6Im5vdGUgaGVyZSIsIl9fY3VzdG9tZXJfY29kZSI6IkExMjMiLCJfX2tleV90eXBlIjoidGVzdCIsImV4cCI6MTUxMTk3MTIwMH0.rB0mCzwb0FqkCXVEoP5ZUAXJsXhakJf1zRDRDCmRKzM'
        app = []

        self.__db = create_engine(
            host=SETTINGS['mysql']['host'],
            port=int(SETTINGS['mysql']['port']),
            db=SETTINGS['mysql']['dbname'],
            user=SETTINGS['mysql']['username'],
            password=SETTINGS['mysql']['passwd'],
            autocommit=SETTINGS['mysql']['autocommit']
    )

    def test(self):
        s = UserService(self.__db)
        self.assertFalse(s.has_permission(1,1))

if __name__ == '__main__':
    unittest.main()