import jwt,json
import inspect
from struct import *
from datetime import datetime, timedelta

from sqlalchemy import desc,text
from app.csvparser.csv_parser import CsvParser
from app.config.models import Trx_Data,Parking

class CliService:
    """ every thing about parsing """
    _db =None
    """ the file which is used by parser to identify the file type and data"""
    _csv_file_names = None;
    def __init__(self, db):
        self._db = db
        self._csv_file_names = {'01': '00220%', '03': 'DPTI%' ,'02': 'ICTX%' ,'05':'TXN_PARK%' };  #start with 00220 or DPTI

    async def query_records_after_manual_close(self, query):
        sql=""
        if query['paid_type'] == '01':
            sql="""select t1.id, t1.card_id as card_no, paid_time, t2.trx_amt, t1.real_fee, t1.paid_type
            from (select * from parking where date_format(exit_time, '%Y%m%d') = :query_date and paid_type = '99') as t1
            join (select t1.trx_amt, t2.id from trx_data as t1, parking as t2 where t2.settlement_type = 0 and t1.card_no = t2.card_id and t1.trx_date = :query_date
            and t2.exit_time != '0000-00-00 00:00:00' and t1.file_name like :file_name and t2.paid_type = '99' and date_format(t2.exit_time, '%Y%m%d') = :query_date and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s'))
            between '00:00:00' and '00:00:05') as t2 on t1.id = t2.id order by paid_time"""
        else:
            sql="""select t1.id, t1.card_id as card_no, paid_time, t2.trx_amt, t1.real_fee, t1.paid_type
             from (select * from `pms`.parking where date_format(exit_time, '%Y%m%d') = ':query_date and paid_type = '99') as t1
             join (select t1.trx_amt, t2.id from trx_data as t1, parking as t2 where t2.settlement_type = 0 and substring(t1.card_no,1,8) = t2.card_id16 and t1.trx_date = ':query_date
              and t2.exit_time != '0000-00-00 00:00:00' and t1.file_name like :file_name and t1.trx_type = '1' and t2.paid_type = '99' and date_format(t2.exit_time, '%Y%m%d') = ':query_date and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s')) between '00:00:00' and '00:00:05') as t2 on t1.id = t2.id order by paid_time"""

        if query['file_name'] == '':
            fileName = self._csv_file_names[query['paid_type']]
        else:
            fileName = query['file_name']
        obj = {
            'query_date': query['query_date'],
            'file_name': fileName
        }
        async with self._db.acquire() as conn:
            bind_sql = text(sql)
            result = [dict(row.items()) async for row in await conn.execute(bind_sql,obj)]
            return result

    async def query_pms_diff_record(self,query):
        sql=""
        if query['paid_type'] == '01':
            """ yoyo card """
            sql ="""select t1.id, t1.card_id16 as card_no, paid_time, t1.real_fee as trx_amt
from (
select * from parking where date_format(exit_time, '%Y%m%d') = :query_date
and paid_type = '01' and settlement_type = 0) as t1
left join (select t2.id from trx_data as t1,parking as t2 where t1.card_no = t2.card_id and t1.trx_date = :query_date
and t2.exit_time != '0000-00-00 00:00:00' and t1.file_name like :file_name and t2.paid_type = '01'
and date_format(t2.exit_time, '%Y%m%d') = :query_date
and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s')) between '00:00:00' and '00:00:05') as t2 on t1.id = t2.id where t2.id is NULL order by paid_time"""
        else:
            sql="""select t1.id, t1.card_id as card_no, paid_time, t1.real_fee as trx_amt
from (
select * from parking where date_format(exit_time, '%Y%m%d') = :query_date
and paid_type = '03' and settlement_type = 0) as t1
left join (select t2.id from trx_data as t1, parking as t2
where substring(t1.card_no,1,8) = t2.card_id16 and t1.trx_date = :query_date
and t2.exit_time != '0000-00-00 00:00:00' and t1.file_name like :file_name and t1.trx_type = '1'
and t2.paid_type = '03' and date_format(t2.exit_time, '%Y%m%d') = :query_date
and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s'))
between '00:00:00' and '00:00:05') as t2
on t1.id = t2.id where t2.id is NULL order by paid_time;
            """
        if query['file_name'] == '':
            fileName = self._csv_file_names[query['paid_type']]
        else:
            fileName = query['file_name']
        obj = {
            'query_date': query['query_date'],
            'file_name': fileName
        }
        async with self._db.acquire() as conn:
            bind_sql = text(sql)
            result = [dict(row.items()) async for row in await conn.execute(bind_sql,obj)]
            return result

    async def query_amt_diff_record(self,query):
        sql=""
        if query['paid_type'] == '01':
            """ yoyo card """
            sql ="""select t1.file_name, t1.trx_amt, CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),
'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',
substring(t1.trx_time,5,2)) as paid_time, t2.id, t2.card_id16 as card_no16, t2.real_fee , t2.paid_time from trx_data as t1,
parking as t2 where t2.garage_code = :garage_code and t1.card_no = t2.card_id and t1.trx_date = :query_date and t2.exit_time != '0000-00-00 00:00:00'
 and t1.file_name like :file_name and t2.paid_type = :paid_type and date_format(t2.exit_time, '%Y%m%d') = :query_date
 and t1.trx_amt <> t2.real_fee and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',
 substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)),
 '%Y-%m-%d %H:%i:%s')) between '00:00:00' and '00:00:05' order by paid_time;"""
        else:
            sql="""select t1.file_name, t1.trx_amt, CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',
 substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',
 substring(t1.trx_time,5,2)) as paid_time, t2.id, t2.card_id16 as card_no16, t2.real_fee, t2.paid_time from trx_data as t1,
 parking as t2 where t2.garage_code = :garage_code and t1.card_no = t2.card_id and t1.trx_date = :query_date and
 t2.exit_time != '0000-00-00 00:00:00' and t1.file_name like :file_name  and t1.trx_type = '1' and t2.paid_type = :paid_type and
 date_format(t2.exit_time, '%Y%m%d') = :query_date and t1.trx_amt <> t2.real_fee and timediff(t2.exit_time,
 str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',
 substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s'))
 between '00:00:00' and '00:00:05' order by paid_time;
            """
        if query['file_name'] == '':
            fileName = self._csv_file_names[query['paid_type']]
        else:
            fileName = query['file_name']
        obj = {
            'query_date': query['query_date'],
            'file_name': query['file_name'],
            'garage_code' : query['garage_code'],
            'paid_type': query['paid_type']
        }
        async with self._db.acquire() as conn:
            bind_sql = text(sql)
            result = [dict(row.items()) async for row in await conn.execute(bind_sql,obj)]
            return result

    async def query_cps_diff_record(self,query):
        sql=""
        if query['paid_type'] == '01':
            """ yoyo card """
            sql ="""select t1.garage_code, t1.file_name as id, t1.card_no, CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)) as paid_time,
             t1.trx_amt from (select * from trx_data where garage_code = :garage_code and trx_date = :query_date and file_name like :file_name) as t1
             left join (select t1.* from trx_data as t1, parking as t2 where t2.settlement_type = 0 and t1.card_no = t2.card_id and t1.trx_date = :query_date and t2.exit_time != '0000-00-00 00:00:00' and
              t1.file_name like :file_name and (t2.paid_type = :paid_type || t2.paid_type = '99') and date_format(t2.exit_time, '%Y%m%d') = :query_date and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s')) between '00:00:00' and '00:00:05') as t2
               on t1.file_name = t2.file_name and t1.trx_date = t2.trx_date and t1.trx_time = t2.trx_time and t1.card_no = t2.card_no and t1.txn_no = t2.txn_no where t2.trx_time is NULL order by paid_time;"""
        else:
            sql="""select t1.garage_code,t1.file_name as id, substring(t1.card_no,1,8) as card_no, CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)) as paid_time, t1.trx_amt
            from (select * from trx_data where trx_date = :query_date and garage_code = :garage_code and file_name like :file_name and trx_type not in ('00','03','42','90')) as t1
             left join (select t1.* from trx_data as t1, parking as t2 where t2.settlement_type = 0 and substring(t1.card_no,1,8) = t2.card_id16 and t1.trx_date = :query_date and t2.exit_time != '0000-00-00 00:00:00' and t1.file_name like :file_name and t1.trx_type not in ('00','03','42','90') and (t2.paid_type = :paid_type || t2.paid_type = '99') and date_format(t2.exit_time, '%Y%m%d') = :query_date and timediff(t2.exit_time, str_to_date(CONCAT(substring(t1.trx_date,1,4),'-',substring(t1.trx_date,5,2),'-',substring(t1.trx_date,7,2),' ',substring(t1.trx_time,1,2),':',substring(t1.trx_time,3,2),':',substring(t1.trx_time,5,2)), '%Y-%m-%d %H:%i:%s')) between '00:00:00' and '00:00:05') as t2
             on t1.file_name = t2.file_name and t1.trx_date = t2.trx_date and t1.trx_time = t2.trx_time and t1.card_no = t2.card_no and t1.txn_no = t2.txn_no where t2.trx_time is NULL order by paid_time;
            """
        if query['file_name'] == '':
            fileName = self._csv_file_names[query['paid_type']]
        else:
            fileName = query['file_name']
        obj = {
            'query_date': query['query_date'],
            'file_name': query['file_name'],
            'garage_code' : query['garage_code'],
            'paid_type': query['paid_type']
        }
        async with self._db.acquire() as conn:
            bind_sql = text(sql)
            result = [dict(row.items()) async for row in await conn.execute(bind_sql,obj)]
            #for x in result:
                #cardno_val = unpack('<L', pack('>L',int(x['card_no'])))
                #x['card_no'] = ('{0:x}'.format(cardno_val[0])).upper().zfill(8)
            return result

    async def query_parking_settlement_record(self,query):
        sql=""
        sql ="""SELECT * FROM `parking` WHERE garage_code = :garage_code and paid_type = :paid_type and settlement_type <> 0 and date_format(txn_datetime, '%Y%m%d') = :query_date ORDER BY `txn_datetime`;
            """
        obj = {
            'query_date': query['query_date'],
            'garage_code' : query['garage_code'],
            'paid_type': query['paid_type']
        }
        async with self._db.acquire() as conn:
            bind_sql = text(sql)
            result = [dict(row.items()) async for row in await conn.execute(bind_sql,obj)]
            return result

    async def query_accounting(self,query):
        if query['paid_type'] == '01':
            """ yoyo card """
            sql = """
                select * from (
                    select t5.paid_type,t5.cps_cnt,t5.cps_fee,t5.format_date,t5.pms_cnt,t5.pms_fee,t5.garage_code,(t5.pms_cnt-t5.cps_cnt) pms_cps_data_diff
                    ,(t5.pms_fee-t5.cps_fee) pms_cps_diff, garage.garage_name from (
                    select t1.paid_type,t1.garage_code,t1.format_date, t1.pms_cnt, t1.pms_fee, IF(t2.cps_cnt IS NULL, 0, t2.cps_cnt) as cps_cnt
                    , IF(t2.cps_fee IS NULL, 0, t2.cps_fee) as cps_fee
                from (
                    select paid_type,garage_code,count(*) as pms_cnt, sum(real_fee) as pms_fee, date_format(exit_time, '%Y%m%d') as format_date
                    from parking where paid_type = :paid_type and settlement_type = 0 and exit_time != '0000-00-00 00:00:00'
                    group by paid_type,garage_code,date_format(exit_time, '%Y%m%d')
                ) as t1

                left join (
                select garage_code,count(*) as cps_cnt, COALESCE(sum(trx_amt), 0) as cps_fee
                ,trx_date from trx_data where file_name like :file_name group by garage_code,trx_date) as t2 on t1.format_date = t2.trx_date
                where (1=1) and t1.garage_code = t2.garage_code) t5 join garage on t5.garage_code = garage.garage_code
                ) t6 left join (SELECT count(*) as settlement_diff ,date_format(txn_datetime, '%Y%m%d') as txn_d FROM parking WHERE settlement_type <> 0 group by date_format(txn_datetime, '%Y%m%d')) t7 on t6.format_date = t7.txn_d
            """
            if query['garage_code'] == '':
                sql = sql +"""
                left join (SELECT garage_code as g_8,trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and trx_type = '1' and file_name LIKE :file_name  GROUP BY g_8, trx_date ) t8 on (t8.trxdate_calstatus_c = t6.format_date and  t8.g_8= t6.garage_code)
                left join (SELECT garage_code as g_9,trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee FROM trx_data WHERE cal_status =  'F' and trx_type = '1' and file_name LIKE :file_name  GROUP BY g_9,trx_date ) t9 on (t9.trxdate_calstatus_f = t6.format_date and  t9.g_9= t6.garage_code)
                left join (SELECT garage_code as g_10,trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and trx_type = '1' and file_name LIKE :file_name  GROUP BY g_10,trx_date ) t10 on (t10.trxdate_calstatus_e = t6.format_date and  t10.g_10= t6.garage_code)
                where 1 =1
                """
            else:
                sql = sql +"""
                left join (SELECT trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and trx_type = '1' and file_name LIKE :file_name and garage_code = :garage_code  GROUP BY trx_date ) t8 on t8.trxdate_calstatus_c = t6.format_date
                left join (SELECT trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee FROM trx_data WHERE cal_status =  'F' and trx_type = '1' and file_name LIKE :file_name and garage_code = :garage_code GROUP BY trx_date ) t9 on t9.trxdate_calstatus_f = t6.format_date
                left join (SELECT trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and trx_type = '1' and file_name LIKE :file_name and garage_code = :garage_code GROUP BY trx_date ) t10 on t10.trxdate_calstatus_e = t6.format_date
                where 1 =1
                """

        elif query['paid_type'] == '02':
            """ icash card """
            sql = """
            select garage_code,garage_name,format_date,pms_cnt,pms_fee,cps_cnt,cps_fee,cal_f_totalfee,cal_e_totalfee,cal_c_totalfee,pms_cps_data_diff,pms_cps_diff,settlement_diff from (
            select t5.paid_type,t5.cps_cnt,t5.cps_fee,t5.format_date,t5.pms_cnt,t5.pms_fee,t5.garage_code,(t5.pms_cnt-t5.cps_cnt) pms_cps_data_diff
            ,(t5.pms_fee-t5.cps_fee) pms_cps_diff, garage.garage_name from (
            select t1.paid_type,t1.garage_code,t1.format_date, t1.pms_cnt, t1.pms_fee, IF(t2.cps_cnt IS NULL, 0, t2.cps_cnt) as cps_cnt
            , IF(t2.cps_fee IS NULL, 0, t2.cps_fee) as cps_fee
            from (
            select paid_type,garage_code,count(*) as pms_cnt, sum(real_fee) as pms_fee, date_format(exit_time, '%Y%m%d') as format_date
            from parking where paid_type = :paid_type and settlement_type = 0 and exit_time != '0000-00-00 00:00:00'
            group by paid_type,garage_code,date_format(exit_time, '%Y%m%d')
            ) as t1

            left join (
            select garage_code,count(*) as cps_cnt, COALESCE(sum(trx_amt), 0) as cps_fee
            ,trx_date from trx_data where file_name like :file_name and trx_type not in ('00','03','42','90','0')  group by garage_code,trx_date) as t2 on t1.format_date = t2.trx_date
            where (1=1) and t1.garage_code = t2.garage_code) t5 join garage on t5.garage_code = garage.garage_code
            ) t6 left join (SELECT count(*) as settlement_diff ,date_format(txn_datetime, '%Y%m%d') as txn_d FROM parking WHERE settlement_type <> 0 group by date_format(txn_datetime, '%Y%m%d')) t7 on t6.format_date = t7.txn_d
        """

            if query['garage_code'] == '':
                sql = sql +"""
                left join (SELECT garage_code as g, trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY g,trx_date ) t8 on (t8.trxdate_calstatus_c = t6.format_date and  t8.g= t6.garage_code)
                left join (
                    SELECT garage_code as g, trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee from (
						select * FROM trx_data WHERE cal_status =  'F' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name
						union all 
						SELECT * FROM trx_data WHERE cal_status =  'E' and (cal_err_code = '8' or cal_err_code = '4') and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name
					)a  GROUP BY g,trx_date
                ) t9 on (t9.trxdate_calstatus_f = t6.format_date and t9.g= t6.garage_code)
                left join (SELECT garage_code as g, trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and cal_err_code != '8' and cal_err_code != '4' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP  BY g,trx_date ) t10 on (t10.trxdate_calstatus_e = t6.format_date and t10.g= t6.garage_code)
                where 1 =1
                """
            else :
                sql = sql +"""
                left join (SELECT trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY trx_date ) t8 on t8.trxdate_calstatus_c = t6.format_date
                left join (
                    SELECT trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee from
                    (
                    SELECT *
                    FROM trx_data WHERE cal_status =  'F' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') 
                    and file_name LIKE :file_name 
                    union all
                    SELECT * FROM trx_data WHERE cal_status =  'E' 
                    and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name and (cal_err_code = '8' or cal_err_code = '4')
                    ) a GROUP BY trx_date 
                ) t9 on t9.trxdate_calstatus_f = t6.format_date
                left join (SELECT trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and cal_err_code != '8' and cal_err_code != '4' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY trx_date ) t10 on t10.trxdate_calstatus_e = t6.format_date
                where 1 =1
                """

        elif query['paid_type'] == '03':
            """ ipass card """
            sql = """
            select garage_code,garage_name,format_date,pms_cnt,pms_fee,cps_cnt,cps_fee,cal_f_totalfee,cal_e_totalfee,cal_c_totalfee,pms_cps_data_diff,pms_cps_diff,settlement_diff from (
            select t5.paid_type,t5.cps_cnt,t5.cps_fee,t5.format_date,t5.pms_cnt,t5.pms_fee,t5.garage_code,(t5.pms_cnt-t5.cps_cnt) pms_cps_data_diff
            ,(t5.pms_fee-t5.cps_fee) pms_cps_diff, garage.garage_name from (
            select t1.paid_type,t1.garage_code,t1.format_date, t1.pms_cnt, t1.pms_fee, IF(t2.cps_cnt IS NULL, 0, t2.cps_cnt) as cps_cnt
            , IF(t2.cps_fee IS NULL, 0, t2.cps_fee) as cps_fee
            from (
            select paid_type,garage_code,count(*) as pms_cnt, sum(real_fee) as pms_fee, date_format(exit_time, '%Y%m%d') as format_date
            from parking where paid_type = :paid_type and settlement_type = 0 and exit_time != '0000-00-00 00:00:00'
            group by paid_type,garage_code,date_format(exit_time, '%Y%m%d')
            ) as t1

            left join (
            select garage_code,count(*) as cps_cnt, COALESCE(sum(trx_amt), 0) as cps_fee
            ,trx_date from trx_data where file_name like :file_name and trx_type not in ('00','03','42','90','0')  group by garage_code,trx_date) as t2 on t1.format_date = t2.trx_date
            where (1=1) and t1.garage_code = t2.garage_code) t5 join garage on t5.garage_code = garage.garage_code
            ) t6 left join (SELECT count(*) as settlement_diff ,date_format(txn_datetime, '%Y%m%d') as txn_d FROM parking WHERE settlement_type <> 0 group by date_format(txn_datetime, '%Y%m%d')) t7 on t6.format_date = t7.txn_d
        """

            if query['garage_code'] == '':
                sql = sql +"""
                left join (SELECT garage_code as g, trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY g,trx_date ) t8 on (t8.trxdate_calstatus_c = t6.format_date and  t8.g= t6.garage_code)
                left join (
                    SELECT garage_code as g, trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee from (
						select * FROM trx_data WHERE cal_status =  'F' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name
						union all 
						SELECT * FROM trx_data WHERE cal_status =  'E' and (cal_err_code = '8' or cal_err_code = '4') and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name
					)a  GROUP BY g,trx_date
                ) t9 on (t9.trxdate_calstatus_f = t6.format_date and t9.g= t6.garage_code)
                left join (SELECT garage_code as g, trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and cal_err_code != '8' and cal_err_code != '4' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP  BY g,trx_date ) t10 on (t10.trxdate_calstatus_e = t6.format_date and t10.g= t6.garage_code)
                where 1 =1
                """
            else :
                sql = sql +"""
                left join (SELECT trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY trx_date ) t8 on t8.trxdate_calstatus_c = t6.format_date
                left join (
                    SELECT trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee from
                    (
                    SELECT *
                    FROM trx_data WHERE cal_status =  'F' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') 
                    and file_name LIKE :file_name 
                    union all
                    SELECT * FROM trx_data WHERE cal_status =  'E' 
                    and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name and (cal_err_code = '8' or cal_err_code = '4')
                    ) a GROUP BY trx_date 
                ) t9 on t9.trxdate_calstatus_f = t6.format_date
                left join (SELECT trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and cal_err_code != '8' and cal_err_code != '4' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY trx_date ) t10 on t10.trxdate_calstatus_e = t6.format_date
                where 1 =1
                """
        
        elif query['paid_type'] == '05':
            """ happycash card """
            sql = """
            select garage_code,garage_name,format_date,pms_cnt,pms_fee,cps_cnt,cps_fee,cal_f_totalfee,cal_e_totalfee,cal_c_totalfee,pms_cps_data_diff,pms_cps_diff,settlement_diff from (
            select t5.paid_type,t5.cps_cnt,t5.cps_fee,t5.format_date,t5.pms_cnt,t5.pms_fee,t5.garage_code,(t5.pms_cnt-t5.cps_cnt) pms_cps_data_diff
            ,(t5.pms_fee-t5.cps_fee) pms_cps_diff, garage.garage_name from (
            select t1.paid_type,t1.garage_code,t1.format_date, t1.pms_cnt, t1.pms_fee, IF(t2.cps_cnt IS NULL, 0, t2.cps_cnt) as cps_cnt
            , IF(t2.cps_fee IS NULL, 0, t2.cps_fee) as cps_fee
            from (
            select paid_type,garage_code,count(*) as pms_cnt, sum(real_fee) as pms_fee, date_format(exit_time, '%Y%m%d') as format_date
            from parking where paid_type = :paid_type and settlement_type = 0 and exit_time != '0000-00-00 00:00:00'
            group by paid_type,garage_code,date_format(exit_time, '%Y%m%d')
            ) as t1

            left join (
            select garage_code,count(*) as cps_cnt, COALESCE(sum(trx_amt), 0) as cps_fee
            ,trx_date from trx_data where file_name like :file_name and trx_type not in ('00','03','42','90','0')  group by garage_code,trx_date) as t2 on t1.format_date = t2.trx_date
            where (1=1) and t1.garage_code = t2.garage_code) t5 join garage on t5.garage_code = garage.garage_code
            ) t6 left join (SELECT count(*) as settlement_diff ,date_format(txn_datetime, '%Y%m%d') as txn_d FROM parking WHERE settlement_type <> 0 group by date_format(txn_datetime, '%Y%m%d')) t7 on t6.format_date = t7.txn_d
        """

            if query['garage_code'] == '':
                sql = sql +"""
                left join (SELECT garage_code as g, trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY g,trx_date ) t8 on (t8.trxdate_calstatus_c = t6.format_date and  t8.g= t6.garage_code)
                left join (
                    SELECT garage_code as g, trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee from (
						select * FROM trx_data WHERE cal_status =  'F' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name
						union all 
						SELECT * FROM trx_data WHERE cal_status =  'E' and (cal_err_code = '8' or cal_err_code = '4') and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name
					)a  GROUP BY g,trx_date
                ) t9 on (t9.trxdate_calstatus_f = t6.format_date and t9.g= t6.garage_code)
                left join (SELECT garage_code as g, trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and cal_err_code != '8' and cal_err_code != '4' and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP  BY g,trx_date ) t10 on (t10.trxdate_calstatus_e = t6.format_date and t10.g= t6.garage_code)
                where 1 =1
                """
            else :
                sql = sql +"""
                left join (SELECT trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY trx_date ) t8 on t8.trxdate_calstatus_c = t6.format_date
                left join (
                    SELECT trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee from
                    (
                    SELECT *
                    FROM trx_data WHERE cal_status =  'F' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') 
                    and file_name LIKE :file_name 
                    union all
                    SELECT * FROM trx_data WHERE cal_status =  'E' 
                    and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name and (cal_err_code = '8' or cal_err_code = '4')
                    ) a GROUP BY trx_date 
                ) t9 on t9.trxdate_calstatus_f = t6.format_date
                left join (SELECT trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and cal_err_code != '8' and cal_err_code != '4' and garage_code = :garage_code and trx_type not in ('00','03','42','90','0') and file_name LIKE :file_name GROUP BY trx_date ) t10 on t10.trxdate_calstatus_e = t6.format_date
                where 1 =1
                """


        sql = sql + " and format_date <= :end_date" if query['end_date'] else sql
        sql = sql + " and format_date >= :start_date" if query['start_date'] else sql
        sql = sql + " and garage_code = :garage_code " if query['garage_code'] else sql
        sql = sql + " order by format_date desc"

        if query['file_name'] == '':
            fileName = self._csv_file_names[query['paid_type']]
        else:
            fileName = query['file_name']
        parameneters = {
            'paid_type': query['paid_type'],
            'file_name': fileName,
            'end_date' : query['end_date'],
            'start_date' :query['start_date'],
            'garage_code' : query['garage_code']
        }
        async with self._db.acquire() as conn:
            sql = text(sql)
            print(sql)
            result = [dict(row.items()) async for row in await conn.execute(sql,parameneters)]
            return result

    async def accounting_daily(self,query):
        if query['paid_type'] == '01':
            """ yoyo card """
            sql = """
        select * from (
        select t5.paid_type,t5.cps_cnt,t5.cps_fee,t5.format_date,t5.pms_cnt,t5.pms_fee,t5.garage_code,(t5.pms_cnt-t5.cps_cnt) pms_cps_data_diff
        ,(t5.pms_fee-t5.cps_fee) pms_cps_diff, garage.garage_name from (
        select t1.paid_type,t1.garage_code,t1.format_date, t1.pms_cnt, t1.pms_fee, IF(t2.cps_cnt IS NULL, 0, t2.cps_cnt) as cps_cnt
, IF(t2.cps_fee IS NULL, 0, t2.cps_fee) as cps_fee
from (
select paid_type,garage_code,count(*) as pms_cnt, sum(real_fee) as pms_fee, date_format(exit_time, '%Y%m%d') as format_date
from parking where paid_type = :paid_type and settlement_type = 0 and exit_time != '0000-00-00 00:00:00'
group by paid_type,garage_code,date_format(exit_time, '%Y%m%d')
) as t1

left join (
select garage_code,count(*) as cps_cnt, COALESCE(sum(trx_amt), 0) as cps_fee
,trx_date from trx_data where file_name like :file_name group by garage_code,trx_date) as t2 on t1.format_date = t2.trx_date
where (1=1) and t1.garage_code = t2.garage_code) t5 join garage on t5.garage_code = garage.garage_code
) t6 left join (SELECT count(*) as settlement_diff ,date_format(txn_datetime, '%Y%m%d') as txn_d FROM parking WHERE settlement_type <> 0 group by date_format(txn_datetime, '%Y%m%d')) t7 on t6.format_date = t7.txn_d
left join (SELECT trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and trx_type = '1' and file_name LIKE :file_name and garage_code = :garage_code  GROUP BY trx_date ) t8 on t8.trxdate_calstatus_c = t6.format_date
left join (SELECT trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee FROM trx_data WHERE cal_status =  'F' and trx_type = '1' and file_name LIKE :file_name and garage_code = :garage_code GROUP BY trx_date ) t9 on t9.trxdate_calstatus_f = t6.format_date
left join (SELECT trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and trx_type = '1' and file_name LIKE :file_name and garage_code = :garage_code GROUP BY trx_date ) t10 on t10.trxdate_calstatus_e = t6.format_date
where 1 =1
"""
        else:
            """ ipass card """
            sql = """
        select * from (
        select t5.paid_type,t5.cps_cnt,t5.cps_fee,t5.format_date,t5.pms_cnt,t5.pms_fee,t5.garage_code,(t5.pms_cnt-t5.cps_cnt) pms_cps_data_diff
        ,(t5.pms_fee-t5.cps_fee) pms_cps_diff, garage.garage_name from (
        select t1.paid_type,t1.garage_code,t1.format_date, t1.pms_cnt, t1.pms_fee, IF(t2.cps_cnt IS NULL, 0, t2.cps_cnt) as cps_cnt
, IF(t2.cps_fee IS NULL, 0, t2.cps_fee) as cps_fee
from (
select paid_type,garage_code,count(*) as pms_cnt, sum(real_fee) as pms_fee, date_format(exit_time, '%Y%m%d') as format_date
from parking where paid_type = :paid_type and settlement_type = 0 and exit_time != '0000-00-00 00:00:00'
group by paid_type,garage_code,date_format(exit_time, '%Y%m%d')
) as t1

left join (
select garage_code,count(*) as cps_cnt, COALESCE(sum(trx_amt), 0) as cps_fee
,trx_date from trx_data where file_name like :file_name and trx_type not in ('00','03','42','90','0') group by garage_code,trx_date) as t2 on t1.format_date = t2.trx_date
where (1=1) and t1.garage_code = t2.garage_code) t5 join garage on t5.garage_code = garage.garage_code
) t6 left join (SELECT count(*) as settlement_diff ,date_format(txn_datetime, '%Y%m%d') as txn_d FROM parking WHERE settlement_type <> 0 group by date_format(txn_datetime, '%Y%m%d')) t7 on t6.format_date = t7.txn_d
left join (SELECT trx_date AS trxdate_calstatus_c,SUM( trx_amt ) AS cal_c_totalfee FROM trx_data WHERE cal_status =  'C' and garage_code = :garage_code and trx_type not in ('00','03','42','90' ,'0') and file_name LIKE :file_name GROUP BY trx_date ) t8 on t8.trxdate_calstatus_c = t6.format_date
left join (SELECT trx_date AS trxdate_calstatus_f,SUM( trx_amt ) AS cal_f_totalfee FROM trx_data WHERE cal_status =  'F' and garage_code = :garage_code and trx_type not in ('00','03','42','90' ,'0') and file_name LIKE :file_name GROUP BY trx_date ) t9 on t9.trxdate_calstatus_f = t6.format_date
left join (SELECT trx_date AS trxdate_calstatus_e,SUM( trx_amt ) AS cal_e_totalfee FROM trx_data WHERE cal_status =  'E' and garage_code = :garage_code and trx_type not in ('00','03','42','90' ,'0') and file_name LIKE :file_name GROUP BY trx_date ) t10 on t10.trxdate_calstatus_e = t6.format_date
where 1 =1
"""

        sql = sql + " and format_date <= :end_date" if query['end_date'] else sql
        sql = sql + " and format_date >= :start_date" if query['start_date'] else sql
        sql = sql + " and format_date = :format_date" if query['exit_date_formatted'] else sql
        sql = sql + " and garage_code = :garage_code " if query['garage_code'] else sql
        sql = sql + " order by format_date desc"

        if query['file_name'] == '':
            fileName = self._csv_file_names[query['paid_type']]
        else:
            fileName = query['file_name']
        parameneters = {
            'paid_type': query['paid_type'],
            'file_name': fileName,
            'end_date' : query['end_date'],
            'start_date' :query['start_date'],
            'garage_code' : query['garage_code']
        }
        async with self._db.acquire() as conn:
            sql = text(sql)
            print(sql)
            result = [dict(row.items()) async for row in await conn.execute(sql,parameneters)]
            return result

    async def accounting_parse(self,location) -> dict:
        parser = CsvParser(location)
        csvCollection=parser.read_files_in_directory()
        """ parse the csv file into database """
        trx = []
        for key in csvCollection:
            #print(key)
            parsed = key.split('/')[-1].split('-')
            garage_code = parsed[0]
            csv_file_date = parsed[-1].rstrip('.csv')

            if 'cps.trx_data' in key:
                d= csvCollection[key].split('\r\n')
                for dd in d:
                    data= self.convertToList(dd,key,garage_code,csv_file_date)
                    #async with self._db.acquire() as conn:
                    #    if data is not None:
                    #        rz =  await conn.execute(Trx_Data.insert().values(data))
            if 'pms.parking' in key:
                d= csvCollection[key].split('\r\n')
                for dd in d:
                    data= self.convertToList(dd,key,garage_code,csv_file_date)
                    #async with self._db.acquire() as conn:
                    #    if data is not None:
                    #        rz =  await conn.execute(Parking.insert().values(data))

        parser.move_files_to_bakcup_directory()
        return csvCollection

    def convertToList(self,row:str, filename:str, garage_code:str, csv_file_date:str):
        k = []
        w= row.split(',')

        if len(w) < 3:
            return None

        w.append(filename)
        w.append(garage_code)
        w.append(csv_file_date)
        return w
