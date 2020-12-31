import aiomysql.sa, json
from app.util.custom_json_encoder import custom_json_handler
from sqlalchemy import text, desc
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import select
from app.config.models import DeviceEvent, Account
from app.services.service import Service
from app.module.csv_handler import CsvHandler
from app.services.system_configuration import SystemConfigurationService
from app.module.csv_spec import CsvSpec

from app.config.system_event_type import SystemEventType
class DeviceEventService(Service):
    """ device_ibox info handler """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    async def get_device_event(self) -> []:
        """ get all device """
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(DeviceEvent.select().order_by(desc(DeviceEvent.c.device_event_id)))]
            return result

    async def add_device_event(self, device_event: dict) -> int:
        self._syslog['create_account_id']=self._user.account_id
        self._syslog['event_id']=SystemEventType.ADD_DEVICE_EVENT.value
        self._syslog['event_message']= json.dumps(device_event,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        
        async with self._db.acquire() as conn:
            result = await conn.execute(DeviceEvent.insert().values(device_event))
            k = await conn.execute('SELECT LAST_INSERT_ID() AS id')
            resultone = await k.fetchone()
            return resultone[0]
    
    async def get_device_event_greatter_by_device_id(self) -> []:
        """ get all device """
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(DeviceEvent.select().order_by(desc(DeviceEvent.c.device_event_id)))]
            return result