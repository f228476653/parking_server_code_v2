
import jwt,json,copy
import inspect
from struct import *
from datetime import datetime, timedelta

from sqlalchemy import desc,text
from app.csvparser.csv_parser import CsvParser
from app.config.models import Trx_Data,Parking
from app.config.models import Parking_In_Out_Record

class ParkingInOutRecordParserService:
    """ every thing about parsing """
    _db =None

    """ the file which is used by parser to identify the file type and data"""
    _csv_file_names = None;
    def __init__(self, db):
        self._db = db
    
    async def parse(self,location):

        parser = CsvParser(location,"parking_in_out_record")
        csvCollection=parser.read_files_in_directory()
        """ parse the csv file into database """
        trx = []
        for key in csvCollection:
            parsed = key.split('/')[-1].split('-')
            garage_code = parsed[0]
            csv_file_date = parsed[-1].rstrip('.csv')
            if 'pms.parking_in_out_record' in key:
                d= csvCollection[key].split('\n')
                for dd in d:
                    data= self.convertToList(dd,key,garage_code,csv_file_date)
                    async with self._db.acquire() as conn:
                        if data is not None:
                            rz =  await conn.execute(Parking_In_Out_Record.insert().values(data))
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