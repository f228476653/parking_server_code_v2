"""Application module."""
import os, time
from app.config.settings import Settings
from app.config.routes import map_routes
from aiomysql.sa import create_engine
from sqlalchemy import text
from app.util.encrypt_helper import EncryptHelper
from app.config.models import Account,Customer,Role,Map_Role_Permission,Permission, Garage, ExitConfig, DevicePV
from app.config.models import ExitTypeConfigDetail,Map_Garage_To_Garage_Group,GarageGroup,Lane,Map_Garage_To_Account
from app.config.models import SystemConfiguration, CustomerIboxArgs, GarageIboxArgs, DeviceIboxArgs, CustomerMapCardCase
from app.config.models import CustomerPv3Args, GaragePv3Args, DevicePv3Args, FeeRule, FeePara
from app.config.db_version_control import DBVersionControl
from datetime import datetime
from aiohttp_swagger import *
environment_settings = None

async def startup(app):
    """Startup app. set jwt config here because we don't want jwt is configurable"""
    app['jwt_secret'] = 'secret'  # note! Changing JWT configuration will fail authorization 
    app['jwt_algorithm'] = 'HS256'
    app['jwt_exp_delta_seconds'] = 60000000
    app['jwt_exp_delta_seconds_remember_me'] = 36000000
    app.logger.info('starting up server')

async def cleanup(app): 
    """Cleanup app."""
    # Mysql/MariaDB
    app.logger.info('server shutdown')
    app['pmsdb'].close()
    await app['pmsdb'].wait_closed()
    app['pmsdb'] = None

async def attach_db(app):
    app.logger.info("mysql host:{}, port: {}, dbname: {}, username: {}, pass: {}".format(
        environment_settings.SETTINGS['mysql']['host']
        ,environment_settings.SETTINGS['mysql']['port']
        ,environment_settings.SETTINGS['mysql']['dbname']
        ,environment_settings.SETTINGS['mysql']['username']
        ,environment_settings.SETTINGS['mysql']['passwd'])
    )

    app['pmsdb'] = await create_engine(
            host=environment_settings.SETTINGS['mysql']['host'],
            port=int(environment_settings.SETTINGS['mysql']['port']),
            db=environment_settings.SETTINGS['mysql']['dbname'],
            user=environment_settings.SETTINGS['mysql']['username'],
            password=environment_settings.SETTINGS['mysql']['passwd'],
            autocommit=environment_settings.SETTINGS['mysql']['autocommit'],
            echo=True,
            charset='utf8',
            use_unicode=True,
            sql_mode='NO_AUTO_VALUE_ON_ZERO',
            maxsize=1000
    )

