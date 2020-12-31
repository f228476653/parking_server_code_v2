
import jwt,json,copy
import inspect
from struct import *
from datetime import datetime, timedelta

from sqlalchemy import desc,text
from app.csvparser.csv_parser import CsvParser
from app.config.models import Trx_Data,Parking
from app.config.models import Lane,Garage
from sqlalchemy.sql import select

class LaneParserService:
    """ every thing about parsing """
    _db =None

    """ the file which is used by parser to identify the file type and data"""
    _csv_file_names = None;
    def __init__(self, db):
        self._db = db

    async def parse(self,location):
        async with self._db.acquire() as conn: 
            trans =await conn.begin() 
            try: 
                parser = CsvParser(location,"lane")
                csvCollection=parser.read_files_in_directory()
                """ parse the csv file into database """
                trx = []
                for key in csvCollection:
                    parsed = key.split('/')[-1].split('-')
                    garage_code = parsed[0]
                    csv_file_date = parsed[-1].rstrip('.csv')
                    if 'pms.lane' in key:
                        d= csvCollection[key].split('\n')
                        for dd in d:
                            data = await self.convertToList(dd,key,garage_code,csv_file_date)
                            if data is not None:
                                rz =  await conn.execute(Lane.insert().values(data))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()
                parser.move_files_to_bakcup_directory()
        return csvCollection

    async def convertToList(self,row:str, filename:str, garage_code:str, csv_file_date:str):
        k = []
        w= row.split(',')

        if len(w) < 3:
            return None
        async with self._db.acquire() as conn:
            g = await conn.execute(select([Garage.c.garage_id]).where(Garage.c.garage_code == garage_code))
            garage_id = await g.scalar()
        w.append(filename)
        w.append(garage_code)
        w.append(csv_file_date)
        w.append(garage_id)
        return w
