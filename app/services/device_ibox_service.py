import aiomysql.sa
from sqlalchemy import text
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import select
from app.config.models import CustomerIboxArgs, Account, CustomerMapCardCase, GarageIboxArgs, DeviceIboxArgs, Customer, Garage
from app.services.service import Service
from app.module.csv_handler import CsvHandler
from app.services.system_configuration import SystemConfigurationService
from app.module.csv_spec import CsvSpec
class DeviceIboxService(Service):
    """ device_ibox info handler """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    # ========================== 以下正式 分隔線============================

    async def get_customer_map_card_case_by_customer_id_and_device_type(self, customer_id: int, device_type: str):
        """ 取得該廠商所啟用的卡種 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(CustomerMapCardCase.select()
                .where(CustomerMapCardCase.c.customer_id == customer_id)
                .where(CustomerMapCardCase.c.device_type == device_type))
                temp = None if result.rowcount == 0 else [dict(row.items()) async for row in result][0]
                return temp
    
    async def save_customer_map_card_case(self,check_customer_id: int, customer_id, card_case: dict, device_type: str):
        async with self._db.acquire() as conn:
            if await self.get_customer_device_argument_by_customer_id(customer_id, device_type) is None:
                await self.add_customer_map_card_case(card_case)
            else:
                await self.update_customer_map_card_case(card_case)
            return True

    async def add_customer_map_card_case(self, customer_map_card_case_bean: dict):
        """ 新增客戶所使用的卡種 """
        async with self._db.acquire() as conn:
            await conn.execute(CustomerMapCardCase.insert()
            .values(customer_map_card_case_bean))

    async def update_customer_map_card_case(self, customer_map_card_case_bean: dict):
        """ 更新客戶所使用卡種 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                await conn.execute(CustomerMapCardCase.update().values(customer_map_card_case_bean)
                .where(CustomerMapCardCase.c.customer_map_card_case_id == customer_map_card_case_bean['customer_map_card_case_id']))
        #raise PermissionError("check_account_has_authorization_to_use_customer","not permit to quesry other customer's data")

    async def get_garage_device_by_garage_id(self, garage_id: int):
        """ 取出之前該廠商該設備的場站層級參數 如果無則回傳None"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(GarageIboxArgs.select()
                .where(GarageIboxArgs.c.garage_id == garage_id))
                result = [dict(row.items()) async for row in result]
                return None if len(result) == 0 else result[0]

    async def save_garage_device_args(self, garage_device_bean: dict, conn = None):
        """ 新增或修改 場站層級參數 """
        if 1 == 1:
            if await self.get_garage_device_by_garage_id(garage_device_bean['garage_id']) is None:
                await self.add_garage_device_argument(garage_device_bean, conn)
                print("!!!!!!!!!!!!!!!!!!!!!! 新增 !!!!!!!!!!!!!!!!!!!!!!")
            else:
                await self.update_garage_device_argument_by_garage_id(garage_device_bean, conn)
                print("!!!!!!!!!!!!!!!!!!!!!!! 修改 !!!!!!!!!!!!!!!!!!!!!!")
    
    async def add_garage_device_argument(self, garage_device_bean: dict, conn):
        """ 新增iBox 場站層級參數 """
        if 1 == 1:
            try:
                result = await conn.execute(GarageIboxArgs.insert().values(garage_device_bean))
            except Exception as e:
                raise PermissionError(e, "insert agrs error")
            else:
                return True

    async def update_garage_device_argument_by_garage_id(self, garage_device_bean: dict, conn):
        """ 更新iBox 場站層級參數"""
        if 1 == 1:
            try:
                result = await conn.execute(GarageIboxArgs.update().values(garage_device_bean)
                .where(GarageIboxArgs.c.garage_ibox_args_id == garage_device_bean['garage_ibox_args_id']))
            except Exception as e:
                raise PermissionError(e, "update agrs error")
            else:
                return True

    async def delete_garage_device_argument_by_garage_id(self, garage_id: int, conn):
        if 1 == 1:
            # async with self._db.acquire() as conn:
            result = await conn.execute(GarageIboxArgs.delete()
            .where(GarageIboxArgs.c.garage_id == garage_id))
            return True

    async def get_customer_device_argument_by_customer_id(self, customer_id: int, device_type):
        """ 取出之前該廠商該設備的客戶層級參數 如果無則回傳None"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                if device_type == 'iBox':
                    print('即將執行')
                    result = await conn.execute(CustomerIboxArgs.select()
                    .where(CustomerIboxArgs.c.customer_id == customer_id))
                    result = [dict(row.items()) async for row in result]
                    return None if len(result) == 0 else result[0]

    async def save_customer_device_args(self, check_customer_id: int, customer_id: int, bean: dict, device_type: str):
        """ 新增或修改 客戶層級參數 """
        if 1 == 1 :
            async with self._db.acquire() as conn:
                if "iBox" == device_type:
                    if await self.get_customer_device_argument_by_customer_id(customer_id, device_type) is None:
                        await self.add_customer_device_argument(customer_id, bean, device_type)
                        print("!!!!!!!!!!!!!!!!!!!!!!!新增")
                    else:
                        await self.update_customer_device_argument_by_customer_id(customer_id, bean, device_type)
                        print("修改!!!!!!!!!!!!!!!!!!!!!!")
                return True
                if i == 'PV3':
                    print('施工中...')
               
    async def add_customer_device_argument(self, customer_id: int, customer_device_bean: dict, device: str):
        """ 新增 客戶層級參數 """
        if 1 == 1:
            if device == 'iBox':
                async with self._db.acquire() as conn:
                    result = await conn.execute(CustomerIboxArgs.insert().values(customer_device_bean))
                    return True
            if device == 'PV3':
                print('新增:', device)

    async def update_customer_device_argument_by_customer_id(self, customer_id: int, customer_device_bean: dict, device: str):
        """ 更新iBox 客戶層級參數"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                if device == 'iBox':
                    result = await conn.execute(CustomerIboxArgs.update().values(customer_device_bean)
                    .where(CustomerIboxArgs.c.customer_ibox_args_id == customer_device_bean['customer_ibox_args_id']))
                    return True
                if device == 'PV3':
                    print('修改:', device)

    async def delete_customer_device_argument_by_customer_id(self, customer_id: int):
        if 1 == 1 :
            async with self._db.acquire() as conn:
                result = await conn.execute(CustomerIboxArgs.delete()
                .where(CustomerIboxArgs.c.customer_id == customer_id))
        return True

    async def get_device_all_car_in_and_out(self, garage_id: int, device: dict):
        async with self._db.acquire() as conn:
            # !!! ibox 不需要car_in 先塞預設值
            # data_in = [dict(i.items()) async for i in await conn.execute(select([DeviceIboxArgs.c.ip]).where(DeviceIboxArgs.c.garage_id == garage_id).where(DeviceIboxArgs.c.station_inout == 1))]
            # car_in = []
            # for i in data_in:
            #     car_in.append(i['ip'])
            # car_in = ",".join(car_in)
            # device['car_in'] = car_in 
            device['car_in'] = '192.168.49.201'

            data_out = await (await conn.execute(select([DeviceIboxArgs.c.ip]).where(DeviceIboxArgs.c.garage_id == garage_id).where(DeviceIboxArgs.c.station_inout == 2))).fetchall()
            car_out = []
            for i in data_out:
                car_out.append(i['ip'])
            car_out = ",".join(car_out)
            device['car_out'] = car_out
            return device

    async def device_export(self, data: dict):
        async with self._db.acquire() as conn:
            # await self.is_ibox_args_exists(data['customer_id'], data['garage_id'], data['device_ibox_args_id'])
            garage_code = data['garage_code']
            build_data = await self.build_csv(data)
            ibox_csv_data = build_data['ibox_csv_data']
            customer_code = build_data['customer_code']
            device_folder_name = build_data['device_folder_name']
            export_path = await self.get_export_path()
            csv_handler = CsvHandler()
            pv_csv = ibox_csv_data['pv']
            # host_csv = ibox_csv_data['host']
            for i in pv_csv:
                csv_handler.export_csv(export_path, i, pv_csv[i], customer_code, garage_code, device_folder_name, 'pv')
            # for i in host_csv:
            #     csv_handler.export_csv(export_path, i, host_csv[i], customer_code, garage_code, device_folder_name, 'host')
            
            # await self.build_csv(customer_device, garage_device, device, garage_code, customer_code)
            return True

    async def build_csv(self, data: dict):
        async with self._db.acquire() as conn:
            customer_id = data['customer_id']
            garage_id = data['garage_id']
            device_ibox_args_id = data['device_ibox_args_id']
            garage_code = data['garage_code']
            customer_code = await(await conn.execute(select([Customer.c.customer_code])
            .where(Customer.c.customer_id == customer_id))).scalar()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', customer_code)
            customer_device = await self.get_customer_device_argument_by_customer_id(customer_id, 'iBox')
            customer_device['host'] = customer_device['host_ip'] + ',' + customer_device['host_port'] + ',' + customer_device['host_user'] + ',' + customer_device['host_pwd']
            garage_device = await self.get_garage_device_by_garage_id(garage_id)
            device = await self.get_device_by_device_id(device_ibox_args_id)
            device = await self.get_device_all_car_in_and_out(garage_id, device)
            # get API config <- 目前沒設定頁面 要自己去sql設定
            system_configuration_service = SystemConfigurationService(self._db, self._user)
            API_url = await system_configuration_service.get_system_configuration_by_key('API_url')
            API_port = await system_configuration_service.get_system_configuration_by_key('API_port')
            API_account = await system_configuration_service.get_system_configuration_by_key('API_account')
            API_pwd = await system_configuration_service.get_system_configuration_by_key('API_pwd')
            API_data = {'API_url': API_url['value'], 'API_port': API_port['value'], 'API_account': API_account['value'], 'API_pwd': API_pwd['value']}
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', API_data)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            # customer_code_sql = """ select customer_code from customer where customer_id = :customer_id """
            # customer_code2 = await conn.execute(text(customer_code_sql), {'customer_id': customer_device['customer_id']})
            # customer_code2 = await customer_code.scalar()
            # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', customer_code2)
            # 負責把物件組成指定格式交給CsvHandler匯出到指定目錄
            print('重點來囉')
            csv_spec = CsvSpec()
            device['driveway'] = 'iBox' + str(device_ibox_args_id)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', device['driveway'])
            # ip = device['ip'].split('.')
            device_folder_name = device['driveway']
            # device_folder_name = device_folder_name.zfill(3)
            ibox_csv_data = csv_spec.get_ibox_export_csv_data(customer_device, garage_device, device, garage_code, customer_code, API_data)
            return {'ibox_csv_data': ibox_csv_data, 'customer_code': customer_code, 'device_folder_name': device_folder_name}

    async def get_export_path(self):
        async with self._db.acquire() as conn:
            # 從系統設定檔取出(目前沒畫面 要更改設定要去資料庫) 匯出csv所要存放路徑
            system_configuration_service = SystemConfigurationService(self._db, self._user)
            # html_export_path = await system_configuration_service.get_system_configuration_by_key('html_device_export_csv')
            ftp_export_path = await system_configuration_service.get_system_configuration_by_key('ftp_device_export_csv')
            # if html_export_path is None:
            #     raise PermissionError("請檢查是否有設定系統device html path ","system_configuration 找不到html所存路徑")
            if ftp_export_path is None:
                raise PermissionError("請檢查是否有設定系統device ftp path","system_configuration 找不到ftp所存路徑")
            export_path = {'ftp': ftp_export_path['value']}
            return export_path

    async def is_ibox_args_exists(self, customer_id, garage_id, device_id):
        async with self._db.acquire() as conn:
            flag = False
            # 在匯出設定檔前 先檢查是否所有參數都收集齊
            condition1 = await self.get_customer_device_argument_by_customer_id(customer_id, 'iBox')
            condition2 = await self.get_garage_device_by_garage_id(garage_id)
            condition3 = await self.get_device_by_device_id(device_id)
            if condition1 != None or condition2 != None or  condition3 or None:
                flag = True
            print('!!!!!!!!!!!!!!!!!@@###################', condition1)
            print('!!!!!!!!!!!!!!!!!@@###################', condition2)
            print('!!!!!!!!!!!!!!!!!@@###################', condition3)
            print('0..............0 :', flag)
            return flag

    async def is_duplicate_ip_from_same_garage(self, garage_id: str, ip: str):
        async with self._db.acquire() as conn:
            print('hello')
            result = await conn.execute(select([DeviceIboxArgs.c.ip]).where(DeviceIboxArgs.c.garage_id == garage_id)
            .where(DeviceIboxArgs.c.ip == ip))
            duplicate_ip = False if result.rowcount == 0 else True
            print(duplicate_ip)
            return duplicate_ip

    # FOR Kevin API 簡易測試版
    async def aaa(self, c, g, d):
        async with self._db.acquire() as conn:
            c_id = await conn.execute(select([Customer.c.customer_id]).where(Customer.c.customer_code == c))
            c_id = await c_id.scalar()
            print(c_id)
            cr = [dict(row.items()) async for row in await conn.execute(CustomerIboxArgs.select().where(CustomerIboxArgs.c.customer_id == c_id))]
            print(cr)
            re = {'customer_device': cr[0]}
            g_c = await conn.execute(select([Garage.c.garage_id]).where(Garage.c.garage_code == g))
            g_id = await g_c.scalar()
            print(g_id)
            gr = [dict(row.items()) async for row in await conn.execute(GarageIboxArgs.select().where(GarageIboxArgs.c.garage_id == g_id))]
            print(gr)
            re['garage_device'] = gr[0]
            dr = [dict(row.items()) async for row in await conn.execute(DeviceIboxArgs.select().where(DeviceIboxArgs.c.ip == d))]
            print(dr) 
            re['device'] = dr[0]
            return re

    # ========================== 以上正式 分隔線============================

    async def add_device_argument(self, device_bean: dict):
        """ 新增 設備層級參數 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                print('準備新增囉')
                result = await conn.execute(DeviceIboxArgs.insert().values(device_bean))
                return True

    async def update_device_argument_by_device_ibox_args_id(self, device_bean: dict):
        """ 更新iBox 設備層級參數 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                print('準備更新囉')
                result = await conn.execute(DeviceIboxArgs.update().values(device_bean)
                .where(DeviceIboxArgs.c.device_ibox_args_id == device_bean['device_ibox_args_id']))
                return True

    async def get_device_by_device_id(self, device_id: int):
        """ 取出之前該廠商該設備的設備層級參數 如果無則回傳None"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(DeviceIboxArgs.select()
                .where(DeviceIboxArgs.c.device_ibox_args_id == device_id))
                result = [dict(row.items()) async for row in result]
                return None if len(result) == 0 else result[0]

    async def get_all_device_by_garage_id(self, garage_id):
        device_query_sql = """ select device_ibox_args_id as id, type as car_type, 'iBox' as device_type, device_name, d.update_time, d.update_user, d.garage_id,
                               IFNULL(f.fee_args_name,'尚未設定') as fee_args_name
                               from device_ibox_args as d  left join fee_rule as f 
                               on d.garage_id = f.garage_id and car_type = type
                               where d.garage_id = :garage_id """
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(text(device_query_sql), {"garage_id": garage_id})]
                print('觀察!!!!!!!!!!!!!!!!!',result)
                return result

    async def save_device_args(self, check_customer_id: int, customer_id: int, bean: dict, device_type: str):
        """ 新增或修改 客戶層級參數 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                if await self.get_device_argument_by_garage_id(bean['garage']) is None:
                    await self.add_device_argument(customer_id, bean)
                    print("!!!!!!!!!!!!!!!!!!!!!!!新增")
                else:
                    await self.update_device_argument_by_device_ibox_args_id(customer_id, bean)
                    print("修改!!!!!!!!!!!!!!!!!!!!!!")
                return True

    async def delete_device_by_device_id(self, device_id: int):
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(DeviceIboxArgs.delete()
                .where(DeviceIboxArgs.c.device_ibox_args_id == device_id))
                print('刪除成功!!!!!!!!!!!!!!!!!')
                return True
                
    async def delete_device_by_garage_id(self, garage_id: int):
        """ 刪除該廠站 所有設備層級參數 !!這應該要跟場站層級一起執行 """
        async with self._db.acquire() as conn:
            result = await conn.execute(DeviceIboxArgs.delete()
            .where(DeviceIboxArgs.c.garage_id == garage_id))
        return True

    async def download_device_parameter(self, data: dict):
        async with self._db.acquire() as conn:
            pass


    
