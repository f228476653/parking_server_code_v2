import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
from app.services.device_ibox_service import DeviceIboxService
from app.services.garage_service import GarageService

class GarageManagementService:
    """ management all garage related service """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    garage_service: GarageService = None
    device_ibox_service: DeviceIboxService = None

    def __init__(self, db, user: Account):
        self._db = db
        self._user = user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        self.garage_service = GarageService(self._db, self._user)
        self.device_ibox_service = DeviceIboxService(self._db, self._user)

    async def add_garage_and_garage_device_configuration(self, data: dict):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                last_insert_id = await self.garage_service.add_garage(data['garage'], conn)
                last_insert_id = last_insert_id[0]
                for i in data['device_type']:
                    if i == 'iBox':
                        bean = data['iBox']
                        bean['garage_id'] = last_insert_id['garage_id']
                        bean['garage_code'] = data['garage']['garage_code']
                        bean['update_user'] = self._user['account']
                        bean['update_time'] = datetime.now()
                        await self.device_ibox_service.save_garage_device_args(bean, conn)
                    elif i == 'PV3':
                        print('施工中>>>>')
            except Exception as e:
                await trans.rollback()
                raise PermissionError(e,"新增場站及場站設備參數錯誤 error")
            else:
                await trans.commit()
                return last_insert_id
    
    async def delete_garage_and_garage_device_configuration(self, id: int, account_id: int):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result1 = await self.garage_service.delete_garage_by_id(id, account_id, conn)
                result2 = await self.device_ibox_service.delete_garage_device_argument_by_garage_id(id, conn)
            except Exception as e:
                await trans.rollback()
                raise PermissionError(e,"delete args error")
            else:
                await trans.commit()
                return result1 & result2
                
    async def update_garage_and_garage_device_configuration(self, data: dict):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.garage_service.update_garage(data['garage'])
                for i in data['device_type']:
                    if i == 'iBox':
                        bean = data['iBox']
                        await self.device_ibox_service.save_garage_device_args(bean, conn)
            except Exception as e:
                await trans.rollback()
                raise e
            else:
                await trans.commit()
                return result