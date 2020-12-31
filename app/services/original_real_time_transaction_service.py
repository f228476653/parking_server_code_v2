
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Parking,Account,Role,Permission,Real_Time_Transaction_Data

from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler


class OriginalRealTimeTransactionService:
    """ every thing about pms transaction"""
    _db =None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    async def query_transaction(self,query: dict,customer_id,order = "desc"):
        where_condition = []
        join_str = []
        table_name = []
        join_condition = []
        
        #轉乘優惠
        #join_str.append(' as temp_parking left join transfer_parking_data as transfer_parking on temp_parking.id = transfer_parking.parking_id')
        #table_name.append( ' temp_parking')
        #join_condition.append(' and 1=1')

        #garage
        join_str.append( f" as temp_transfer left join garage as g on  temp_transfer.garage_code = g.garage_code ")
        table_name.append( 'temp_transfer.*, g.garage_name ,g.garage_id')
        """
        table_name.append( 'temp_transfer')
        """
        join_condition.append(' and 1=1')

        #電子發票
        join_str.append( f" as temp_garage left join e_invoice_number_data as e on temp_garage .id = e.sales_id and temp_garage.garage_code = e.garage_code ")
        table_name.append( 'temp_garage.*,e.invoice_number ')
        """
        table_name.append( 'temp_garage')
        """
        join_condition.append(' and 1=1')
        """
        #車辨
        #join_str.append( f" as temp_einvoice left join parking_lpr_data as lpr on temp_einvoice.id = lpr.parking_id ")
        #table_name.append( 'temp_einvoice')
        #join_condition.append( ' and 1=1 ' )
        """
        

        #sql = "select id, pv, pv_out, card_id, card_id16, t1.`type` as `type` from parking_view as t1 left join parking_costrule_view as pcview on t1.id = pcview.pid where 1 = 1 and exit_time != '0000-00-00 00:00:00' and paid_time != '0000-00-00 00:00:00' and settlement_type = 0"
        #print(query)
        select_sql = f"""select id, pv, pv_out, card_id, card_id16, t1.`type` as `type`, garage_code ,enter_time, paid_time, exit_time,CAST(timediff( exit_time,enter_time) AS char)as timediff , 
        fee, real_fee, paid_type, disability_mode from parking_view as t1 where 1 = 1  and exit_time  <> '0000-00-00 00:00:00' and paid_time  <> '0000-00-00 00:00:00' and settlement_type = 0 """
        # out
        if query.__contains__('card_id16'):
            where_condition.append( " and card_id16 = '" + query['card_id16']+"'")
        
        if query.__contains__('garage_code'):
            where_condition.append( " and garage_code = '" + query['garage_code']+"'")
        
        if query.__contains__('car_type'):
            #sql += " and (t1.type = '" + data['card_type'] +"' or pcview.type = '"+ data['card_type'] +"')";
            where_condition.append( " and t1.type = '" + query['car_type']+"'")
       
        if query.__contains__('pv_in'):
            where_condition.append( " and pv = '"+ query['pv_in']+"'")

        if query.__contains__('pv_out'):
            where_condition.append( " and pv_out ='"+query['pv_out']+"'")

        if query.__contains__('paid_type'):
            where_condition.append( " and paid_type='"+query['paid_type']+"'")

        if query.__contains__('enter_time_begin') and query.__contains__('enter_time_end'):
            where_condition.append(" and enter_time between '"+ query['enter_time_begin']+"' and '"+ query['enter_time_end']+"'")
        elif query.__contains__('enter_time_begin'):
            where_condition.append( " and enter_time > '"+query['enter_time_begin']+"'")
        elif query.__contains__('enter_time_end'):
            where_condition.append( " and enter_time < '"+ query['enter_time_end']+"'")
        
        if query.__contains__('paid_time_begin') and query.__contains__('paid_time_end'):
            where_condition.append( " and exit_time between '"+ query['paid_time_begin'] +"' and '" + query['paid_time_end']+"'")
        elif query.__contains__('paid_time_begin'):
            where_condition.append(" and exit_time > '"+query['paid_time_begin']+"'")
        elif query.__contains__('paid_time_end'):
            where_condition.append(" and exit_time < '"+query['paid_time_end']+"'")

        if query.__contains__('real_fee'):
            where_condition.append(" and real_fee = '"+ query['real_fee']+"'")
        
        if query.__contains__('einvoice_number') :
            join_condition[1] = f"and e.sales_id > 0 and e.use_status = 1 and e.invoice_number like '{query['einvoice_number']}' "
        
        if query.__contains__('invoice_check'):
            if query['invoice_check'] == '1':
                join_condition[1] = f"and e.sales_id > 0 and e.use_status = 1  "

        condition = ''.join(where_condition)
        #print(condition)
        sql = select_sql + condition 

        sql += " order by `enter_time` " + order
        for i in range(len(join_str)):
            single_table_name = str(table_name[i])
            single_join = str(join_str[i])
            single_condition = str(join_condition[i])
            sql = f'select {single_table_name} from ( {sql} ) {single_join} where 1 = 1 {single_condition}'
        garage_id_sql = ''
        if query.__contains__('garage_group_id'):
            if self._user.is_superuser:
                if query['garage_group_id']!='all':
                    garage_id_sql =""" where garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                        garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+str(query['garage_group_id']) + ')'
            if not self._user.is_superuser:
                if query['garage_group_id']!='all':
                    garage_id_sql =  """ where garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                    garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+str(query['garage_group_id']) + ' and g.customer_id='+str(self._user.customer_id)+')'
                else:
                    garage_id_sql = """ where garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                        left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                        where ma.account_id= """ + str(self._user.account_id)+ ')' 
        else:
            if not self._user.is_superuser:
                garage_id_sql =  """ where and garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                    left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                    where ma.account_id= """ + str(self._user.account_id)+ ')'

        sql = f'select *, (@SN:=@SN +1) as no  from ( {sql} ) as tend,(SELECT @SN :=0) as number {garage_id_sql} order by garage_code, paid_time {order}'
       
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(sql)]
            return result
    
    async def select_db(self,sql) :
        async with self._db.acquire() as conn:
            result = await conn.execute(sql)
            return result

