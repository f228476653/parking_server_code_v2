
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account,SystemLog,Shift_Checkout

from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
import random, string


class ShiftCheckoutService:
    """ post checkout data """
    _db =None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    async def add_shift_checkout(self,shift_checkout:Shift_Checkout):
        self._syslog['create_account_id']=shift_checkout['create_account_id']
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']= json.dumps(shift_checkout,default=custom_json_handler)
        shift_checkout['data_in_json'] = str(shift_checkout['data_in_json']).replace("'","'/")
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Shift_Checkout.insert().values(shift_checkout))
            r = shift_checkout['checkout_no']
            return r
    
    async def get_shift_checkout_by_condition(self, data):
        async with self._db.acquire() as conn:
            where_clause = {}
            sql = """ select s.* , g.garage_name from shift_checkout s left join garage g on s.garage_id = g.garage_id where  1=1 """
            if 'checkout_no' in data and data['checkout_no'] != '':
                sql = sql + " and s.checkout_no = :checkout_no"
                where_clause['checkout_no'] = data['checkout_no']
            if 'query_date_start' in data:
                sql = sql + f" and s.checkout_time  >= '{data['query_date_start']} 00:00:00' "
            if 'query_date_end' in data:
                sql = sql + f" and s.checkout_time  <= '{data['query_date_end']} 23:59:59' "
            if 'garage_id' in data:
                sql = sql + " and s.garage_id = :garage_id"
                where_clause['garage_id'] = data['garage_id']
            if 'garage_group_id' in data:
                if data['garage_group_id'] != 'all':
                    sql = sql + " and s.garage_id in (select garage_id from map_garage_to_garage_group where garage_group_id = :garage_group_id)"
                    where_clause['garage_group_id'] = data['garage_group_id']
                else :
                    print(self._user.is_superuser)
                    if self._user.is_superuser:
                        sql = sql + " and 1=1 "
                    else:
                        sql = sql + f""" and s.garage_id 
                        in (select garage_id from map_garage_to_garage_group where garage_group_id 
                        in (select garage_group_id from map_garage_group_to_account where account_id = :account_id))"""       
            else:
                if self._user.is_superuser:
                    sql = sql + " and 1=1 "
                else :
                    sql = sql + f""" and s.garage_id 
                    in (select garage_id from map_garage_to_garage_group where garage_group_id 
                        in (select garage_group_id from map_garage_group_to_account where account_id = :account_id))"""
            where_clause['account_id'] = data['account_id']
            print(sql)
            data = [dict(row.items()) async for row in await conn.execute(text(sql), where_clause)]
            return data

    
