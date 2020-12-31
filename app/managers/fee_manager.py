from datetime import datetime
from app.config.models import Account
from app.services.systemlog_service import SystemlogService
from app.services.fee_service import FeeService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
class FeeManager:
    """ management all fee related service """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    _fee: FeeService = None

    def __init__(self, db, user: Account):
        self._db = db
        self._user = user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        self._fee = FeeService(self._db, self._user)
    
    async def store_fee_args(self, data: dict):
        data['feeRule']['update_user'] = self._user['account']
        data['feeRule']['update_time'] = datetime.now()
        data['feePara1']['update_user'] = self._user['account']
        data['feePara1']['update_time'] = datetime.now()
        data['feePara2']['update_user'] = self._user['account']
        data['feePara2']['update_time'] = datetime.now()
        if "fee_rule_id" in data['feeRule']:
            print('執行更新', data)
            return await self._fee.update_fee_args(data['feeRule'], data['feePara1'], data['feePara2'])
        else:
            print('執行新增', data)
            return await self._fee.save_fee_args(data['feeRule'], data['feePara1'], data['feePara2'])

    async def get_fee_args(self, garage_id: int, car_type: str):
        return await self._fee.get_fee_args(garage_id, car_type)

    async def delete_fee_args(self, fee_rule_id: int):
        return await self._fee.delete_fee_args(fee_rule_id)

    async def get_special_day_list(self, year: int):
        return await self._fee.get_special_day_list(year)
