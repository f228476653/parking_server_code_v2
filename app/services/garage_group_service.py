
import jwt,json
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import desc,func, text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Garage,GarageGroup,Map_Garage_To_Garage_Group, Account

from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler


class GarageGroupService:
    """ everything about garage group (which are under customer_id constraint)"""
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

    async def get_garage_groups(self):
        if self._user.is_superuser:
            async with self._db.acquire() as conn:
                # return [dict(row.items()) async for row in await conn.execute(GarageGroup.select().order_by(desc(GarageGroup.c.create_date)))]
                sql = """ SELECT g.*, c.company_name FROM garage_group AS g LEFT JOIN customer AS c ON g.customer_id = c.customer_id ORDER BY g.create_date DESC"""
                return [dict(row.items()) async for row in await conn.execute(text(sql))]
        else:
            return await self.get_garage_groups_by_customer_id(self._user.customer_id)

    async def get_map_garage_to_garage_group_by_garage_group_id(self,garage_group_id) -> [Map_Garage_To_Garage_Group]:
        async with self._db.acquire() as conn:
            s = [dict(row.items()) async for row in await conn.execute(Map_Garage_To_Garage_Group.select().where(Map_Garage_To_Garage_Group.c.garage_group_id == garage_group_id))]
            return s

    async def get_garage_group_by_id(self,id: int):
        async with self._db.acquire() as conn:
            data= await conn.execute(GarageGroup.select().where((GarageGroup.c.garage_group_id == id)))
            return await data.fetchone()

    async def get_garage_groups_by_customer_id(self, customer_id:int) -> [GarageGroup]:
        async with self._db.acquire() as conn:
            # result = [dict(row.items()) async for row in await conn.execute(GarageGroup.select().where( GarageGroup.c.customer_id == customer_id))]
            sql = """ SELECT g.*, c.company_name FROM garage_group AS g LEFT JOIN customer AS c ON g.customer_id = c.customer_id WHERE g.customer_id=:customer_id ORDER BY g.create_date DESC"""
            result = [dict(row.items()) async for row in await conn.execute(text(sql),{'customer_id':customer_id})]
            return result

    async def get_garage_groups_by_account_id(self, account_id:int) -> [GarageGroup]:
        if self._user.is_superuser:
            sql = "select * from garage_group "
        else:
            sql = "select * from garage_group where garage_group_id in (select garage_group_id from map_garage_group_to_account where account_id=:account_id)"
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(text(sql), {"account_id" : account_id})]
            return result

    async def add_garage_group(self,garage_group,garages:List[int]):
        self._syslog['create_account_id']=garage_group['create_account_id']
        self._syslog['event_id']=SystemEventType.ADD_GARAGE_GROUP.value
        self._syslog['event_message']= json.dumps(garage_group,default=custom_json_handler)+json.dumps(garages,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(GarageGroup.insert().values(garage_group))
            garage_group_id = result.lastrowid
            for item in garages:
                    await conn.execute(Map_Garage_To_Garage_Group.insert().values(garage_group_id =garage_group_id, garage_id = item))

            r = await conn.execute(GarageGroup.select().where(GarageGroup.c.garage_group_id == garage_group_id))
            r = await r.fetchone()
            return r

    async def update_garage_group(self,garage_group,garages:List[int]) -> GarageGroup:
        self._syslog['create_account_id']=garage_group['create_account_id']
        self._syslog['event_id']=SystemEventType.UPDATE_GARAGE_GROUP.value
        self._syslog['event_message']= json.dumps(garage_group,default=custom_json_handler)+json.dumps(garages,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            await conn.execute(Map_Garage_To_Garage_Group.delete().where(Map_Garage_To_Garage_Group.c.garage_group_id == garage_group['garage_group_id']))
            result = await conn.execute(GarageGroup.update().values(garage_group).where(GarageGroup.c.garage_group_id == garage_group['garage_group_id']))
            for item in garages:
                    await conn.execute(Map_Garage_To_Garage_Group.insert().values(garage_group_id = garage_group['garage_group_id'], garage_id = item))
            return garage_group

    async def delete_garage_group_by_id(self,id,account_id) -> bool:
        self._syslog['create_account_id']=account_id
        self._syslog['event_id']=SystemEventType.DELETE_GARAGE_GROUP.value
        self._syslog['event_message']= f'{{\"id\": {id}}}'
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(GarageGroup.delete().where((GarageGroup.c.garage_group_id == id)))
            result2 = await conn.execute(Map_Garage_To_Garage_Group.delete().where((Map_Garage_To_Garage_Group.c.garage_group_id == id)))
            return True





            
