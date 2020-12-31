
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.sql import select
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Parking,Account,Role,Permission,Garage,Real_Time_Transaction_Data,Shift_Checkout
from app.module.sql_clause import ParkingSQL, PageSQL
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
from app.models.real_time_and_parking_compound import RealtimeParkingCompound


class RealTimeTransactionService:
    """ every thing about tablat transaction data"""
    _db =None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    async def get_transaction(self,data,order = "desc"):
        where_condition = []
        #原本 p.garage_code = c.garage_code
        select_sql = """
	select parking_id,garage_name,vehicle_identification_number,enter_time,exit_time,paid_time as pay_datetime,exit_type_name ,user_name
        ,'sedan' as vehicle_type,real_fee as real_fees ,invoice_number
        from (select  r.user_name,p.*,c.garage_name,c.garage_id,r.exit_type_name ,r.invoice_number from `parking` as p join garage c on 
        p.garage_id = c.garage_id left join (
        select aa.account,CONCAT(aa.user_first_name,aa.user_last_name)  as user_name,pk.exit_time,pk.parking_id,ex.exit_type as exit_type_name,rt.einvoice as invoice_number from real_time_transaction_data rt right join parking pk on rt.parking_id= pk.parking_id
left join exit_type_config_detail ex on rt.exit_type_config_detail_id = ex.exit_type_config_detail_id
left join account aa on rt.create_account_id = aa.account_id 
where rt.in_or_out = 1 and rt.record_status= 1 and pk.record_status= 1)r on r.parking_id =p.parking_id) a 	
	"""
        
        """in or out"""
        if data.__contains__('in_or_out') and data['in_or_out'] == '1' :
            if data.__contains__('exit_time_from') and data['exit_time_from'] != None and data['exit_time_from'] != '0000-00-00 00:00:00':
                where_condition.append('a.`in_or_out_datetime` >=' + '"'+ data['exit_time_from']+'"')
            if data.__contains__('exit_time_to') and data['exit_time_to'] != None and data['exit_time_to'] != '0000-00-00 00:00:00':
                where_condition.append('a.`in_or_out_datetime`  <=' + '"'+ data['exit_time_to']+'"')
            if data.__contains__('card_id_appearance') and data['card_id_appearance'] != None and data['card_id_appearance'] != '':
                where_condition.append('a.`card_id_appearance` = ' + '"'+data['card_id_appearance']+'"')
            if data.__contains__('card_id_16') and data['card_id_16'] != None and data['card_id_16'] != '':
                where_condition.append('a.`card_id_16` = ' + '"'+data['card_id_16']+'"')
            if data.__contains__('disability_mode') and data['disability_mode'] != None and data['disability_mode'] != '':
                where_condition.append('a.disability_mode='+'"'+ data['disability_mode']+'"')
            if data.__contains__('vehicle_identification_number') and data['vehicle_identification_number'] != None and data['vehicle_identification_number'] != '':
                where_condition.append('a.`vehicle_identification_number` like ' +'"%%'+ data['vehicle_identification_number'] +'%%"')
            if data.__contains__('in_or_out'):
                where_condition.append('a.`in_or_out` =' +'"'+ data['in_or_out']+'"')
        elif data.__contains__('in_or_out') and data['in_or_out'] == '0' :
            if data.__contains__('enter_time_to') and data['enter_time_to'] != None and data['enter_time_to'] != '0000-00-00 00:00:00':
                where_condition.append('a.`in_or_out_datetime` <=' + '"'+ data['enter_time_to']+'"')
            if data.__contains__('enter_time_from') and data['enter_time_from'] != None and data['enter_time_from'] != '0000-00-00 00:00:00':
                where_condition.append('a.`in_or_out_datetime`  >=' + '"'+ data['enter_time_from']+'"')
            if data.__contains__('card_id_appearance') and data['card_id_appearance'] != None and data['card_id_appearance'] != '':
                where_condition.append('a.`card_id_appearance` = ' + '"'+data['card_id_appearance']+'"')
            if data.__contains__('card_id_16') and data['card_id_16'] != None and data['card_id_16'] != '':
                where_condition.append('a.`card_id_16` = ' + '"'+data['card_id_16']+'"')
            if data.__contains__('disability_mode') and data['disability_mode'] != None and data['disability_mode'] != '':
                where_condition.append('a.disability_mode='+'"'+ data['disability_mode']+'"')
            if data.__contains__('vehicle_identification_number') and data['vehicle_identification_number'] != None and data['vehicle_identification_number'] != '':
                where_condition.append('a.`vehicle_identification_number` like ' +'"%%'+  data['vehicle_identification_number'] +'%%"')  
            if data.__contains__('in_or_out'):
                where_condition.append('a.`in_or_out` =' +'"'+ data['in_or_out']+'"')

	       
        condition = ' and '.join(where_condition)
        if len(condition)>0 :
             condition = 'and' + condition
        if 'garage_id' in data:
               sql = select_sql + 'where garage_id = '+ '"'+ str(data['garage_id']) +'"'+ ' and 1=1 ' + condition
        elif 'garage_group_id' in data:
            if self._user.is_superuser:
                if data['garage_group_id']!='all':
                    sql = select_sql + """ where garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                        garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+str(data['garage_group_id']) + ')'+' and 1=1' +condition
                else:
                    sql = select_sql  +' where 1=1 '+condition
            if not self._user.is_superuser:
                if data['garage_group_id']!='all':
                    sql = select_sql + """ where garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                    garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+str(data['garage_group_id']) + ' and g.customer_id='+str(self._user.customer_id)+')'+' and 1=1' +condition
                else:
                    sql = select_sql + """where garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                        left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                        where ma.account_id= """ + str(self._user.account_id)+ ')' + condition
        else:
            if self._user.is_superuser:
                sql = select_sql  +' where 1=1 '+condition
            if not self._user.is_superuser:
                sql = select_sql + """where garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                    left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                    where ma.account_id= """ + str(self._user.account_id)+ ')' + condition
        sql += " order by `create_date` " + order

        async with self._db.acquire() as conn:
            print('+++++++++')
            print(sql)
            print('+++++++++')
            data_count = await conn.execute(sql)
            if data_count.rowcount >0 :
                result = [dict(row.items()) async for row in data_count]
            else:
                result = None
            return result

    async def add_transaction(self,transaction):
        async with self._db.acquire() as conn:
            trans =await conn.begin()
            try: 
                real_time_data = transaction.copy()
                transaction['garage_code'] = await(await conn.execute(select([Garage.c.garage_code]).where(Garage.c.garage_id == transaction['garage_id']))).scalar()
                compound = RealtimeParkingCompound(transaction)
                parking = compound.parking
                parking_id = '0'
                if  real_time_data['in_or_out'] == '0' :
                    result = await conn.execute(Parking.insert().values(parking))
                    real_time_data['parking_id'] = result.lastrowid
                    parking_id=result.lastrowid
                if  real_time_data['in_or_out'] == '1' :
                    result = await conn.execute(Parking.update().values(parking).where(Parking.c.parking_id == parking['parking_id']).where(Parking.c.garage_id == parking['garage_id']))
                    parking_id = parking['parking_id'] == '' and 0 or int(parking['parking_id'])
                if await self.check_is_new(real_time_data):
                    await conn.execute(Real_Time_Transaction_Data.insert().values(real_time_data))
                else :
                    await conn.execute(Real_Time_Transaction_Data.update().values(real_time_data).where(Real_Time_Transaction_Data.c.parking_id == real_time_data['parking_id']).where(Real_Time_Transaction_Data.c.in_or_out == real_time_data['in_or_out']))
                    self._syslog['create_account_id']=self._user['account_id']
                    self._syslog['event_id']=667
                    self._syslog['event_message']='add_transaction : ='+ f'Real_Time_Transaction_Data -- {real_time_data} -- has inert before'
                    result = await self._log_service.addlog(self._syslog)
            except Exception as e:
                await trans.rollback()
                self._syslog['create_account_id']=self._user['account_id']
                self._syslog['event_id']=666
                self._syslog['event_message']='add_transaction : ='+ f'error: {e}, data: {real_time_data}'
                result = await self._log_service.addlog(self._syslog)
                raise
            else:
                await trans.commit()
                return parking_id

    async def check_is_new(self ,real_time_data) ->bool:
        print(real_time_data['in_or_out_datetime'])
        sql = f"""select * from real_time_transaction_data where parking_id = {real_time_data['parking_id']}
            and in_or_out_datetime = '{real_time_data['in_or_out_datetime']}'
            and  in_or_out = {real_time_data['in_or_out']}
            and  garage_id = {real_time_data['garage_id']} """
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(sql)]
            print(sql)
            if len (result) > 0:
                return False
            else:
                return True

    async def delete_transaction_by_id(self,parking_id,account_id,garage_id) -> bool:

        #to do add log
        async with self._db.acquire() as conn:
            result = await conn.execute('DELETE FROM real_time_transaction_data  where parking_id ="' + parking_id+'" and garage_id="' + garage_id +'" ')
            result = await conn.execute('DELETE FROM parking where parking_id  ="'+ parking_id+'" and  garage_code  ="'+ garage_id+'"')
            return True

    async def get_transaction_by_checkout_no(self,checkout_no,garage_id):
        """use checkout_no get clock_in_time and clock_out_time , then get transaction data in this period"""
        async with self._db.acquire() as conn:
            shift_checkout_result= await conn.execute(Shift_Checkout.select().where(Shift_Checkout.c.checkout_no == checkout_no).where(Shift_Checkout.c.garage_id == garage_id))
            result= await shift_checkout_result.fetchone()
            if result != None:
                clock_in_time= result['clock_in_time']
                clock_out_time= result['clock_out_time']
                rt_sql="""select 
                out_record.out_count,
                out_record.real_fees_total,
		out_record.receivable_total,
                in_record.in_count ,shift_checkout.data_in_json
                from 
(select data_in_json from shift_checkout where checkout_no=:checkout_no and garage_id =:garage_id order by create_date desc limit 1 ) as shift_checkout,
                (select IFNULL(CAST(count(*) AS UNSIGNED INTEGER),CAST('0' AS UNSIGNED INTEGER)) as in_count from real_time_transaction_data
                where in_or_out_datetime >=:clock_in_time and in_or_out_datetime <=:clock_out_time and in_or_out='0' and garage_id =:garage_id and record_status =1 ) as in_record,
                (select IFNULL(CAST(count(*) AS UNSIGNED INTEGER),CAST('0' AS UNSIGNED INTEGER)) as out_count ,IFNULL(CAST(sum(real_fees) AS UNSIGNED INTEGER), CAST('0' AS UNSIGNED INTEGER)) as real_fees_total,IFNULL(CAST(sum(receivable) AS UNSIGNED INTEGER),CAST('0' AS UNSIGNED INTEGER)) as receivable_total  from real_time_transaction_data
                where in_or_out_datetime >=:clock_in_time and in_or_out_datetime <=:clock_out_time and in_or_out='1' and garage_id =:garage_id and record_status =1 ) as out_record  """
                print(rt_sql)
                transaction_result= [dict(row.items()) async for row in await conn.execute(text(rt_sql),{'clock_in_time' : clock_in_time, 'clock_out_time' : clock_out_time ,'garage_id' :garage_id ,'checkout_no':checkout_no})]
            else:
                transaction_result = None
            return transaction_result

    async def cancel_parking(self,parking_id):
        cancel_result = True
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rt= await conn.execute(Real_Time_Transaction_Data.select().where(Real_Time_Transaction_Data.c.parking_id == parking_id))
                if rt.rowcount > 0:
                    record_status={'record_status':0}
                    "rt_update = await conn.excete(Real_Time_Transaction_Data.update().values(record_status).where(Real_Time_Transaction_Data.c.parking_id= parking_id))"
                    "pk_update = await conn.excete(Parking.update().values(record_status).where(Parking.c._id= _id))"
                    rt_update = await conn.execute(Real_Time_Transaction_Data.update().values(record_status).where(Real_Time_Transaction_Data.c.parking_id== parking_id))
                    pk_update = await conn.execute(Parking.update().values(record_status).where(Parking.c.parking_id== parking_id))
                else:
                    cancel_result = False
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()
            return cancel_result

    async def get_transaction_by_garage_code(self, query_clause: dict):
        """ get real_time_transaction_info """
        select_condition = ParkingSQL()
        query = select_condition.query_argu_by_str(query_clause,self._user)
        async with self._db.acquire() as conn:
            data = [dict(row.items()) async for row in await conn.execute(text(query['sql']),query['arg'])]
        return data

    async def get_transaction_pad(self,data,order = "desc"):
        where_condition = []
        #原本 p.garage_code = c.garage_code
        sql =""
        select_sql = """ 
        select * from (
            select 
            p.parking_id as parking_id 
            ,c.garage_name as garage_name
            ,rt.vehicle_identification_number as vehicle_identification_number
            ,p.enter_time as enter_time
            ,p.exit_time as exit_time
            ,dv.device_type ,
            IF(p.exit_time ='0000-00-00 00:00:00' ,0 ,cast(TIMEDIFF(p.exit_time, p.enter_time) AS CHAR)) as diff_hours
            ,p.vehicle_type as vehicle_type 
            ,p.fee as receivable
            ,p.real_fee as real_fee
            ,ex.exit_type as exit_type_name
            ,rt.exit_type_config_detail_remarks as exit_type_config_detail_remarks 
            ,CONCAT(aa.user_first_name,aa.user_last_name)  as user_name 
            ,rt.einvoice as invoice_number  
            ,rt.tax_id_number_buyer as tax_id_number_buyer 
            ,p.record_status as record_status
            ,c.garage_id
            from parking p
            left join garage c on p.garage_id = c.garage_id
            left join (select * from real_time_transaction_data where in_or_out =1) rt on p.parking_id = rt.parking_id
            left join exit_type_config_detail ex on rt.exit_type_config_detail_id = ex.exit_type_config_detail_id
            left join account aa on rt.create_account_id = aa.account_id
            left join device_view dv on dv.garage_id = c.garage_id
            where p.exit_time <> '0000-00-00 00:00:00' and p.record_status=1
            union all

            select 
            p.parking_id as parking_id 
            ,c.garage_name as garage_name
            ,rt.vehicle_identification_number as vehicle_identification_number
            ,p.enter_time as enter_time
            ,p.exit_time as exit_time
            ,dv.device_type ,
            IF(p.exit_time ='0000-00-00 00:00:00' ,0 ,cast(TIMEDIFF(p.exit_time, p.enter_time) AS CHAR)) as diff_hours
            ,p.vehicle_type as vehicle_type 
            ,p.fee as receivable
            ,p.real_fee as real_fee
            ,ex.exit_type as exit_type_name
            ,rt.exit_type_config_detail_remarks as exit_type_config_detail_remarks 
            ,CONCAT(aa.user_first_name,aa.user_last_name)  as user_name 
            ,rt.einvoice as invoice_number  
            ,rt.tax_id_number_buyer as tax_id_number_buyer 
            ,p.record_status as record_status
            ,c.garage_id
            from parking p
            left join garage c on p.garage_id = c.garage_id
            left join (select * from real_time_transaction_data where in_or_out = 0) rt on p.parking_id = rt.parking_id
            left join exit_type_config_detail ex on rt.exit_type_config_detail_id = ex.exit_type_config_detail_id
            left join account aa on rt.create_account_id = aa.account_id
            left join device_view dv on dv.garage_id = c.garage_id
            where p.exit_time = '0000-00-00 00:00:00' and p.record_status=1
        ) a
        
	"""
        if data.__contains__('paid_time_begin') and data['paid_time_begin'] != None and data['paid_time_begin'] != '0000-00-00 00:00:00':
            where_condition.append('a.`paid_time` >=' + '"'+ data['paid_time_begin']+'"')
        if data.__contains__('paid_time_end') and data['paid_time_end'] != None and data['paid_time_end'] != '0000-00-00 00:00:00':
            where_condition.append('a.`paid_time`  <=' + '"'+ data['paid_time_end']+'"')
        if data.__contains__('exit_time_begin') and data['exit_time_begin'] != None and data['exit_time_begin'] != '0000-00-00 00:00:00':
            where_condition.append('a.`exit_time` >=' + '"'+ data['exit_time_begin']+'"')
        if data.__contains__('exit_time_end') and data['exit_time_end'] != None and data['exit_time_end'] != '0000-00-00 00:00:00':
            where_condition.append('a.`exit_time`  <=' + '"'+ data['exit_time_end']+'"')
        if data.__contains__('vehicle_identification_number') and data['vehicle_identification_number'] != None and data['vehicle_identification_number'] != '':
            where_condition.append('a.`vehicle_identification_number` like ' +'"%%'+ data['vehicle_identification_number'] +'%%"')
        if data.__contains__('enter_time_begin') and data['enter_time_begin'] != None and data['enter_time_begin'] != '0000-00-00 00:00:00':
            where_condition.append('a.`enter_time` >=' + '"'+ data['enter_time_begin']+'"')
        if data.__contains__('enter_time_end') and data['enter_time_end'] != None and data['enter_time_end'] != '0000-00-00 00:00:00':
            where_condition.append('a.`enter_time`  <=' + '"'+ data['enter_time_end']+'"')
        if data.__contains__('exit_type_config_detail_name') and data['exit_type_config_detail_name'] != None and data['exit_type_config_detail_name'] != '':
            where_condition.append('a.`exit_type_name` like ' +'"%'+ data['exit_type_config_detail_name']+'%"')
        if data.__contains__('real_fee') and data['real_fee'] != None and data['real_fee'] != '':
            where_condition.append('a.`real_fee` =' +'"'+ data['real_fee']+'"')
        if data.__contains__('einvoice_number') and data['einvoice_number'] != None and data['einvoice_number'] != '':
            where_condition.append('a.`invoice_number` =' +'"'+ data['invoice_number']+'"')            
        if data.__contains__('create_user_name') and data['create_user_name'] != None and data['create_user_name'] != '':
            where_condition.append('a.`user_name` like ' +'"%'+ data['create_user_name']+'%"') 
        if data.__contains__('vehicle_type') and data['vehicle_type'] != None and data['vehicle_type'] != '' and data['vehicle_type'] != 'all':
            where_condition.append('a.`vehicle_type` =' + str(data['vehicle_type']))
        if data.__contains__('abnormal') and data['abnormal'] != None and data['abnormal'] == True:
            where_condition.append("`record_status` <> '1' ")
        elif data.__contains__('abnormal') and data['abnormal'] != None and data['abnormal'] == 'check':
            pass
        else:
            where_condition.append("`record_status` = '1' ")
	       
        condition = ' and '.join(where_condition)
        if len(condition) > 0:
            condition = ' and ' + condition

        if  data.__contains__('garage_id') and data['garage_id'] != '':
               sql = select_sql + 'where garage_id = '+ '"'+ str(data['garage_id']) +'"' + condition
        elif data.__contains__('garage_group_id'):
            if self._user.is_superuser:
                if data['garage_group_id']!='all':
                    sql = select_sql + """ where garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                        garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+str(data['garage_group_id']) + ')'+' and 1=1' +condition
                else:
                    sql = select_sql  +' where 1=1 '+condition
            if not self._user.is_superuser:
                if data['garage_group_id']!='all':
                    sql = select_sql + """ where garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                    garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+str(data['garage_group_id']) + ' and g.customer_id='+str(self._user.customer_id)+')'+' and 1=1' +condition
                else:
                    sql = select_sql + """where garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                        left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                        where ma.account_id= """ + str(self._user.account_id)+ ')' + condition
        else:
            if self._user.is_superuser:
                sql = select_sql  +' where 1=1 '+condition
            if not self._user.is_superuser:
                sql = select_sql + """where garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                    left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                    where ma.account_id= """ + str(self._user.account_id)+ ')' + condition

        sql += f" and device_type='3'  order by `parking_id`  {order} "

        async with self._db.acquire() as conn:
            print('-'*10)
            print(sql)
            print('-'*10)
            data_count = await conn.execute(sql)
            if data_count.rowcount >0 :
                result = [dict(row.items()) async for row in data_count]
            else:
                result = []
            return result


    async def add_complete_transaction(self,transaction):
        async with self._db.acquire() as conn:
            trans =await conn.begin()
            try: 
                real_time_data = transaction.copy()
                transaction['garage_code'] = await(await conn.execute(select([Garage.c.garage_code]).where(Garage.c.garage_id == transaction['garage_id']))).scalar()
                compound = RealtimeParkingCompound(transaction)
                parking = compound.parking
                parking_id = '0'
                if  real_time_data['in_or_out'] == '0' :
                    result = await conn.execute(Parking.insert().values(parking))
                    real_time_data['parking_id'] = result.lastrowid
                    parking_id=result.lastrowid
                if  real_time_data['in_or_out'] == '1' :
                    result = await conn.execute(Parking.update().values(parking).where(Parking.c.parking_id == parking['parking_id']).where(Parking.c.garage_id == parking['garage_id']))
                    parking_id = parking['parking_id'] == '' and 0 or int(parking['parking_id'])
                if await self.check_is_new(real_time_data):
                    await conn.execute(Real_Time_Transaction_Data.insert().values(real_time_data))
                else :
                    await conn.execute(Real_Time_Transaction_Data.update().values(real_time_data).where(Real_Time_Transaction_Data.c.parking_id == real_time_data['parking_id']).where(Real_Time_Transaction_Data.c.in_or_out == real_time_data['in_or_out']))
                    self._syslog['create_account_id']=self._user['account_id']
                    self._syslog['event_id']=667
                    self._syslog['event_message']='add_transaction : ='+ f'Real_Time_Transaction_Data -- {real_time_data} -- has inert before'
                    result = await self._log_service.addlog(self._syslog)
            except Exception as e:
                await trans.rollback()
                self._syslog['create_account_id']=self._user['account_id']
                self._syslog['event_id']=666
                self._syslog['event_message']='add_transaction : ='+ f'error: {e}, data: {real_time_data}'
                result = await self._log_service.addlog(self._syslog)
                raise
            else:
                await trans.commit()
                return parking_id