async def populate_init_values(engine):
    """generate default data to database."""

    root_passwd = EncryptHelper().encrypt('@@123qwe')
    user_passwd = EncryptHelper().encrypt('123')
    await populate_permission(engine)
    async with engine.acquire() as conn:
        # await conn.execute(FeeRule.insert().values({"fee_rule_id": 1, "new_car_hour": 1, "period": 30, "normal_day":"2018/3/31, 2018/4/1", "holiday": "2018/1/1, 2018/1/2", "free_time": 30, "fee_mode": 0, "update_time": "2018/6/26 00:00:00", "update_user": "root", "garage_id": 1}))
        # await conn.execute(FeePara.insert().values({"fee_para_id": 1, "fee_para_mode": "normal_day", "hour_period_fee1": 20, "hour_period_fee1_start": 0, "hour_period_fee1_end": 12, "hour_period_fee2": 20, "hour_period_fee2_start": 12, "hour_period_fee2_end": 0, "max_fee": 500, "max_hour": 12, "special_rule": 0, "special_fee_start": 8, "special_fee_end": 16, "special_fee_max": 0, "special_fee_hour": 23, "monthly_pass": 0, "update_time": "2018-06-26 00:00:00", "update_user": "root", "fee_rule_id": 1}))
        # await conn.execute(FeePara.insert().values({"fee_para_id": 2, "fee_para_mode": "holiday", "hour_period_fee1": 30, "hour_period_fee1_start": 0, "hour_period_fee1_end": 12, "hour_period_fee2": 30, "hour_period_fee2_start": 12, "hour_period_fee2_end": 0, "max_fee": 250, "max_hour": 8, "special_rule": 0, "special_fee_start": 8, "special_fee_end": 16, "special_fee_max": 0, "special_fee_hour": 23, "monthly_pass": 0, "update_time": "2018-06-26 00:00:00", "update_user": "root", "fee_rule_id": 1}))
         #系統匯出到主機上的路徑
        await conn.execute(SystemConfiguration.insert().values({"key": "ftp_device_export_csv", "value": "csvs/out", "description": "ftp_device參數匯出路徑", "config_group_name": "device"}))
        await conn.execute(SystemConfiguration.insert().values({"key": "html_device_export_csv", "value": "/usr/share/nginx/html/files/out", "description": "html_device參數匯出路徑", "config_group_name": "device"}))
        # await conn.execute(Garage.insert().values({'garage_id': 1, 'garage_code': 23400, 'customer_id': 0}))
        # await conn.execute(CustomerIboxArgs.insert().values({"customer_ibox_args_id": 1, "market_code": "P21", "cashier_no": "A110", "system_id": "42", "comp_id": "29", "machine": "4D3C2B1A", "ipass_water_lv_host": "192.168.0.101", "ipass_water_lv_port": 8988, "socket_ip": "10.20.1.74", "transaction_system_id": "00", "loc_id": "02", "transaction_terminal_no": "471F6241", "tid": "00000002", "mid": "0000000000000000", "YHDP_water_lv": 3000, "YHDP_water_lv_host": "192.168.0.101", "YHDP_water_lv_port": 6666, "nii": 667, "host_ip": "192.168.35.129", "host_port": "8000", "host_user": "root", "host_pwd": "@@123qwe", "update_user": "root", "update_time": datetime.now(), "customer_id": 0}))
        # await conn.execute(GarageIboxArgs.insert().values({"garage_ibox_args_id": 1, "garage_code": "23400", "store_no": "323", "pos_no": 1, "eid_store_no": "3346", "plid": "01E1", "printer": 1, "tax_id_num": "86517413", "ntp_server": "103.18.128.60", "update_user": "root", "update_time": datetime.now(), "garage_id": 1}))
        # await conn.execute(DeviceIboxArgs.insert().values({"device_ibox_args_id": 1, "device_name": "iBox一號", "external_ip": "192.168.11.106", "station_inout": 1, "ECC": 1, "iPass": 1, "iCash": 0, "YHDP": 1, "ip": "192.168.0.102", "gateway": "255.255.255.255", "eid_pos_no": "346Z", "client_pv": "192.168.53.201,192.168.53.202", "time_sync_period": 24, "update_user": "root", "update_time": datetime.now(), "garage_id": 1}))
        # await conn.execute(CustomerMapCardCase.insert().values({'customer_map_card_case_id': 1, 'device_type': 'iBox', 'enable_card_case': 7, 'customer_id': 0}))
       
        # await conn.execute(Garage.insert().values({'garage_id': 2, 'garage_code': 23500, 'customer_id': 0}))
        # await conn.execute(CustomerPv3Args.insert().values({"customer_pv3_args_id": 1, "market_code": "P21", "cashier_no": "A110", "system_id": "42", "comp_id": "29", "machine": "4D3C2B1A", "ipass_water_lv_host": "192.168.0.101", "ipass_water_lv_port": 8988, "socket_ip": "10.20.1.74", "transaction_system_id": "00", "loc_id": "02", "transaction_terminal_no": "471F6241", "tid": "00000002", "mid": "0000000000000000", "YHDP_water_lv": 3000, "YHDP_water_lv_host": "192.168.0.101", "YHDP_water_lv_port": 6666, "nii": 667, "client_pv": "192.168.53.201,192.168.53.202", "time_sync_period": 24, "update_user": "root", "update_time": datetime.now(), "customer_id": 0}))
        # await conn.execute(GaragePv3Args.insert().values({"garage_pv3_args_id": 1, "garage_code": "23400", "store_no": "323", "pos_no": 1, "eid_store_no": "3346", "plid": "01E1", "printer": 1, "tax_id_num": "86517413", "ntp_server": "103.18.128.60", "update_user": "root", "update_time": datetime.now(), "garage_id": 1}))
        # await conn.execute(DevicePv3Args.insert().values({"device_pv3_args_id": 1, "device_name": "PV3一號", "external_ip": "61.222.250.66", "station_inout": 1, "ECC": 1, "iPass": 1, "iCash": 0, "YHDP": 1, "ip": "192.168.0.102", "mac_ip": "255.255.255.255", "eid_pos_no": "346Z", "update_user": "root", "update_time": datetime.now(), "garage_id": 1}))
        # await conn.execute(CustomerMapCardCase.insert().values({'customer_map_card_case_id': 2, 'device_type': 'Pv3', 'enable_card_case': 7, 'customer_id': 0}))

        await conn.execute(Account.insert().values({'account': 'system', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1,'customer_id':0}))
        await conn.execute(Account.insert().values({'account': 'root', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1,'customer_id':0}))
        await conn.execute(Customer.insert().values({'customer_id':0, 'customer_code':'8001','company_union_number':'800101','contact_username': 'root', 'company_name': u'Acer ITS','customer_status':1,'phone_number1':'02-26963690#8301','create_account_id':0}))
        """ 新增系統用戶管理員預設權限 """
        await conn.execute(Role.insert().values({'role_id':1, 'name': 'root_admin', 'description': 'root admin role','role_type':'root_admin','is_system_role':1,'customer_id':0,'create_account_id':0}))
        pad_permission = getAllAdminPermission()
        for w in pad_permission:
            await conn.execute(Map_Role_Permission.insert().values({'role_id': 1, 'permission_id': w, 'create_account_id':0}))
        
        """新增平板型用戶管理員預設角色與權限  """
        await conn.execute(Role.insert().values({'role_id':2, 'name': 'pad_admin', 'description': 'admin role','role_type':'pad_admin','is_system_role':1,'customer_id':1,'create_account_id':0}))
        pad_permission = getPadAdminPermission()
        for w in pad_permission:
            await conn.execute(Map_Role_Permission.insert().values({'role_id': 2, 'permission_id': w, 'create_account_id':0}))

    
        
