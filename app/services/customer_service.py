
import jwt,json
from datetime import datetime, timedelta

from app.config.models import Customer,Permission, Account
from sqlalchemy import desc
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler


class CustomerService:
    """ every thing about customer """
    _db =None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

    async def get_customers(self):
        """ get all customer """
        if self._user.is_superuser:
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(Customer.select().order_by(desc(Customer.c.create_date)))]
                return result
        else:
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(Customer.select().where(Customer.c.customer_id == self._user.customer_id).order_by(desc(Customer.c.create_date)))]
                return result
        
    async def get_customer_by_id(self,id):
        """ get customer by id """
        async with self._db.acquire() as conn:
            data= await conn.execute(Customer.select().where((Customer.c.customer_id == id)))
            return await data.fetchone()

    async def delete_customer_by_id(self,customer_id):
        self._syslog['create_account_id']=customer_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']='delete_customer_by_id : id='+ customer_id
        result = await self._log_service.addlog(self._syslog)
        id = int(customer_id)
        async with self._db.acquire() as conn:
            result = await conn.execute(Customer.delete().where(Customer.c.customer_id == id))
            return result.rowcount

    async def add_customer(self,customer:Customer):
        self._syslog['create_account_id']=customer['create_account_id']
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']='add_customer: '+json.dumps(customer,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            print(f'customer------{customer}')
            result = await conn.execute(Customer.insert(customer))
            return result.lastrowid

    async def update_customer(self,customer:Customer,id:int):
        self._syslog['create_account_id']=customer['modified_account_id']
        self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
        self._syslog['event_message']=json.dumps(customer,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)

        async with self._db.acquire() as conn:
            result = await conn.execute(Customer.update().where(Customer.c.customer_id == id).values(customer))
            return result.rowcount

    async def get_customer_latest_update_date_by_customer_id(self,customer_id:int):
        result = await self.get_customer_by_id(customer_id)
        return result is None and '1980-01-01 00:00:00' or str(result[17])
