import aiomysql.sa
from sqlalchemy import text
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import select
from app.config.models import DevicePV
from app.services.service import Service

class DevicePvService(Service):
    """ device_pv info handler """
    _db = None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
    
    async def add_device_pv(self, customer_id: int, device_pv_bean: dict):
        if self.is_account_has_authorization_to_use_garage(customer_id):
            async with self._db.acquire() as conn:
                result = await conn.execute(DevicePV.insert().values(device_pv_bean));
                return result.lastrowid
        raise PermissionError("check_account_has_authorization_to_use_garage","not permit to quesry other customer's data")
    
    async def show_all_device_pv_by_garage_id(self, customer_id: int, garage_id: int):
        if await self.is_account_has_authorization_to_use_garage(customer_id):
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(DevicePV.select()
                .where(DevicePV.c.garage_id == garage_id))]
                return result
        raise PermissionError("check_account_has_authorization_to_use_garage","not permit to quesry other customer's data")

    async def show_device_pv_by_device_id(self, customer_id: int, device_pv_id: int):
        if await self.is_account_has_authorization_to_use_garage(customer_id):
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(DevicePV.select().where(DevicePV.c.device_pv_id == device_pv_id))]
                return result[0]
        raise PermissionError("check_account_has_authorization_to_use_garage","not permit to quesry other customer's data")
            
    async def update_device_pv_by_device_id(self, customer_id: int, device_pv_bean: dict):
        if self.is_account_has_authorization_to_use_garage(customer_id):
            async with self._db.acquire() as conn:
                result = await conn.execute(DevicePV.update().values(device_pv_bean)
                .where(DevicePV.c.device_pv_id == device_pv_bean['device_pv_id']))
                return result.rowcount
            raise PermissionError("check_account_has_authorization_to_use_garage","not permit to quesry other customer's data")    

    async def delete_device_pv_by_device_pv_id(self, customer_id: int, device_pv_id: int):
        if self.is_account_has_authorization_to_use_garage(customer_id):
            async with self._db.acquire() as conn:
                result = await conn.execute(DevicePV.delete().where(DevicePV.c.device_pv_id == device_pv_id))
                return result.rowcount
        raise PermissionError("check_account_has_authorization_to_use_garage","not permit to quesry other customer's data")