def getPadAdminPermission():
    """ 取得平板型用戶 權限 """
    return [1,2,3,4,5,6,11,12,13,31,32,33,91,92,93,111,112,113,131,143,181,182]

def getAllAdminPermission():
    """ 取得最大 權限 """
    return [1,2,3,4,5,6,11,12,13,21,22,23,191,192,193,31,32,33,41,42,43,51,52,53,54,61,62,63,65,64,66,67,71,72,73,74,75,81,82,83,91,92,93,111,112,113,121,122,123,131,132,133,141,142,143,144,151,152,153,154,161,162,163,163,181,182]

async def populate_permission(engine):
    """ 維運管理群組 """
    async with engine.acquire() as conn:
        """ 1,2, 11, 21, 31, 91, 101,111,121,131,132,151,152,153,154,181,182"""
        await conn.execute(Permission.insert().values({'permission_id':1,'name': '維運管理', 'description': '維運管理功能群組','permission_type':'group','create_account_id':0,'parent_id':0}))

        await conn.execute(Permission.insert().values({'permission_id':2,'name': '帳號管理', 'description': '帳號管理功能','permission_type':'page','create_account_id':0,'parent_id':1}))
        await conn.execute(Permission.insert().values({'permission_id':3,'name': '帳號修改', 'description': '帳號管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':2}))
        await conn.execute(Permission.insert().values({'permission_id':4,'name': '帳號刪除', 'description': '帳號管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':2}))
        await conn.execute(Permission.insert().values({'permission_id':5,'name': '帳號場站指派', 'description': '帳號管理場站指派','permission_type':'page_feature','create_account_id':0,'parent_id':2}))
        await conn.execute(Permission.insert().values({'permission_id':6,'name': '帳號角色指派', 'description': '帳號管理角色指派', 'permission_type':'page_feature','create_account_id':0,'parent_id':2}))

        await conn.execute(Permission.insert().values({'permission_id':11,'name': '角色管理', 'description': '角色管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':12,'name': '角色修改', 'description': '角色管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':11}))
        await conn.execute(Permission.insert().values({'permission_id':13,'name': '角色刪除', 'description': '角色管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':11}))

        await conn.execute(Permission.insert().values({'permission_id':21,'name': '客戶管理', 'description': '客戶管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':22,'name': '客戶基本設定修改', 'description': '客戶管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':21}))
        await conn.execute(Permission.insert().values({'permission_id':23,'name': '客戶刪除', 'description': '客戶管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':21}))

        await conn.execute(Permission.insert().values({'permission_id':191,'name': '客戶行事曆匯入', 'description': '客戶行事曆匯入','permission_type':'page_feature','create_account_id':0,'parent_id':21}))
        await conn.execute(Permission.insert().values({'permission_id':192,'name': '客戶行事曆匯出', 'description': '客戶行事曆匯出','permission_type':'page_feature','create_account_id':0,'parent_id':21}))
        await conn.execute(Permission.insert().values({'permission_id':193,'name': '客戶行事曆產出dat', 'description': '客戶行事曆產出dat','permission_type':'page_feature','create_account_id':0,'parent_id':21}))

        await conn.execute(Permission.insert().values({'permission_id':31,'name': '場站管理', 'description': '場站管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':32,'name': '場站基本設定修改', 'description': '場站管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':33,'name': '場站刪除', 'description': '場站管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':31}))

        await conn.execute(Permission.insert().values({'permission_id':41,'name': '票證設定管理', 'description': '票證設定管理功能','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':42,'name': '票證設定修改', 'description': '票證設定修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':41}))
        await conn.execute(Permission.insert().values({'permission_id':43,'name': '票證設定刪除', 'description': '票證設定刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':41}))

        await conn.execute(Permission.insert().values({'permission_id':51,'name': '設備管理', 'description': '設備管理','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':52,'name': '設備新增', 'description': '設備新增功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':51}))
        await conn.execute(Permission.insert().values({'permission_id':53,'name': '設備修改', 'description': '設備修改功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':51}))
        await conn.execute(Permission.insert().values({'permission_id':54,'name': '設備刪除', 'description': '設備刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':51}))

        await conn.execute(Permission.insert().values({'permission_id':61,'name': '定期票', 'description': '定期票','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':62,'name': '定期票新增', 'description': '定期票新增','permission_type':'page_feature','create_account_id':0,'parent_id':61}))
        await conn.execute(Permission.insert().values({'permission_id':63,'name': '定期票修改', 'description': '定期票修改','permission_type':'page_feature','create_account_id':0,'parent_id':61}))
        await conn.execute(Permission.insert().values({'permission_id':64,'name': '定期票刪除', 'description': '定期票刪除','permission_type':'page_feature','create_account_id':0,'parent_id':61}))
        await conn.execute(Permission.insert().values({'permission_id':65,'name': '定期票產出dat', 'description': '定期票產出dat','permission_type':'page_feature','create_account_id':0,'parent_id':61}))
        await conn.execute(Permission.insert().values({'permission_id':66,'name': '定期票匯入', 'description': '定期票匯入','permission_type':'page_feature','create_account_id':0,'parent_id':61}))
        await conn.execute(Permission.insert().values({'permission_id':67,'name': '定期票匯出', 'description': '定期票匯出','permission_type':'page_feature','create_account_id':0,'parent_id':61}))
        
        await conn.execute(Permission.insert().values({'permission_id':71,'name': '場站行事曆', 'description': '場站行事曆','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':72,'name': '場站行事曆新增', 'description': '場站行事曆新增','permission_type':'page_feature','create_account_id':0,'parent_id':71}))
        await conn.execute(Permission.insert().values({'permission_id':73,'name': '場站行事曆修改', 'description': '場站行事曆修改','permission_type':'page_feature','create_account_id':0,'parent_id':71}))
        await conn.execute(Permission.insert().values({'permission_id':74,'name': '場站行事曆刪除', 'description': '場站行事曆刪除','permission_type':'page_feature','create_account_id':0,'parent_id':71}))
        await conn.execute(Permission.insert().values({'permission_id':75,'name': '場站行事曆產出dat', 'description': '場站行事曆產出dat','permission_type':'page_feature','create_account_id':0,'parent_id':71}))

        await conn.execute(Permission.insert().values({'permission_id':81,'name': '發票設定管理', 'description': '發票設定管理功能','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':82,'name': '發票設定修改', 'description': '發票設定修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':81}))
        await conn.execute(Permission.insert().values({'permission_id':83,'name': '發票設定刪除', 'description': '發票設定刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':81}))

        await conn.execute(Permission.insert().values({'permission_id':91,'name': '出場設定管理', 'description': '出場設定功能','permission_type':'page','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':92,'name': '出場設定修改', 'description': '出場設定修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':91}))
        await conn.execute(Permission.insert().values({'permission_id':93,'name': '出場啟用停用切換', 'description': '出場啟用停用切換功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':91}))

        await conn.execute(Permission.insert().values({'permission_id':101,'name': '車道設定管理', 'description': '車道設定功能','permission_type':'page','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':102,'name': '車道設定修改', 'description': '車道設定修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':101}))
        await conn.execute(Permission.insert().values({'permission_id':103,'name': '車道刪除', 'description': '車道刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':101}))

        await conn.execute(Permission.insert().values({'permission_id':111,'name': '場站群組管理', 'description': '場站群組管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':112,'name': '場站群組基本設定修改', 'description': '場站群組管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':111}))
        await conn.execute(Permission.insert().values({'permission_id':113,'name': '場站群組刪除', 'description': '場站群組管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':111}))

        await conn.execute(Permission.insert().values({'permission_id':121,'name': '授權金鑰管理', 'description': '授權金鑰管理','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':122,'name': '授權金鑰基本設定修改', 'description': '授權金鑰基本設定修改','permission_type':'page_feature','create_account_id':0,'parent_id':121}))
        await conn.execute(Permission.insert().values({'permission_id':123,'name': '授權金鑰刪除', 'description': '授權金鑰刪除','permission_type':'page_feature','create_account_id':0,'parent_id':122}))

        """ 帳務管理群組 """
        await conn.execute(Permission.insert().values({'permission_id':131,'name': '帳務管理', 'description': '帳務管理群組','permission_type':'group','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':132,'name': '帳務查詢', 'description': '帳務查詢功能','permission_type':'page','create_account_id':0,'parent_id':131}))
        await conn.execute(Permission.insert().values({'permission_id':133,'name': '帳務報表訂閱', 'description': '帳務報表訂閱','permission_type':'page_feature','create_account_id':0,'parent_id':131,'enable':0}))
        await conn.execute(Permission.insert().values({'permission_id':141,'name': 'PV即時交易資料查詢', 'description': 'PV即時交易資料查詢功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':142,'name': 'PV3即時交易資料查詢', 'description': 'PV3即時交易資料查詢功能','permission_type':'page','create_account_id':0,'parent_id':131}))
        await conn.execute(Permission.insert().values({'permission_id':143,'name': '平板即時交易資料查詢', 'description': '平板即時交易資料查詢功能','permission_type':'page','create_account_id':0,'parent_id':131}))
        await conn.execute(Permission.insert().values({'permission_id':144,'name': 'IBox即時交易資料查詢', 'description': 'IBox即時交易資料查詢功能','permission_type':'page','create_account_id':0,'parent_id':131}))
        
        """ 儀表板 群組 """
        await conn.execute(Permission.insert().values({'permission_id':151,'name': '儀表板', 'description': '儀表板群組','permission_type':'group','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':152,'name': '資源分析', 'description': '資源分析','permission_type':'page','create_account_id':0,'parent_id':151}))
        await conn.execute(Permission.insert().values({'permission_id':153,'name': '營收分析', 'description': '營收分析','permission_type':'page','create_account_id':0,'parent_id':151}))
        await conn.execute(Permission.insert().values({'permission_id':154,'name': '交易分析', 'description': '交易分析','permission_type':'page','create_account_id':0,'parent_id':151}))
        """ 計費設定 """
        await conn.execute(Permission.insert().values({'permission_id':161,'name': '計費設定管理', 'description': '計費設定管理','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':162,'name': '計費設定新增', 'description': '計費設定新增','permission_type':'page_feature','create_account_id':0,'parent_id':161}))
        await conn.execute(Permission.insert().values({'permission_id':163,'name': '計費設定修改', 'description': '計費設定修改','permission_type':'page_feature','create_account_id':0,'parent_id':161}))
        await conn.execute(Permission.insert().values({'permission_id':164,'name': '計費設定刪除', 'description': '計費設定刪除','permission_type':'page_feature','create_account_id':0,'parent_id':161}))

        """ 報表群組 """
        await conn.execute(Permission.insert().values({'permission_id':181,'name': '報表', 'description': '報表群組','permission_type':'group','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':182,'name': '結班報表', 'description': '結班報表','permission_type':'page','create_account_id':0,'parent_id':181}))
        
        

