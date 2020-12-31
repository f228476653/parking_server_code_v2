
import jwt,json
from sqlalchemy import desc,func
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account,SystemLog,Parking,Trx_Data,Lane,Einvoice_Number_Data,Garage
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from sqlalchemy.sql import select
from app.util.custom_json_encoder import custom_json_handler
import asyncio


class PmsDataUploadService:
    """ post checkout data """
    _db =None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    async def add_pms_parking(self,parking_data:Parking,create_account):
        self._syslog['create_account_id']=create_account
        self._syslog['event_id']=7001
        self._syslog['event_message']= json.dumps(parking_data,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        columns = ['id','pv' ,'pv_out','card_id', 'card_id16', 'enter_time' ,'exit_time' 
        ,'paid_time','duration' ,'fee' ,'real_fee' ,'note' ,'paid_type' ,'entry_balance','exit_balance'
        ,'settlement_type' ,'txn_datetime' ,'txn_amt' ,'disability_mode','card_autoload_flag' ,'entry_mode' ,'garage_code']
            #value = [dict(zip(columns,p)) for p in parking_data]
            #print(type(p))
            #print(value)
        for p in parking_data:
            async with self._db.acquire() as conn:
                value = dict(zip(columns,p))
                count = [dict(row.items()) async for row in await conn.execute(Parking.select().where(Parking.c.id == value['id']).where(Parking.c.garage_code == value['garage_code']))]
                garage_id = await(await conn.execute(select([Garage.c.garage_id]).where(Garage.c.garage_code == value['garage_code']))).scalar()
                value['garage_id'] = garage_id
                if len(count) >= 1:
                    result = await conn.execute(Parking.update().values(value).where(Parking.c.id == value['id']).where(Parking.c.garage_code == value['garage_code']))
                else:
                    result = await conn.execute(Parking.insert().values(value))
        return True

    async def add_pms_lane(self,lane_data:Lane,create_account):
        self._syslog['create_account_id']=create_account
        self._syslog['event_id']=7002
        #self._syslog['event_message']= json.dumps(Lane,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        columns = ['garage_lane_id','pv' ,'type' ,'pricing_scheme' ,'pv_ip' ,'pv_netmask' ,'pv_gateway' 
        ,'pms_ip' ,'pms_port' ,'ecc_ip' ,'ecc_port' ,'in_out' ,'aisle' ,'invoice','cps_ip' 
        ,'pv_cutoff' ,'MEntryB' ,'MExitD','pv_version' ,'last_response_time','response_type' 
        ,'invoice_printer_status','pricing_scheme_disability' ,'pv_response_confirm','etag_flag' 
        ,'costrule_using_para' ,'lane_costrule_mode' ,'gate_control_mode'  ,'garage_code']
        async with self._db.acquire() as conn:
            for p in lane_data:
                value = dict(zip(columns,p))
                count = [dict(row.items()) async for row in await conn.execute(Lane.select().where(Lane.c.garage_lane_id == value['garage_lane_id']).where(Lane.c.garage_code == value['garage_code']))]
                garage_id = await(await conn.execute(select([Garage.c.garage_id]).where(Garage.c.garage_code == value['garage_code']))).scalar()
                value['garage_id'] = garage_id
                if len(count) >= 1:
                    result = await conn.execute(Lane.update().values(value).where(Lane.c.garage_lane_id == value['garage_lane_id']).where(Lane.c.garage_code == value['garage_code']))
                else:
                    result = await conn.execute(Lane.insert().values(value))
                await asyncio.sleep(0.1)
        return True

    async def add_pms_einvoice_number(self,einvoice_data:Einvoice_Number_Data,create_account):
        self._syslog['create_account_id']=create_account
        self._syslog['event_id']=7003
        self._syslog['event_message']= json.dumps(einvoice_data,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        columns = ['no' ,'tax_id' ,'tax_id_buyer' ,'random_code','use_year_month' ,
        'invoice_number' ,'einvoice_print_status' ,'donate_status' ,'sale_print_status' ,
        'preserve_code' ,'einvoice_device_no' ,'txn_total_amt' ,'invoice_amt' ,
        'txn_date' ,'txn_time' ,'merchant_id','counter_id','pos_id',
        'batch_number' ,'transaction_number','business_date','process_status',
        'process_time' ,'upload_status' ,'upload_time' ,'use_status' ,
        'use_time' ,'sales_type' ,'sales_id' ,'update_time' ,'update_user','garage_code']
        async with self._db.acquire() as conn:
            #value = [dict(zip(columns,p)) for p in parking_data]
            #print(type(p))
            #print(value)invoice_number use_year_month
            for p in einvoice_data:
                p = ['' if c is None else c for c in p]
                value = dict(zip(columns,p))
                count = [dict(row.items()) async for row in await conn.execute(Einvoice_Number_Data.select()
                .where(Einvoice_Number_Data.c.use_year_month == value['use_year_month'])
                .where(Einvoice_Number_Data.c.invoice_number == value['invoice_number'])
                .where(Einvoice_Number_Data.c.garage_code == value['garage_code']))]
                garage_id = await(await conn.execute(select([Garage.c.garage_id]).where(Garage.c.garage_code == value['garage_code']))).scalar()
                value['garage_id'] = garage_id
                if len(count) >= 1:
                    result = await conn.execute(Einvoice_Number_Data.update().values(value)
                    .where(Einvoice_Number_Data.c.use_year_month == value['use_year_month'])
                    .where(Einvoice_Number_Data.c.invoice_number == value['invoice_number'])
                    .where(Einvoice_Number_Data.c.garage_code == value['garage_code']))
                else:
                    result = await conn.execute(Einvoice_Number_Data.insert().values(value))
                await asyncio.sleep(0.1)
        return True

    async def add_pms_trx_data(self,trx_data:Trx_Data,create_account):
        self._syslog['create_account_id']=create_account
        self._syslog['event_id']=7004
        self._syslog['event_message']= json.dumps(trx_data,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        columns = ['import_date','file_name','trx_date' ,'trx_time' ,'card_no' ,
        'txn_no' ,'trx_amt' ,'device_id' ,'trx_type' ,'trx_sub_type' ,
        'el_value' ,'cal_date' ,'cal_status' ,'dept_id' ,'unit_id' ,
        'cal_err_code' ,'update_date' ,'garage_code']
        async with self._db.acquire() as conn:
            for p in trx_data:
                value = dict(zip(columns,p))
                count = [dict(row.items()) async for row in await conn.execute(Trx_Data.select()
                .where(Trx_Data.c.trx_date == value['trx_date'])
                .where(Trx_Data.c.trx_amt == value['trx_amt'])
                .where(Trx_Data.c.trx_time == value['trx_time'])
                .where(Trx_Data.c.card_no == value['card_no'])
                .where(Trx_Data.c.garage_code == value['garage_code']))]
                if len(count) >= 1:
                    result = await conn.execute(Trx_Data.update().values(value)
                    .where(Trx_Data.c.trx_date == value['trx_date'])
                    .where(Trx_Data.c.trx_time == value['trx_time'])
                    .where(Trx_Data.c.card_no == value['card_no'])
                    .where(Trx_Data.c.garage_code == value['garage_code'])
                    .where(Trx_Data.c.trx_amt == value['trx_amt']))
                else:
                    result = await conn.execute(Trx_Data.insert().values(value))
        return True
