
import jwt,json,copy
import inspect
from struct import *
from datetime import datetime, timedelta

from sqlalchemy import desc,text
from app.csvparser.csv_parser import CsvParser
from app.config.models import Trx_Data,Parking
from app.config.models import SystemConfig,Garage

class SystemConfigParserService:
    """ every thing about parsing """
    _db =None

    """ the file which is used by parser to identify the file type and data"""
    _csv_file_names = None;
    def __init__(self, db):
        self._db = db
        self._csv_file_names = {'01': '00220%', '03': 'DPTI%'};  #start with 00220 or DPTI

    async def parse(self,location):
        """ parse the csv file into database, this will parse csv content and insert data into table::system_config,table::garage """
        parser = CsvParser(location)
        csvCollection=parser.read_files_in_directory()
        trx = []
        for key in csvCollection:
            if 'skip' in key:
                continue
            
            parsed = key.split('/')[-1].split('-')
            garage_code = parsed[0]
            csv_file_date = parsed[2].rstrip('.csv')
            d= csvCollection[key].split('\r\n')
            customer_id = self.check_customer_id(parsed[1])

            for dd in d:
                await self.save_system_config(dd,garage_code,csv_file_date)
                await self.save_garage(dd,customer_id)
                            
        return csvCollection

    def check_customer_id(self,company_name:str):
        """ we use file name to identify the customer_id ,note the customer_id must pre-insert into table::customer"""
        customer_id = 0
        if company_name == 'taiwan_parking':#聯通
            customer_id=1
        elif company_name == 'altob':#一卡通
            customer_id=2
        else:
            customer_id=0
        
        return customer_id

    async def save_garage(self,row:str,customer_id:int):
        """ parse data and save into garage """
        w = row.split(',')
        garage= self.convert_to_gargae_list(w,customer_id)
        if garage is not None:
            async with self._db.acquire() as conn:
                rr = await conn.execute(Garage.insert().values(garage))

    async def save_system_config(self,row:str,garage_code:str,csv_file_date:str):
        w = row.split(',')
        data= self.convert_to_system_config_list(w,garage_code,csv_file_date)
        async with self._db.acquire() as conn:
            if data is not None:
                rz =  await conn.execute(SystemConfig.insert().values(data))

    def convert_to_gargae_list(self,w:list,customer_id:int):
        k = []
        if len(w) < 2 or not w[0] or not w[1]:
            return None
        
        k.append(w[-1].lstrip().rstrip())
        k.append(w[0].lstrip('\ufeff').rstrip())
        k.append(1)
        return k

    def convert_to_system_config_list(self,w:list, garage_code:str, csv_file_date:str):
        if len(w) < 3:
            return None
        kk=w.copy()
        kk[3] = kk[3].lstrip('\ufeff')
        del kk[3]
        del kk[3]
        del kk[3]
        del kk[3]
        del kk[3]
        del kk[3]
        del kk[3]

        kk.append(csv_file_date)
        kk.append(garage_code)
        kk.append(1) #modified_account_id
        return kk