async def populate_demo_values(engine):
    """generate default data to database."""

    root_passwd = EncryptHelper().encrypt('@@123qwe')
    user_passwd = EncryptHelper().encrypt('123')
    populate_permission(engine)
    async with engine.acquire() as conn:
        await conn.execute(SystemConfiguration.insert().values({"key": "ibox_export_csv", "value": "./export_csv", "description": "iBox參數設定儲存位置","config_group_name": "system_configuration"}))
        await conn.execute(Account.insert().values({'account': 'demo', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':False,'role_id':1,'create_account_id':1,'customer_id':1}))
        await conn.execute(Account.insert().values({'account': 'root', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1,'customer_id':1}))

    
        await conn.execute(Account.insert().values({'account': 'B20_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B28_manager', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B20_accountant', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B21_guard', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B25_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B24_accountant', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B24_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B23_guard', 'is_customer_root':0 , 'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B22_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B25_accountant', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B21_manager', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B22_manager', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B23_manager', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B22_accountant', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B24_manager','is_customer_root':0 , 'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B26_guard','is_customer_root':0 , 'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'B27_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C21_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C22_guard', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C23_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C24_guard', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C25_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C26_guard', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C27_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C20_guard', 'is_customer_root':0 ,'password': root_passwd,'is_superuser':True,'role_id':1,'create_account_id':1}))
        await conn.execute(Account.insert().values({'account': 'C21_guard', 'is_customer_root':0 ,'password': user_passwd,'is_superuser':False,'role_id':2,'create_account_id':1}))

    async with engine.acquire() as conn:
        await conn.execute(Customer.insert().values({'customer_code':'12001','company_union_number':'19348200','contact_username': 'root', 'company_name': u'Attwater Parking Garage','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B20','company_union_number':'19348201','contact_username': 'ray', 'company_name': 'Best Parking','customer_status':'0','mobile':'0919220660','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B21','company_union_number':'19348202','contact_username': 'Liu,Yuxin', 'company_name': 'Midway Airport Parking Express','customer_status':'1','mobile':'0913050778','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B22','company_union_number':'19348203','contact_username': 'Lin,Aaron R', 'company_name': 'KAU Parking & Transit','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B23','company_union_number':'19348204','contact_username': 'MaxChen', 'company_name': 'TEMU Parking Lot', 'customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B24','company_union_number':'19348205','contact_username': 'Tseng,Strikeris', 'company_name': 'Super Park Lot','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B25','company_union_number':'19348206','contact_username': 'Chen, Tweetie', 'company_name': 'Economy Parking Lot','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B26','company_union_number':'19348207','contact_username': 'JalenChen', 'company_name': 'West Campus Garage','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B27','company_union_number':'19348208','contact_username': 'tsuming,Wang', 'company_name': 'Grantel Park Garage','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'B28','company_union_number':'19348209','contact_username': 'Yang,Xiang', 'company_name': 'Airport Parking','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C20','company_union_number':'19348210','contact_username': 'Tsao Daniel', 'company_name': 'OHara Parking','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C21','company_union_number':'1934821','contact_username': 'Liu,Kay', 'company_name': 'ALCOO Parking','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C22','company_union_number':'19348222','contact_username': 'Chang,Glory', 'company_name': 'Everyday Garage','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C23','company_union_number':'19348331','contact_username': 'Huang,Jenny', 'company_name': 'Everyday Garage','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C24','company_union_number':'19348333','contact_username': 'Hsieh,Gavin', 'company_name': 'KBG Company','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C25','company_union_number':'19348344','contact_username': 'Chen,Alina', 'company_name': 'ABC Company1','customer_status':'0','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C26','company_union_number':'19348123','contact_username': 'Tsai,Albert', 'company_name': 'KBG Company','customer_status':'1','mobile':'0919220770','create_account_id':1}))
        await conn.execute(Customer.insert().values({'customer_code':'C27','company_union_number':'19348613','contact_username': 'Su,BowBow', 'company_name': 'ABC Company1','customer_status':'0','mobile':'0919220770','create_account_id':1}))

    
    async with engine.acquire() as conn:
        await conn.execute(Role.insert().values({'name': 'admin', 'description': 'admin role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'user', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'www', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'aaa', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'bbb', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'ccc', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'ddd', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'e', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'f', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'g', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'h', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'i', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'jj', 'description': 'user role','role_type':'system','create_account_id':1}))
        await conn.execute(Role.insert().values({'name': 'kk', 'description': 'user role','role_type':'system','create_account_id':1}))
        
        await conn.execute(Map_Role_Permission.insert().values({'role_id': 1, 'permission_id': 1,'create_account_id':1}))
        await conn.execute(Map_Role_Permission.insert().values({'role_id': 1, 'permission_id': 2,'create_account_id':1}))
        await conn.execute(Map_Role_Permission.insert().values({'role_id': 1, 'permission_id': 3,'create_account_id':1}))
        await conn.execute(Map_Role_Permission.insert().values({'role_id': 1, 'permission_id': 4,'create_account_id':1}))
        await conn.execute(Map_Role_Permission.insert().values({'role_id': 2, 'permission_id': 1,'create_account_id':1}))
        await conn.execute(Map_Role_Permission.insert().values({'role_id': 2, 'permission_id': 2,'create_account_id':1}))
        await conn.execute(Garage.insert().values({'garage_id':1,'garage_code':'11001','garage_name':'A21 環北站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':2,'garage_code':'11002','garage_name':'A9 林口站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':3,'garage_code':'11003','garage_name':'A6 泰山貴和站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':4,'garage_code':'11004','garage_name':u'A4 新莊副都心站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':5,'garage_code':'11007','garage_name':u'A5 泰山站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':6,'garage_code':'11006','garage_name':u'A3 新北產業園區站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':7,'garage_code':'11107','garage_name':u'A7 體育大學站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':8,'garage_code':'11015','garage_name':u'A15 大園站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':9,'garage_code':'11016','garage_name':u'A16 橫山站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':10,'garage_code':'11017','garage_name':u'A17 領航站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':11,'garage_code':'11011','garage_name':u'A11 坑口站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':12,'garage_code':'11020','garage_name':u'A20 興南站停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':13,'garage_code':'11021','garage_name':u'和平公園停車場'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':14,'garage_code':'11022','garage_name':u'德光公園'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':15,'garage_code':'11108','garage_name':'水樣公園'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':16,'garage_code':'11023','garage_name':'崇明停E6'.encode('utf-8')}))
        await conn.execute(Garage.insert().values({'garage_id':17,'garage_code':'11024','garage_name':'崇明五街'.encode('utf-8')}))
        await conn.execute(Map_Garage_To_Account.insert().values({'garage_id':1,'account_id':1}))

async def update_schema(engine, update_schema_list: list):
    """update"""
    root_passwd = EncryptHelper().encrypt('@@123qwe')
    user_passwd = EncryptHelper().encrypt('123')
    async with engine.acquire() as conn:
        for sql in update_schema_list:
            print(sql)
            c = [dict(row.items()) async for row in await conn.execute(text(sql),{'customer_id' : 2})]
            #c = await conn.execute(text(sql))
            # d = [dict(i.items() async for i in c)]
            print(c)
    print('update finished')

async def read_prodcution_env(app):
    await environment_settings.load_environment()

async def read_custom_env(app):
    await environment_settings.load_environment(app['command_args'].env)

async def read_develop_env(app):
    await environment_settings.load_environment()
    print (environment_settings.SETTINGS)

async def fast_enable_kevin_env(app):
    await environment_settings.load_environment(app['command_args'].p)    
    
async def handle_db_schema(app):
    db_version_clause =  app['command_args'].db
    schema = DBVersionControl(app['pmsdb'])
    status = db_version_clause[0]
    # try:
    if status == "init":
        await schema.V0_0()
        result = {"is_corrent": True, "index_start" : 0, "index_end": len(schema.version) -1}
    elif status == "update":
        version_number = show_db_version()
        if version_number == db_version_clause[1]:
            result = schema.is_correct_version_number(float(db_version_clause[1]), float(db_version_clause[2]))
        else:
            message = '''current version no match please checkout version.txt
            current version:{0}
            input current version:{1}
            '''.format(version_number, db_version_clause[1])
            raise Exception(message)
    elif status == "backup":
        # TODO backup db sql
        print("start backup")
        await schema.back()
    else:
        print('prefix no match')
        return
    if result['is_corrent']:
        for i in schema.version[result['index_start'] : result['index_end'] + 1]:
            version_no = "v" + str(i).replace('.', '_')
            update_schema = getattr(schema, version_no)
            await update_schema()
        if status == "init":
            await populate_init_values(app['pmsdb'])
        # write schema version to version.txt
        update_version_index = result['index_end']
        version = "v" + str(schema.version[update_version_index])
        with open("./version.txt", "w+") as f:
            version_message = "db schema version : " + version
            print('目前版本:', version_message)
            f.write(version_message)
        f.close()
    else:
        print('輸入版本號有誤 請確認有此版本', result['version_start'], result['version_end'])
    # except Exception as e:
    #     print('更新DB版本出現錯誤 ', e)
        

def show_db_version():
    if os.path.isfile("./version.txt"):
        with open("./version.txt", "r") as f:
            r = f.readlines()
            result = r[-1]
        f.close()
        print(result)
        version = result.split(': v')
        version_number = version[1].rsplit()
        return version_number[0]
    else:

        version_number = '查無檔案version.txt'
        print(version_number)
        return version_number

def app_config(app):
    global environment_settings
    environment_settings = Settings()
    """Add app configs."""
    if app['command_args'].prod:
        app.on_startup.append(read_prodcution_env)
    elif app['command_args'].p:
        app.on_startup.append(fast_enable_kevin_env)
    elif app['command_args'].env:
        app.on_startup.append(read_custom_env)
    else:
        app.on_startup.append(read_develop_env)
    
    #app.on_startup.append(map_routes)
    
    app.on_startup.append(startup)
    app.on_startup.append(attach_db)
    
    if app['command_args'].db:
        print('開始變更db 版本')
        app.on_startup.append(handle_db_schema)
    elif app['command_args'].init:
        app.on_startup.append(init)
    elif app['command_args'].demo:
        app.on_startup.append(populate_demo_data)

    app.on_cleanup.append(cleanup)

    return app
