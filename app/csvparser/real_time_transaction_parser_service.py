import jwt, json, math ,re
import inspect
from struct import *
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import desc, text
from app.csvparser.real_time_csv_parser import RealTimeCsvProcess
from app.config.models import Real_Time_Transaction_Data, Parking, Lane, Parking_In_Out_Record, Einvoice_Number_Data
import shutil,os
from sqlalchemy.orm import sessionmaker
class RealTimeTransactionParserService:
    """ every thing about parsing """
    _db =None

    """ the file which is used by parser to identify the file type and data"""
    _csv_file_names = None;
    def __init__(self, db):
        self._db = db
        self._timestamp =datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")

    async def parse(self,location,account_id):       
        process_data = RealTimeCsvProcess(self._db)
        csvCollection = process_data.real_time_transaction_process(location)
        """ parse the csv file into database """
        async with self._db.acquire() as conn:
            trans =await conn.begin()
            try:
                for parse_data in csvCollection:
                    data = await process_data.process_csv_data(parse_data, account_id)
                    parking_bean = data['parking_bean']
                    einvoice_bean = data['einvoice_bean']
                    real_time_transaction_bean = data['real_time_transaction_bean']
                    in_or_out = parse_data[2]                
                    driveway_info = await self.get_driveway_info(parking_bean, parse_data[13], in_or_out ,real_time_transaction_bean)
                    print(f'---parking---{parking_bean}--')
                    #aisle = lane_info['aisle']
                    if parse_data is not None:
                        await self.get_parking_in_info_by_card_id(parking_bean, in_or_out)
                        parking_id = await self.add_or_update_parking(parking_bean, in_or_out)
                        real_time_transaction_bean['parking_id'] = parking_id
                        # parking_in_out_bean['parking_id'] = parking_id
                        real_time_transaction_bean['exit_type_config_detail_id'] = await self.get_exit_config_id_by_garage_code(parse_data[14])
                        await self.add_real_time_transaction_data(real_time_transaction_bean)
                        # result = await self.add_parking_in_out_record(parking_in_out_bean, in_or_out)
                    # TODO 在確認備份是否要改動
                await trans.commit()
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                self.move_to_backup(location)
        return True

    async def add_or_update_parking(self, parking_bean : dict, in_or_out : str):
        async with self._db.acquire() as conn:
            if "0" is in_or_out :
                is_new = await (await conn.execute(Parking.select().where(Parking.c.garage_id == parking_bean['garage_id']).where(Parking.c.card_id16 == parking_bean['card_id16']).where(Parking.c.enter_time == parking_bean['enter_time']))).fetchall()
                if len(is_new) == 0 :
                    print('true')
                    parking_id = (await conn.execute(Parking.insert().values(parking_bean))).lastrowid
                else:
                    print('else')
                    print(is_new)
                    sql = """ select parking_id from parking where card_id = :card_id and garage_id=:garage_id and enter_time = :enter_time order by enter_time desc limit 1 """
                    parking_id = await(await conn.execute(text(sql), {"card_id" : parking_bean['card_id'],"garage_id" :parking_bean['garage_id'],"enter_time":parking_bean['enter_time'] })).scalar()
                    parking_result = await conn.execute(Parking.update().values(parking_bean).where(Parking.c.parking_id == parking_id))    
            elif "1" is in_or_out:
                sql = """  select parking_id from parking where card_id = :card_id and garage_id=:garage_id and enter_time = :enter_time order by enter_time desc limit 1  """
                parking_id = await(await conn.execute(text(sql), {"card_id" : parking_bean['card_id'],"garage_id" :parking_bean['garage_id'],"enter_time":parking_bean['enter_time'] })).scalar()
                parking_result = await conn.execute(Parking.update().values(parking_bean).where(Parking.c.parking_id == parking_id))
        return parking_id

    async def add_real_time_transaction_data(self, data : dict) -> int:
        """  處理新即時交易資料相關邏輯 """
        async with self._db.acquire() as conn:
            rz = await conn.execute(Real_Time_Transaction_Data.insert().values(data))
        return rz

    async def get_exit_config_id_by_garage_code(self, garage_code : str):
        """ get exit_config_id """
        select_exit_config_sql = """select exit_config_id 
                                    from exit_config where garage_id = (
                                                                        select garage_id 
                                                                        from garage
                                                                        where garage_code = :garage_code ) """
        async with self._db.acquire() as conn:
            exit_config_id = await(await conn.execute(text(select_exit_config_sql), {"garage_code" : garage_code})).scalar()
        return exit_config_id

    async def get_parking_in_info_by_card_id(self, parking_bean : dict, in_or_out : str) -> dict:
        """ 取得進場時的parking資訊 """
        select_parking_sql = "select enter_time, parking_id from parking where card_id =:card_id order by parking_id desc limit 1"
        if "0" is in_or_out:
            return
        async with self._db.acquire() as conn:
            temp = [dict(row.items()) async for row in await conn.execute(text(select_parking_sql), {"card_id" : parking_bean['card_id']})]
            parking_bean['parking_id'] = temp[0]['parking_id']
            parking_bean['enter_time'] = temp[0]['enter_time'] 
            temp_duration = (parking_bean['exit_time'] - parking_bean['enter_time']).seconds / 3600
            parking_bean['duration'] = math.ceil(temp_duration)
            return parking_bean
    
    async def add_parking_in_out_record(self, data : dict, in_or_out : str):
        """ handle parking_in_out_record """
        async with self._db.acquire() as conn:
            if "1" is in_or_out :
                temp = [dict(row.items()) async for row in await conn.execute(Parking_In_Out_Record.select().where(Parking_In_Out_Record.c.card_id == data['card_id']))]
                data['entry_time'] = temp[0]['entry_time']
            insert_result = await conn.execute(Parking_In_Out_Record.insert().values(data))
            return insert_result
    
    async def get_driveway_info(self, parking_bean : dict, pv_ip : str, in_or_out : str ,real_time_transaction_bean: dict) -> dict:
        vehicle_type_dict = {'01':'汽車' ,'02':'汽車','03':'大客車'}
        vehicle_type = vehicle_type_dict.get(real_time_transaction_bean['vehicle_type'])
        async with self._db.acquire() as conn:
            data = [dict(row.items()) async for row in await conn.execute(Lane.select().where(Lane.c.pv_ip == pv_ip))]
            #lane_info = {"pv" : data[0]['pv'], "aisle" : data[0]['aisle']}
            #進場
            if "0" is in_or_out:
                parking_bean['pv'] = f'{vehicle_type}入口'
                parking_bean['pv_out'] = '出口'
            #出場
            elif "1" is in_or_out:
                parking_bean['pv_out'] = f'{vehicle_type}出口'
            return True

    def move_to_backup(self,location):
        p = Path(location)
        print(location)
        backup_path = f'{location}/backup'
        pattern = "^\\d+_\\d+_\\d+\\.csv$"
        l = list(p.glob('**/*.csv'))
        print(f'{l}')
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        for z in l:
            print(z.name)
            if re.match(pattern,z.name):
                print("true")
                shutil.copy(z,backup_path+"/"+z.name)
                os.remove(z)
                os.rename(os.path.join(backup_path,z.name),os.path.join(backup_path,f'bak__{self._timestamp}_{z.name}'))          
        return True
