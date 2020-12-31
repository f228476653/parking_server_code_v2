
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Clock_Time_Card

from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler

class ClockInAndOutService:
    """ everything about clock in and out"""
    _db =None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    
    async def add_clock_record(self,clock_time_card):
        """ every thing about clock in and clock off """
        self._syslog['create_account_id']=clock_time_card['create_account_id']
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']=  json.dumps(clock_time_card,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            r = await conn.execute(Clock_Time_Card.insert().values(clock_time_card))
            return None
