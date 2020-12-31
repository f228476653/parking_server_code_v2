
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account,Role,Permission,Parking,Real_Time_Transaction_Data,Einvoice_Number_Data,GaragePadArgs,E_Invoice_Config
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler


class EinvoiceService:
    """ every thing about einvoice"""
    _db =None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    async def add_einvoice(self,in_or_out,account_id,einvoice):
        #帶發票資訊、in or out、parking_id
        #如果沒資料 就新增，
        #有資料 return error
        self._syslog['create_account_id']=account_id
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']='add_einvoice: '+json.dumps(einvoice,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        parking_id = einvoice['sales_id']
        async with self._db.acquire() as conn: 
            #TODO add garage_id
            garage_code = einvoice['garage_code']
            select_stmt="""select invoice_number from e_invoice_number_data where sales_id =:parking_id and garage_code =:garage_code and  use_status = 1 """
            einvoice_data = await conn.execute(text(select_stmt),{'parking_id':parking_id,'garage_code':garage_code})
            trans = await conn.begin()
            try:
                if einvoice_data == None or einvoice_data=='':
                    return 'not exist'
                else :
                    sql = 'update real_time_transaction_data set einvoice = "' + einvoice['invoice_number'] + '" ,einvoice_print_status = "' +einvoice['einvoice_print_status']+ '", tax_id_number_buyer="' +einvoice['tax_id_number_buyer']+ '" where parking_id = "' +parking_id+ '" and in_or_out = "' +in_or_out+ '"'
                    print(sql)
                    real_time_data = await conn.execute(sql)
                    print(einvoice)
                    einvoice_insert = await conn.execute(Einvoice_Number_Data.insert().values(einvoice))
            except Exception as e:
                await trans.rollback()
                print(e)
                return False
            else:
                await trans.commit()
                return True
    
    async def update_einvoice(self,data:Einvoice_Number_Data) ->bool:
        """ update einvoice """
        self._syslog['update_account_id']=data['update_user']
        self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
        self._syslog['event_message']= json.dumps(data,default=custom_json_handler)
        async with self._db.acquire() as conn:
            result = await conn.execute(Einvoice_Number_Data.update().values(data).where(Einvoice_Number_Data.c.invoice_number == data['invoice_number']).where(Einvoice_Number_Data.c.garage_code==data['garage_code']).where(Einvoice_Number_Data.c.sales_id==data['sales_id']).where(Einvoice_Number_Data.c.use_year_month==data['use_year_month']))
        return True
 
    async def delete_einvoice(self,in_or_out:int,parking_id:int,account_id) -> bool:
        #帶發票資訊、in or out、parking_id
        #delete 發票資料
        self._syslog['create_account_id']=account_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']= 'delete_einvoice: parking_id = : '+ parking_id
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute('DELETE FROM e_invoice_Number_Data where parking_id =\"' + parking_id+'\"')
            result = await conn.execute('UPDATE Real_Time_Transaction_Data set einvoice = \"\",modify_id =\"'+ account_id + '\",modify_date =\"'+ datetime.quinow() + '\", einvoice_print_status = \"\", tax_id_number_buyer = \"\" where parking_id =\"'+ parking_id+ '\" and in_or_out = \"'+ in_or_out +'\" ')
            return True



            
