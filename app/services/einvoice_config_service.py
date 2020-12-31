
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import GaragePadArgs,E_Invoice_Config
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler

from app.services.systemlog_service import SystemlogService

class EinvoiceConfigService:
    """ every thing about einvoice"""
    _db =None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    async def get_garage_einvoice_config(self,garage_id):
        async with self._db.acquire() as conn:
            garage_config = await(await conn.execute(GaragePadArgs.select().where(GaragePadArgs.c.garage_id == garage_id))).fetchone()
            einvoice_config = [dict(row.items()) async for row in  await conn.execute(E_Invoice_Config.select()
            .where(E_Invoice_Config.c.e_invoice_config_id == garage_config['e_invoice_config_id'])
            .where(E_Invoice_Config.c.is_used == '1'))]
            return einvoice_config

    async def get_last_update_einvoice_config(self,garage_id):
        einvoice_config = await self.get_garage_einvoice_config(garage_id)
        return len(einvoice_config) > 0 and str(einvoice_config[0]['update_time']) or '1980-01-01 00:00:00'

    async def add_customer_level_einvoice_config(self, config,customer_id):
        async with self._db.acquire() as conn:
            for c in config:
                print(c)
                if c:
                    #self._syslog['create_account_id']=c['create_account_id']
                    self._syslog['event_id']=SystemEventType.Add.value
                    self._syslog['event_message']='add_customer_level_einvoice_config: '+json.dumps(c,default=custom_json_handler)
                    result_log = await self._log_service.addlog(self._syslog)
                    c['customer_id'] = customer_id
                    result = await conn.execute(E_Invoice_Config.insert().values(c))
            return result.lastrowid

    async def update_customer_level_einvoice_config(self, config,customer_id):
        print('update_add1')
        async with self._db.acquire() as conn:
            print(f'43534543-----------{config}')
            i= 0
            for c in config:
                if c:
                    i= i+1
                    print(f'3424---------{c}')
                    set_before = await conn.execute(E_Invoice_Config.select().where(E_Invoice_Config.c.customer_id == customer_id).where(E_Invoice_Config.c.einvoice_company == c['einvoice_company']))
                    print(f'!@#@!#--------{set_before.rowcount}')
                    if set_before.rowcount == 0 :
                        print(f'addd ---------{c}')
                        c['customer_id'] = customer_id
                        result = await conn.execute(E_Invoice_Config.insert().values(c))
                    else:
                        print(f'update ---------{c}')
                        c['customer_id'] = customer_id
                        result = await conn.execute(E_Invoice_Config.update().values(c)
                        .where(E_Invoice_Config.c.customer_id == c['customer_id'])
                        .where(E_Invoice_Config.c.einvoice_company == c['einvoice_company']))
                    print(f'----------------{i}')
            return 0
            

    async def get_customer_level_einvoice_config(self,customer_id):
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(E_Invoice_Config.select()
            .where(E_Invoice_Config.c.customer_id == customer_id))]
        return result
    

            
