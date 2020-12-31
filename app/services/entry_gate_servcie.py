
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account,EntryGate,SystemLog

from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler


class EntryGateService:
    """ every thing about user , like account, permission, role"""
    _db =None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    async def add_entry_gate(self,entry_gate:EntryGate):
        self._syslog['create_account_id']=entry_gate['create_account_id']
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']= json.dumps(entry_gate,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(EntryGate.insert().values(entry_gate))
            r = await self.get_entry_gate_by_id(result.lastrowid)
            return r

    async def get_entry_gate_by_id(self,id):
        """ get entry_gate by id """
        async with self._db.acquire() as conn:
            queryResult= await conn.execute(EntryGate.select().where((EntryGate.c.entry_gate_id == id)))
            result= await queryResult.fetchone()
            return result
    
    async def get_entry_gates_by_garage_id(self,garage_id):
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(
                'select t1.*,t2.garage_name from entry_gate t1 join garage t2 on t1.garage_id = t2.garage_id where staiton_id =:id',{'id':garage_id})]
            return result

    async def get_entry_gates_by_customer_id(self,customer_id):
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(
                'select t1.*,t2.garage_name from entry_gate t1 join garage t2 on t1.garage_id = t2.garage_id where customer_id =:id',{'id':customer_id})]
            return result

    async def get_entry_gates_by_garage_id_sn(self,garage_id,sn):
        """ get used sn according to the garage_id """
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(
                text('select t1.*,t2.garage_name from entry_gate t1 join garage t2 on t1.garage_id = t2.garage_id where t1.garage_id=:garage_id and t1.entry_gate_sn=:sn'),{'garage_id':garage_id,'sn':sn})]
            return result

    async def update_entry_gate(self,entry_gate:EntryGate) -> int:
        """ update entry_gate """
        self._syslog['update_account_id']=entry_gate['modified_account_id']
        self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
        self._syslog['event_message']= json.dumps(entry_gate,default=custom_json_handler)
        async with self._db.acquire() as conn:
            r = await conn.execute(EntryGate.update().values(entry_gate).where(EntryGate.c.entry_gate_id == entry_gate['entry_gate_id']))
            r2 = await self._log_service.addlog(self._syslog)
            result = await self.get_entry_gate_by_id(entry_gate['entry_gate_id'])
            return result

    async def delete_entry_gate_by_id(self,id,account_id) -> bool:
        self._syslog['create_account_id']=account_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']= 'delete_entry_gate_by_id: id = : '+ id
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(EntryGate.delete().where((EntryGate.c.entry_gate_id == id)))
            return True

    async def get_entry_gates(self):
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(
                'select t1.*,t2.garage_name from entry_gate t1 join garage t2 on t1.garage_id = t2.garage_id')]
            return result


            