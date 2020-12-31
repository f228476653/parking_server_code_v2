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
from app.services.device_event_service import DeviceEventService
from app.services.fee_service import FeeService

class DeviceManager:
    """ management all garage related service """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    garage_service: GarageService = None
    device_ibox_service: DeviceIboxService = None
    device_event_service: DeviceEventService = None
    fee_service: FeeService = None
    
    def __init__(self, db, user: Account):
        self._db = db
        self._user = user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        self.garage_service = GarageService(self._db, self._user)
        self.device_ibox_service = DeviceIboxService(self._db, self._user)
        self.device_event_service = DeviceEventService(self._db, self._user)
        self.fee_service = FeeService(self._db, self._user)

    async def get_device_event(self) -> []:
        return await self.device_event_service.get_device_event()

    async def add_device_event(self, device_event: dict):
        return await self.device_event_service.add_device_event(device_event)

    async def device_export(self, data: dict, device_type: str, car_type):
        print('現在觀察匯出')
        if await self.is_args_exist(data, device_type, car_type):
            print('資料正確')
            print(data['garage_id'])
            print(car_type)
            # print(car_type)
            await self.device_ibox_service.device_export(data)
            # !!費率暫時關閉!!
            # await self.fee_service.build_csv(data['garage_id'], car_type)
        else:
            print('有錯')
        return True

    async def is_args_exist(self, data: dict, device_type: str, car_type):
        # !!費率暫時關閉!!
        # flag1 = await self.fee_service.get_fee_args(data['garage_id'], car_type)
        # flag1 = flag1['status']
        # if not flag1:
        #     raise Exception('費率參數尚未設定 請先設定費率')
        if device_type == 'iBox':
            flag2 = await self.device_ibox_service.is_ibox_args_exists(data['customer_id'], data['garage_id'], data['device_ibox_args_id'])
            if not flag2:

                raise Exception('iBox參數尚未設定')
        # TODO PV3, PAD CASE
        return True

    async def download_device_parameter(self, data: dict, device_type: str, car_type):
        print('現在觀察匯出')
        print('資料正確')
        print(data['garage_id'])
        print(device_type)
        if "iBox" == device_type:
            await self.device_ibox_service.download_device_parameter(data)
        return True
