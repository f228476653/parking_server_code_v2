from pprint import pprint
import json,os,time,xlrd,logging,ftplib
from xlrd import open_workbook
from datetime import datetime, timedelta
from app.config.models import Account
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
from sqlalchemy import text
from sqlalchemy.sql import select
from app.config.models import Customer,Garage,Commutation_Ticket_Order,Commutation_Ticket_Config,Commutation_Ticket_Period_Config
import re

class CommutationTicketService:
    """ parse ticket.xls data into DB,then create insert sql by garage and deliver to garage """
    _db =None
    _log_service = None
    _syslog = None
    _excel_path = None
    _user_insert = []
    _user_edit = []
    _user_disabled = []
    _type_insert = []
    _type_edit =[]
    _type_disabled = []
    _execute_time = datetime.utcnow()
    _ftp_target_folder = '/commutation_ticket'
    #pv用卡號當key,日期分平日/假日;pv3用卡號當key,日期分星期一到日;pad:用車號當key，日期分平日/假日
    _pv_type = None

    #config應該不用garage_id
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        #self._excel_path =os.path.join((os.path.dirname(__file__)).split('app')[0], 'dir/commutation_ticket')

    #1
    async def update_commutation_ticket(self,excel_path,execute_id):
        """ check if input file exist and whether update """
        pattern ="^\w+[-]\w+[-]\d+[-]\w+.xlsx$"
        self._execute_id = execute_id
        self._read_path = os.path.join((os.path.dirname(__file__)).split('app')[0], excel_path)
        path_list = {}
        try:
            customer_code = excel_path.split('/')[2]
            async with self._db.acquire() as conn:
                customer_id = await(await conn.execute(select([Customer.c.customer_id]).where(Customer.c.customer_code==customer_code))).scalar()
            if customer_id == None:
                self._syslog['create_account_id']=0
                self._syslog['event_id']=349
                self._syslog['event_message']=f'update_commutation_ticket : time= {self._execute_time},can not find customer_id by customer_code :{customer_code}'
                result = await self._log_service.addlog(self._syslog)
                return False
            #print(f"now data ---{self._execute_time}")
            for f in os.listdir(self._read_path):
                if re.match(pattern,f):
                    #print(f"%^_)_{(f.split('-')[3]).split('.')[0]=='pv'}")
                    await self.compare_new_and_current_data(os.path.join(self._read_path,f), customer_id)
                    if str((f.split('-')[3]).split('.')[0]) =='pv':
                        #print('pv')
                        path_list = await self.generate_sql_file_by_customer_garage_id(customer_id, (f.split('-')[3]).split('.')[0] ,excel_path)
                        await self.deliver_data(path_list)
                    if (f.split('-')[3]).split('.')[0] =='pv3' or (f.split('-')[3]).split('.')[0] =='pad':
                        path_list = await self.generate_dat_file_by_customer_garage_id(customer_id, (f.split('-')[3]).split('.')[0] ,excel_path)
        except Exception as e:
            self._syslog['create_account_id']=0
            self._syslog['event_id']=656
            self._syslog['event_message']=f'update_commutation_ticket,Error:{e}  '
            result = await self._log_service.addlog(self._syslog)
            return False
        return True

    async def deliver_data(self,path_list):
        print(f"path_list---------------{path_list}")
        for file in path_list:
            ftp_info = await self.get_garage_ftp_info_by_customer_garage_id(file['customer_garage_id'])
            print(f"ftp_info---------------{ftp_info}")
            if ftp_info is None or len(ftp_info) ==0 :
                pass
            await self.send_files_by_ftp(ftp_info[0]['ftp_ip'],ftp_info[0]['ftp_port'],ftp_info[0]['ftp_userid'],ftp_info[0]['ftp_pwd'],self._ftp_target_folder,'commutation_ticket.sql',file['generate_path'])

    def read_excel(self,sheet_name,fileadd):
        wb = open_workbook(fileadd)
        sheet = wb.sheet_by_name(sheet_name)
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        items = []
        for row in range(1, number_of_rows):
            values = []
            for col in range(number_of_columns):
                value  = self.check_excel_data(sheet.cell(row, col),wb)
                try:
                    value = str(value)
                except ValueError as e:
                    print(e)
                finally:
                    values.append(value)
            items.append(values)
        return items
    
    async def get_current_commutation_tickets(self,sheet_name, customer_id:str):
        #以customer為單位
        if sheet_name == 'ticket_user':
            current_stmt= """select o.vehicle_plate_number,o.card_id16, c.commutation_ticket_config_name ,o.begin_date,
                                    o.end_date,g.customer_garage_id ,o.telephone,o.cellphone,o.buyer_name, o.create_date,o.end_date,g.customer_garage_id
                                    from commutation_ticket_order o
                                        left join  garage g
                                            on o.customer_garage_id = g.customer_garage_id
                                        left join commutation_ticket_config c
                                            on c.commutation_ticket_config_id = o.commutation_ticket_config_id
                                    where o.customer_id = :customer_id"""
            
        if sheet_name == 'ticket_type':
            current_stmt= """select c.commutation_ticket_config_name,p.days_of_the_week,substring(p.time_begin1,1,2),substring(p.time_begin1,3,2),
                                substring(p.time_end1,1,2),substring(p.time_end1,3,2),substring(p.time_begin2,1,2),substring(p.time_begin2,3,2),substring(p.time_end2,1,2),substring(p.time_end2,3,2)
                                ,c.unit_sales,c.sales_num,c.vehicle_type,c.pay_amount
                            from commutation_ticket_config c
                            left join commutation_ticket_period_config p on c.commutation_ticket_config_id = p.commutation_ticket_config_id where c.customer_id = :customer_id
                            """
        async with self._db.acquire() as conn:
            result = await conn.execute(text(current_stmt),{'customer_id' : customer_id})
            result = list(await result.fetchall())
            return result
    #2
    async def compare_new_and_current_data(self,filename:str, customer_id:str):
        """票種不分場站以業者為主"""
        new_ticket_user_data = self.read_excel('ticket_user',filename)
        new_ticket_type_data =self.read_excel('ticket_type',filename)
        current_ticket_user_data =await self.get_current_commutation_tickets('ticket_user',customer_id)
        current_ticket_type_data =await self.get_current_commutation_tickets('ticket_type',customer_id)
        
        async with self._db.acquire() as conn:   
            disable_sql = """
            update commutation_ticket_period_config set is_active = 0 ,update_date =:update_date where commutation_ticket_config_id in (select commutation_ticket_config_id from commutation_ticket_config where customer_id =:customer_id);
            update commutation_ticket_order set is_active = 0 ,update_date =:update_date where customer_id =:customer_id;
            update commutation_ticket_config set is_active = 0,update_date =:update_date  where customer_id =:customer_id;
            """
            await conn.execute(text(disable_sql),{'customer_id': customer_id ,'update_date': self._execute_time})

            for i in range(len(new_ticket_type_data)) :
                ticket_config=None
                ticket_period_config=None
                ticket_config={
                    'commutation_ticket_config_name': new_ticket_type_data[i][0],
                    'customer_id': customer_id,
                    'unit_sales': new_ticket_type_data[i][2],
                    'sales_num': new_ticket_type_data[i][3],
                    'pay_amount': new_ticket_type_data[i][4],
                    'vehicle_type': new_ticket_type_data[i][1],
                    'is_active':1
                }
                
                ticket_period_config={
                    'days_of_the_week': new_ticket_type_data[i][5],
                    'time_begin1': self.prepend_zero(new_ticket_type_data[i][6])+':'+self.prepend_zero(new_ticket_type_data[i][7]),
                    'time_end1':   self.prepend_zero(new_ticket_type_data[i][8])+':'+self.prepend_zero(new_ticket_type_data[i][9]),
                    'time_begin2': "00:00" if new_ticket_type_data[i][10]=='' else (self.prepend_zero(new_ticket_type_data[i][10]) + ':' + self.prepend_zero(new_ticket_type_data[i][11])),
                    'time_end2': "00:00" if new_ticket_type_data[i][12]=='' else (self.prepend_zero(new_ticket_type_data[i][12]) + ':' + self.prepend_zero(new_ticket_type_data[i][13])),
                    'is_active':1
                }

                ticket_config['create_date']= self._execute_time
                if not await self.is_commutation_ticket_config_exist(ticket_config['commutation_ticket_config_name'],ticket_config['customer_id']):
                    await conn.execute(Commutation_Ticket_Config.insert().values(ticket_config))
                r = await self.get_commutation_ticket_config_id(ticket_config['commutation_ticket_config_name'],customer_id)
                ticket_period_config['commutation_ticket_config_id']=r[0]['commutation_ticket_config_id']
                await self.add_commutation_ticket_period_config(ticket_period_config)
                # 為了保留完整紀錄所以不update
                # 採全部inactive 再把收到的全部ＥＸＣＥＬ資料新增
                # print(type(ticket_period_config))
                # if await self.is_commutation_ticket_type_exist(current_ticket_type_data, new_ticket_type_data[i]) :
                    #todo select id where clause commutation_ticket_config_name /customer_id /isactive
                    # #update ticket_period_config where clause id
                    # ticket_period_config['update_date']= self._execute_time
                    # ticket_config['update_date']= self._execute_time
                    # r = await self.get_commutation_ticket_config_id(new_ticket_type_data[i][0],customer_id)
                    # ticket_period_config['commutation_ticket_config_id']=r[0]['commutation_ticket_config_id']
                    # 為了保留完整紀錄所以不update
                    # await conn.execute(Commutation_Ticket_Config.update().values(ticket_config).where(Commutation_Ticket_Config.c.commutation_ticket_config_name == ticket_config['commutation_ticket_config_name']).where(Commutation_Ticket_Config.c.customer_id == ticket_config['customer_id']) )
                    # await conn.execute(Commutation_Ticket_Period_Config.update().values(ticket_period_config).where(Commutation_Ticket_Period_Config.c.commutation_ticket_config_id==ticket_period_config['commutation_ticket_config_id']).where(Commutation_Ticket_Period_Config.c.days_of_the_week==new_ticket_type_data[i][5]))
                    
                    #print(f'-------ticket_period_config------{ticket_period_config}')
                    #print(f'--------------{ticket_config}')
                    # await conn.execute(text(f"update commutation_ticket_config set is_active='1',update_date='{self._execute_time}' where commutation_ticket_config_name =:commutation_ticket_config_name and customer_id =:customer_id"),ticket_config)
                    #await conn.execute(Commutation_Ticket_Config.update().values(ticket_config).where(Commutation_Ticket_Config.c.commutation_ticket_config_name ==current_ticket_type_data[i][1]).where(Commutation_Ticket_Config.c.customer_id==customer_id))
                # else:
                    # print('type_not_same')
                    # ticket_config['create_date']= self._execute_time
                    # if not await self.is_commutation_ticket_config_exist(ticket_config['commutation_ticket_config_name'],ticket_config['customer_id']):
                    #     await conn.execute(Commutation_Ticket_Config.insert().values(ticket_config))

                    # r = await self.get_commutation_ticket_config_id(ticket_config['commutation_ticket_config_name'],customer_id)
                    # ticket_period_config['commutation_ticket_config_id']=r[0]['commutation_ticket_config_id']
                    # await self.add_commutation_ticket_period_config(ticket_period_config)
                    
            """insert user :get user data in excel but not in DB ; update user :compare key ,if same update all data except key from excel"""
            for i in range(len(new_ticket_user_data)) :
                customer_garage_id = new_ticket_user_data[i][5]
                commutation_config_name = new_ticket_user_data[i][2]
                #print(f'--{new_ticket_user_data[i][0]}')
                #print(f'--{new_ticket_user_data[i][1]}')
                #print(f'--{new_ticket_user_data[i][2]}')
                #print(f'--{new_ticket_user_data[i][3]}')
                #print(f'--{new_ticket_user_data[i][4]}')
                #print(f'--{new_ticket_user_data[i][5]}')
                garages = await self.get_garage_by_customer_garage_id(customer_garage_id)

                if garages is None or len(garages)==0:
                    raise Exception(f'can not find garage by customer_garage_id {new_ticket_user_data[i][5]}') 
                else:
                    garages = garages[0]['garage_id']

                r = await self.get_commutation_ticket_config_id(commutation_config_name,customer_id,1)
                user_data = None
                user_data = {
                    'vehicle_plate_number': new_ticket_user_data[i][0],
                    'card_id16': new_ticket_user_data[i][1],
                    'commutation_ticket_config_id': r[0]['commutation_ticket_config_id'],
                    'begin_date': new_ticket_user_data[i][3],
                    'end_date': new_ticket_user_data[i][4],
                    'customer_garage_id': customer_garage_id, #這裡是customer 自己定義的id
                    'garage_id': garages,
                    'telephone': new_ticket_user_data[i][6],
                    'cellphone': new_ticket_user_data[i][7],
                    'buyer_name': new_ticket_user_data[i][8],
                    'customer_id': customer_id,
                    'is_active':1
                }
                
                # if await self.is_to_update_commutation_ticket_order(current_ticket_user_data,new_ticket_user_data[i][1],commutation_config_name,customer_garage_id):
                #     user_data['update_date']=self._execute_time
                #     #print(f'------------order same---------------{user_data}')
                #     await conn.execute(Commutation_Ticket_Order.update().values(user_data).where(Commutation_Ticket_Order.c.card_id16==new_ticket_user_data[i][1]).where(Commutation_Ticket_Order.c.commutation_ticket_config_id==r[0]['commutation_ticket_config_id']).where(Commutation_Ticket_Order.c.customer_garage_id==customer_garage_id))
                # else :
                    # user_data['create_date']=self._execute_time
                    # await conn.execute(Commutation_Ticket_Order.insert().values(user_data))
                user_data['create_date']=self._execute_time
                await conn.execute(Commutation_Ticket_Order.insert().values(user_data))

    async def get_commutation_ticket_config_id(self,commutation_ticket_config_name:str, customer_id:str, is_active=1):
        async with self._db.acquire() as conn:
            sql = """select commutation_ticket_config_id from 
            commutation_ticket_config 
            where 
            commutation_ticket_config_name =:commutation_ticket_config_name and customer_id =:customer_id and is_active =:is_active
            """
            #already inactive so dont use is_active 
            condition = {
                'commutation_ticket_config_name':commutation_ticket_config_name,
                'customer_id': customer_id,
                'is_active': is_active
            }
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return result

    # async def is_to_update_commutation_ticket_order(self,current_ticket_user_data, card_id16,commutation_ticket_config_name,customer_garage_id):
    #     is_equal = False
    #     for k in range(len(current_ticket_user_data)) :
    #         #print(f'------1----{card_id16}')
    #         #print(f'------1----{current_ticket_user_data[k][1]}')
    #         #print(f'------2----{commutation_ticket_config_name}')
    #         #print(f'------2----{current_ticket_user_data[k][2]}')
    #         #print(f'------5----{customer_garage_id}')
    #         #print(f'------5----{current_ticket_user_data[k][5]}')
    #         #卡號、票種、部門編號
    #         if card_id16.strip() == current_ticket_user_data[k][1].strip()  and commutation_ticket_config_name.strip() == current_ticket_user_data[k][2].strip() and customer_garage_id.strip() == current_ticket_user_data[k][5].strip():
    #             #print(f'======order true---------')
    #             is_equal = True
    #             break
    #     return is_equal

    async def get_garage_by_customer_garage_id(self,customer_garage_id):
        async with self._db.acquire() as conn:
            sql = """ select * from garage where customer_garage_id =:customer_garage_id"""
            condition = {
                "customer_garage_id": customer_garage_id
            }
            return [dict(row.items()) async for row in await conn.execute(text(sql),condition)]

    async def is_commutation_ticket_config_exist(self,commutation_ticket_config_name:str,customer_id:str,is_active=1):
        async with self._db.acquire() as conn:
            sql = """ select * from commutation_ticket_config where commutation_ticket_config_name =:commutation_ticket_config_name and customer_id =:customer_id and is_active=:is_active"""
            condition = {
                "commutation_ticket_config_name": commutation_ticket_config_name,
                "customer_id": customer_id,
                "is_active":is_active
            }
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            #print(result)
            return len(result) >0 and True or False

    # async def is_commutation_ticket_type_exist(self,current_ticket_type_data, new_ticket_type):
    #     is_exist = False
    #     #print('---------------')
    #     for k in range(len(current_ticket_type_data)) :
    #         #print(f'{str(new_ticket_type[1])}----{str(current_ticket_type_data[k][1])}')
    #         #print(f'{str(new_ticket_type[0])}----{str(current_ticket_type_data[k][0])}')
    #         #print(f'--------------------------')
    #         #比對  星期 票種
    #         if str(new_ticket_type[5]) == str(current_ticket_type_data[k][1]) and str(new_ticket_type[0]) == str(current_ticket_type_data[k][0]):
    #             is_exist = True
    #             #print(is_exist)
    #             break
    #     return is_exist

    async def add_commutation_ticket_period_config(self,ticket_period_config):
        async with self._db.acquire() as conn:
            await conn.execute(Commutation_Ticket_Period_Config.insert().values(ticket_period_config))

    async def deliver_to_garage(self,customer_id):
        ##抓參數檔案
        garages_data = await self.get_garage_by_customer_id(customer_id)
        for garage in garages_data:
            await genreate_sql_by_garage_id(garage['garage_code'])

    #3
    async def generate_dat_file_by_customer_garage_id(self,customer_id, device_type:str, execel_path:str) -> []:
        # pv3、產生dat
        # pad /usr/share/nginx/html/pad-files/customer_id/garage_id
        garage_code_list =  await self.get_garage_by_customer_id(customer_id)
        path_list = []
        for g in garage_code_list:
            generate_dir = os.path.join(self._read_path, "generate_dat", g['customer_garage_id'])
            generate_path = os.path.join(self._read_path, "generate_dat", g['customer_garage_id'], "commutation_ticket.dat")
            self.mkdirs(generate_dir)
            data = await self.get_dat_data(device_type, g['customer_garage_id'])
            try:
                os.remove(generate_path)
            except OSError:
                pass
            
            path_list.append(
                {
                    'dir':execel_path+'/'+'generate_dat'+'/'+ g['customer_garage_id']+'/'+'commutation_ticket.dat',
                    'generate_path':generate_path,
                    'customer_garage_id':g['customer_garage_id']
                }
            )

            with open (generate_path,"a") as w:
                for aa in data:
                    w.write(','.join("{!s}".format(val) for (key,val) in aa.items())+'\n')
            print(path_list)    
            return path_list

    async def generate_sql_file_by_customer_garage_id(self,customer_id, device_type:str, execel_path:str) -> []:
        # pv傳到場站
        # pad /usr/share/nginx/html/pad-files/customer_id/garage_id
        garage_code_list =  await self.get_garage_by_customer_id(customer_id)
        truncate_sql = "truncate `commutation_ticket_order`; truncate `commutation_ticket_vehicle_data`; truncate `commutation_ticket_rule`;\n "
        ticket_order_sqlScript = "INSERT INTO `commutation_ticket_order` (card_id16,ticket_rule,begin_date,end_date,sale_amount,create_time,create_user) VALUES ('"
        ticket_vehicle_sqlScript = "INSERT INTO `commutation_ticket_vehicle_data` (owner_name,vehicle_no,vehicle_color,telephone,cellphone,email,create_user,card_id16 ) VALUES ('"
        ticket_rule_sqlScript ="insert into `commutation_ticket_rule` (no,name,use_unit_type,use_nums,pay_amount,vehicle_type,weekday_begin1,weekday_mins_begin1,weekday_end1,weekday_mins_end1,weekday_begin2,weekday_mins_begin2,weekday_end2,weekday_mins_end2,weekend_begin1,weekend_mins_begin1,weekend_end1,weekend_mins_end1,weekend_begin2,weekend_mins_begin2,weekend_end2,weekend_mins_end2,create_time) VALUES ('"
        path_list = []
        print(garage_code_list)
        for g in garage_code_list:
            generate_dir = os.path.join(self._read_path, "generate_sql", g['customer_garage_id'])
            generate_path = os.path.join(self._read_path, "generate_sql", g['customer_garage_id'], "commutation_ticket.sql")
            print(generate_path)
            self.mkdirs(generate_dir)
            data = await self.get_sql_data(device_type, g['customer_garage_id'])
            try:
                os.remove(generate_path)
            except OSError:
                pass
            
            path_list.append(
                {
                    'dir':execel_path+'/'+'generate_sql'+'/'+ g['customer_garage_id']+'/'+'commutation_ticket.sql',
                    'generate_path':generate_path,
                    'customer_garage_id':g['customer_garage_id']
                }
            )

            with open (generate_path,"a") as w:
                w.write(truncate_sql)
                for aa in data.get('commutation_ticket_order'):
                    w.write(ticket_order_sqlScript + "','".join("{!s}".format(val) for (key,val) in aa.items())+"'); \n")
                for bb in data.get('commutation_ticket_vehicle_data'):
                    w.write(ticket_vehicle_sqlScript + "','".join("{!s}".format(val) for (key,val) in bb.items())+"'); \n")
                for cc in data.get('commutation_ticket_rule'):
                    w.write(ticket_rule_sqlScript + "','".join("{!s}".format(val) for (key,val) in cc.items())+"'); \n")
            print(path_list)    
        return path_list

    def prepend_zero(self,to_prepend:str):
        if len(to_prepend) == 1:
            to_prepend= '0'+to_prepend
        
        return to_prepend

    async def get_dat_data(self,device_type:str, customer_garage_id:str):
        """決定要用車牌還是卡號當key"""
        sql = None
        if device_type == 'pv3':
            sql = """
            select o.card_id16,o.begin_date,o.end_date,
                concat(p_sunday.time_begin1,':','00') as p_sunday_begin1,
                 concat(p_sunday.time_end1,':','00') p_sunday_end1,
                concat(p_sunday.time_begin2,':','00') as p_sunday_begin2,
                 concat(p_sunday.time_end2,':','00') as p_sunday_end2,
 		concat(p_monday.time_begin1,':','00') as p_monday_begin1,
                 concat(p_monday.time_end1,':','00') as p_monday_end1,
                concat(p_monday.time_begin2,':','00')as p_monday_begin2,
               concat(p_monday.time_end2,':','00') as p_monday_end2,
		concat(p_tuesday.time_begin1,':','00') as p_tuesday_begin1,
                concat(p_tuesday.time_end1,':','00')as p_tuesday_end1,
                 concat(p_tuesday.time_begin2,':','00') p_tuesday_begin2,
               concat(p_tuesday.time_end2,':','00') p_tuesday_end2,
                concat(p_wednesday.time_begin1,':','00') as p_wednesday_begin1,
                concat(p_wednesday.time_end1,':','00')as p_wednesday_end1,
                concat(p_wednesday.time_begin2,':','00')as p_wednesday_begin2,
                concat(p_wednesday.time_end2,':','00')as p_wednesday_end2,
                concat(p_thursday.time_begin1,':','00')as p_thursday_begin1,
                concat(p_thursday.time_end1,':','00') as p_thursday_end1,
                concat(p_thursday.time_begin2,':','00')as p_thursday_begin2,
                concat(p_thursday.time_end2,':','00')as p_thursday_end2,
		concat(p_friday.time_begin1,':','00')as p_friday_begin1,
                concat(p_friday.time_end1,':','00')as p_friday_end1,
                concat(p_friday.time_begin2,':','00') as p_friday_begin2,
                concat(p_friday.time_end2,':','00')p_friday_end2,
		concat(p_saturday.time_begin1,':','00') as p_saturday_begin1,
                concat(p_saturday.time_end1,':','00') as p_saturday_end1,
                concat(p_saturday.time_begin2,':','00') as p_saturday_begin2,
                concat(p_saturday.time_end2,':','00') as p_saturday_end2,
                
                c.commutation_ticket_config_id
                from commutation_ticket_order o
                left join commutation_ticket_config c
                on c.commutation_ticket_config_id = o.commutation_ticket_config_id
                left join (select * from commutation_ticket_period_config where days_of_the_week = 0) p_sunday
                on p_sunday.commutation_ticket_config_id = c.commutation_ticket_config_id

                left join (select * from commutation_ticket_period_config where days_of_the_week = 1) p_monday
                on p_monday.commutation_ticket_config_id = c.commutation_ticket_config_id

		left join (select * from commutation_ticket_period_config where days_of_the_week = 2) p_tuesday
                on p_tuesday.commutation_ticket_config_id = c.commutation_ticket_config_id

		left join (select * from commutation_ticket_period_config where days_of_the_week = 3) p_wednesday
                on p_wednesday.commutation_ticket_config_id = c.commutation_ticket_config_id

		left join (select * from commutation_ticket_period_config where days_of_the_week = 4) p_thursday
                on p_thursday.commutation_ticket_config_id = c.commutation_ticket_config_id
		
		left join (select * from commutation_ticket_period_config where days_of_the_week = 5) p_friday
                on p_friday.commutation_ticket_config_id = c.commutation_ticket_config_id

		left join (select * from commutation_ticket_period_config where days_of_the_week = 6) p_saturday
                on p_saturday.commutation_ticket_config_id = c.commutation_ticket_config_id

                where o.is_active =1 and o.customer_garage_id =:customer_garage_id
            """
        """pad無卡號，用車號"""
        if device_type == 'pad' :
            sql=""""""
        """PV只有分平日假日時間"""
        if device_type == 'pv':
            sql="""select o.card_id16,o.begin_date,o.end_date,
                (CASE
                    WHEN p_daily.time_begin1 ='0' THEN 0
                    ELSE concat(p_daily.time_begin1,':','00')
                END) as daily_time_begin1,
                (CASE
                    WHEN p_daily.time_end1 ='0' THEN 0
                    ELSE concat(p_daily.time_end1,':','00')
                END) as daily_time_end1,
                (CASE
                    WHEN p_daily.time_begin2 ='0' THEN 0
                    ELSE concat(p_daily.time_begin2,':','00')
                END) as daily_time_begin2,
                (CASE
                    WHEN p_daily.time_end2 ='0' THEN 0
                    ELSE concat(p_daily.time_end2,':','00')
                END) as daily_time_end2,
                (CASE
                    WHEN p_holiday.time_begin1 ='0' THEN 0
                    ELSE concat(p_holiday.time_begin1,':','00')
                END) as holiday_time_begin1,
                (CASE
                    WHEN p_holiday.time_end1 ='0' THEN 0
                    ELSE concat(p_holiday.time_end1,':','00')
                END) as holiday_time_end1,
                (CASE
                    WHEN p_holiday.time_begin2 ='0' THEN 0
                    ELSE concat(p_holiday.time_begin2,':','00')
                END) as holiday_time_begin2,
                (CASE
                    WHEN p_holiday.time_end2 ='0' THEN 0
                    ELSE concat(p_holiday.time_end2,':','00')
                END) as holiday_time_end2,
                c.commutation_ticket_config_id
                from commutation_ticket_order o
                left join commutation_ticket_config c
                on c.commutation_ticket_config_id = o.commutation_ticket_config_id
                left join (select * from commutation_ticket_period_config where days_of_the_week = 6) p_holiday
                on p_holiday.commutation_ticket_config_id = c.commutation_ticket_config_id
                left join (select * from commutation_ticket_period_config where days_of_the_week = 1) p_daily
                on p_daily.commutation_ticket_config_id = c.commutation_ticket_config_id
                where o.is_active =1 and o.customer_garage_id =:customer_garage_id
        """
        async with self._db.acquire() as conn:
            condition = {
                'customer_garage_id': customer_garage_id
            }
            data = [dict(row.items()) async for row in await conn.execute(text(sql), condition)]
            return data

    async def get_sql_data(self,device_type:str, customer_garage_id:str):
        """決定要用車牌還是卡號當key"""
        sql = None
        #print(f'3434----------------{device_type}')
        if device_type == 'pv3':
            sql = ""
        if device_type == 'pv':
            order_sql = """select card_id16,commutation_ticket_config_id,begin_date,end_date,sale_amount,create_date,'acer' from commutation_ticket_order where is_active =1 and customer_garage_id =:customer_garage_id;
            """
            vehicle_data_sql = """select buyer_name,vehicle_plate_number,vehicle_color,telephone,cellphone,email,'acer', card_id16 from commutation_ticket_order where is_active =1 and customer_garage_id =:customer_garage_id;
            """
            rule_sql="""
            select c.commutation_ticket_config_id,c.commutation_ticket_config_name,c.unit_sales,c.sales_num,c.pay_amount,c.vehicle_type,
            substring(p_daily.time_begin1,1,2) as weekday_begin1,
            substring(p_daily.time_begin1,4,2) as weekday_mins_begin1,
            substring(p_daily.time_end1,1,2) as weekday_end1,
            substring(p_daily.time_end1,4,2) as weekday_mins_end1,
            substring(p_daily.time_begin2,1,2) as weekday_begin2,
            substring(p_daily.time_begin2,4,2) as weekday_mins_begin2,
            substring(p_daily.time_end2,1,2) as weekday_end2,
            substring(p_daily.time_end2,4,2) as weekday_mins_end2,
            substring(p_holiday.time_begin1,1,2) as weekend_begin1,
            substring(p_holiday.time_begin1,4,2) as weekend_mins_begin1,
            substring(p_holiday.time_end1,1,2) as weekend_end1,
            substring(p_holiday.time_end1,4,2) as weekend_mins_end1,
            substring(p_holiday.time_begin2,1,2) as weekend_begin2,
            substring(p_holiday.time_begin2,4,2) as weekend_mins_begin2,
            substring(p_holiday.time_end2,1,2) as weekend_end2,
            substring(p_holiday.time_end2,4,2) as weekend_mins_end2,
            c.create_date from commutation_ticket_config c 
            left join (select * from commutation_ticket_period_config where days_of_the_week = 6) p_holiday
                            on p_holiday.commutation_ticket_config_id = c.commutation_ticket_config_id
            left join (select * from commutation_ticket_period_config where days_of_the_week = 1) p_daily
                            on p_daily.commutation_ticket_config_id = c.commutation_ticket_config_id
            where customer_id = (select customer_id from commutation_ticket_order where customer_garage_id =:customer_garage_id limit 1)
            and c.is_active =1 ;
            """
        async with self._db.acquire() as conn:
            condition = {
                'customer_garage_id': customer_garage_id
            }
            #print(sql)
            order_data = [dict(row.items()) async for row in await conn.execute(text(order_sql), condition)]
            vehicle_data = [dict(row.items()) async for row in await conn.execute(text(vehicle_data_sql), condition)]
            rule_data = [dict(row.items()) async for row in await conn.execute(text(rule_sql), condition)]
            #print(f'order_data-----------------{order_data}')
            #print(f'vehicle_data-----------------{vehicle_data}')
            #print(f'rule_data-----------------{rule_data}')
            deliver_content={
                'commutation_ticket_order':order_data,
                'commutation_ticket_vehicle_data':vehicle_data,
                'commutation_ticket_rule':rule_data
            }
            return deliver_content

    def mkdirs(self,path):
        # 判断结果
        if not os.path.exists(path):
            # 建立目錄
            os.makedirs(path)
            # 如果不存在則建立目錄
            return True
        else:
            # 如果目錄存在則不建立
            return False
  
    async def get_garage_by_customer_id(self,customer_id):
        """to know which garage that i hovw to deliver dat"""
        async with self._db.acquire() as conn:
            sql = "select distinct(customer_garage_id) from commutation_ticket_order where customer_id =:customer_id" 
            condition = {'customer_id': customer_id}
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
        return result

    async def get_garage_ftp_info_by_customer_garage_id(self, customer_garage_id:str):
        async with self._db.acquire() as conn:
            sql = "select * from garage_ftp_info where garage_code=:customer_garage_id"
            condition = {
                'customer_garage_id':customer_garage_id
            } 
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
        return result

    def check_excel_data(self,cell,wb) :
        # ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        if cell.ctype == 3:
            value = datetime(*xlrd.xldate_as_tuple(cell.value, wb.datemode)).strftime('%Y-%m-%d')
        elif cell.ctype == 2:
            value = str(cell.value).split('.')[0]
        elif cell.ctype == 0:
            value = ''
        else :
            value = cell.value
            value = value.replace("'","")
        return value
    
    async def send_files_by_ftp(self,ip,port,account,password,target_folder,target_file_name,source_file_full_path):
            ftp_connection = ftplib.FTP()
            ftp_connection.connect(ip,int(port))
            ftp_connection.login(account,password)
            """print(f'single_row 0 is = {single_row[0]}')"""
            ftp_connection.cwd(target_folder)
            ftp_connection.storbinary(f'STOR '+target_file_name, open(source_file_full_path,'rb'))
            ftp_connection.close() 
