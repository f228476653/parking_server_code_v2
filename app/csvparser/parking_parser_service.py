
import jwt,json,copy
import inspect
from struct import *
from datetime import datetime, timedelta

from sqlalchemy import desc,text
from app.csvparser.csv_parser import CsvParser
from app.config.models import Trx_Data,Parking
from app.config.models import SystemConfig,Garage

class ParkingParserService:
    """ every thing about parsing """
    _db =None

    """ the file which is used by parser to identify the file type and data"""
    _csv_file_names = None;
    def __init__(self, db):
        self._db = db
        self._csv_file_names = {'01': '00220%', '03': 'DPTI%'};  #start with 00220 or DPTI

    async def parse(self,location):
        async with self._db.acquire() as conn: 
            trans =await conn.begin() 
            try: 
                parser = CsvParser(location,"parking")
                csvCollection=parser.read_files_in_directory()
                """ parse the csv file into database """
                trx = []
                for key in csvCollection:
                    parsed = key.split('/')[-1].split('-')
                    garage_code = parsed[0]
                    csv_file_date = parsed[-1].rstrip('.csv')
                    if 'pms.parking' in key:
                        d= csvCollection[key].split('\n')
                        for dd in d:
                            data= self.convertToList(dd,key,garage_code,csv_file_date)
                            if data is not None:
                                z = [dict(row.items()) async for row in await conn.execute(Parking.select().where(Parking.c.id==data[0]).where(Parking.c.garage_code==data[22]))]
                                if len(z) == 0:
                                    rz =  await conn.execute(Parking.insert().values(data))
                                else:
                                    rz =  await conn.execute(Parking.update().values(data).where(Parking.c.id==data[0]).where(Parking.c.garage_code==data[22]))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()
                parser.move_files_to_bakcup_directory()
        return csvCollection

    def convertToList(self,row:str, filename:str, garage_code:str, csv_file_date:str):
        k = []
        w= row.split(',')

        if len(w) < 3:
            return None

        w.append(filename)
        w.append(garage_code)
        w.append(csv_file_date)
        return w
