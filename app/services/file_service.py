import time, datetime
from app.services.service import Service
from app.services.systemlog_service import SystemlogService
from app.services.user_service import UserService
from app.services.customer_service import CustomerService
from app.services.garage_service import GarageService
from app.services.exit_config_service import ExitConfigService
from app.services.einvoice_config_service import EinvoiceConfigService
from app.services.device_pad_service import DevicePadService
from app.config.models import Account
import os,glob
#import boto3
import operator
from sqlalchemy import desc,text

class FileService(Service):
    """ every thing about file"""
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None

    def __init__(self, db, user: Account):
        #print(request)
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

    async def get_updated_date_by_garage_id(self, customer_id: int ,garage_id: int ,file_server_path):
        user_service = UserService(self._db,self._user)
        customer_service = CustomerService(self._db,self._user)
        garage_service = GarageService(self._db,self._user)
        exit_service = ExitConfigService(self._db)
        einvoice_config_service = EinvoiceConfigService(self._db)
        device_pad_service =  DevicePadService(self._db)
        account_modified_date= await user_service.get_account_latest_update_date_by_garage_id(garage_id)
        customer_modified_date= await customer_service.get_customer_latest_update_date_by_customer_id(customer_id)
        garage_modified_date= await garage_service.get_garage_latest_update_date_by_garage_id(garage_id)
        garage_args_modified_date= await garage_service.get_garage_pad_args_last_update(garage_id)
        exit_config_modified_date= await exit_service.get_exit_config_detail_last_update(garage_id)
        einvoice_config_modified_date= await einvoice_config_service.get_last_update_einvoice_config(garage_id)
        device_pad_modified_date=  await device_pad_service.get_last_update_device_pad(garage_id)
        update_status = {
            'costrule-sedan' :{
                'file_name':'costrule_file-sedan',
                'url':f'{file_server_path}/pad_files/{customer_id}/{garage_id}/costrule.properties-sedan',
                'updated_date':int(self.get_file_update_date(customer_id,garage_id,'costrule.properties-sedan'))
            },
            'costrule-suv' :{
                'file_name':'costrule_file-suv',
                'url':f'{file_server_path}/pad_files/{customer_id}/{garage_id}/costrule.properties-suv',
                'updated_date':int(self.get_file_update_date(customer_id,garage_id,'costrule.properties-suv'))
            },

            'commutation_ticket' : {
                'file_name':'commutation_ticket',
                'url':f'{file_server_path}/pad_files/{customer_id}/{garage_id}/commutation_ticket.dat',
                'updated_date':int(self.get_file_update_date(customer_id,garage_id,'commutation_ticket.dat'))
            },

            'account' : {
                'file_name':'api',
                'url':'/account/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(account_modified_date, "%Y-%m-%d %H:%M:%S").timetuple())
            },

            'parking_fee_calculator' : {
                'file_name':'ParkingFeeCalculator.jar',
                'url':f'{file_server_path}/pad_files/{customer_id}/{garage_id}/ParkingFeeCalculator.jar',
                'updated_date':int(self.get_file_update_date(customer_id,garage_id,'ParkingFeeCalculator.jar'))
            },
            
            'customer' : {
                'file_name':'api',
                'url':'/customers/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(customer_modified_date, "%Y-%m-%d %H:%M:%S").timetuple())
            },

            'garage': {
                'file_name':'api',
                'url':'/garage/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(garage_modified_date, "%Y-%m-%d %H:%M:%S").timetuple())
            },

            'cartype_discount': {
                'file_name':'cartype_discount.dat',
                'url':f'{file_server_path}/pad_files/{customer_id}/{garage_id}/cardtype_discount.dat',
                'updated_date':int(self.get_file_update_date(customer_id,garage_id,'cardtype_discount.dat'))
            },

            'holiday': {
                'file_name':'holiday.dat',
                'url':f'{file_server_path}/pad_files/{customer_id}/{garage_id}/holiday.dat',
                'updated_date':int(self.get_file_update_date(customer_id,garage_id,'holiday.dat'))
            },

            'exit_config_detail': {
                'file_name':'api',
                'url':'/exit_settings/garage/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(str(exit_config_modified_date), "%Y-%m-%d %H:%M:%S").timetuple())
            },

            'e_invoice_config':{
                'file_name':'api',
                'url':'/einvoice-config/get_einvoice_config/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(str(einvoice_config_modified_date), "%Y-%m-%d %H:%M:%S").timetuple())
            },

            'device_pad':{
                'file_name':'api',
                'url':'/device/pad/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(str(device_pad_modified_date), "%Y-%m-%d %H:%M:%S").timetuple())
            },
            'pad_garage_args':{
                'file_name':'api',
                'url':'/pad-garage-args/{id:\d*}',
                'updated_date':time.mktime(datetime.datetime.strptime(str(garage_args_modified_date), "%Y-%m-%d %H:%M:%S").timetuple())
            }
        }

        return update_status
    
    async def get_ip_address_of_the_current_EC2(self):
        #client = boto3.client('ec2')
        #instance_dict = client.describe_instances().get('Reservations')
        #for eip_dict in addresses_dict['Addresses']:
            #print (eip_dict['PublicIp'])
        #for reservation in instance_dict:
            #for instance in reservation['Instances']: 
                #if instance[u'State'][u'Name'] == 'running' and instance.get(u'PublicIpAddress') is not None:
                    #n=instance.get(u'PublicIpAddress')
                    #print(n)
        return True

    def get_file_update_date(self,customer_id,garage_id,file_name):
        file_path=os.path.join('/usr/share/nginx/html/files/pad_files/',customer_id,garage_id,file_name)
        file_modified_date = os.stat(file_path).st_mtime
        return file_modified_date

    async def get_apk_by_garage_id(self,customer_id,garage_id,file_server_path):

        walk_path = f"/usr/share/nginx/html/files/pad_files"
        apk_path=None
        for dirPath, dirNames, fileNames in os.walk(f'{walk_path}/{customer_id}/{garage_id}'):
            #n = [dirPath for n in dirNames if n.endswith('.jar')]
            #print(f'n-----{n}')
            for n in fileNames:
                if n.endswith('.apk'):
                    index = dirPath.find('pad_file')
                    apk_path = os.path.join(file_server_path,dirPath[index:],n)
        if apk_path == None:
            for dirPath, dirNames, fileNames in os.walk(f'{walk_path}/{customer_id}'):
                for n in fileNames:
                    if n.endswith('.apk'):
                        index = dirPath.find('pad_file')
                        apk_path = os.path.join(file_server_path,dirPath[index:],n)
        
        if apk_path == None:
            for p in glob.glob(f"{walk_path}/**.apk"):
                index = p.find('pad_file')
                apk_path = os.path.join(file_server_path,p[index:])
        return apk_path

    async def file_upload(self, filename, content, function_name):
        # Windows 測試
        # file_directory_path = "D:\\test_use"
        # 正式環境
        file_directory_path = "/home/pms_plus/file_directory/ui_file_uploader/"

        # 待修改 利用switch判斷
        # if (operator.eq(function_name.decode('utf-8'), "customer")):
        #     print(function_name.decode('utf-8'))

        sql = "SELECT customer_code FROM `customer` WHERE customer_id = :customer_id"
        async with self._db.acquire() as conn: 
            query = await conn.execute(text(sql), {'customer_id':self._user['customer_id']})
            if query.rowcount > 0:
                query_list = [dict(row.items()) async for row in query]
                query_list[0]['customer_code']

                upload_path = os.path.join(file_directory_path, function_name.decode('utf-8'), str(query_list[0]['customer_code']))
                self.mkdirs(upload_path)
                fp = open(os.path.join(upload_path, (filename.decode('utf-8'))), 'wb')
                fp.write(content)
                fp.close
                
        return "upload_success"

    """ 建立多層目錄 """
    def mkdirs(self, path): 
        # 去除前方空格
        path = path.strip()
        # 去除尾巴 \ 符號
        path = path.rstrip("\\")

        # 判斷路徑是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
    
        # 判断结果
        if not isExists:
            # 建立目錄
            os.makedirs(path)
            # 如果不存在則建立目錄
            return True
        else:
            # 如果目錄存在則不建立
            return False