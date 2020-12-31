import aiomysql.sa
from sqlalchemy import text
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import select
from app.config.models import CustomerPv3Args, Account, CustomerMapCardCase, GaragePv3Args, DevicePv3Args, Customer, Garage
from app.services.service import Service
from app.module.csv_handler import CsvHandler
from app.services.system_configuration import SystemConfigurationService
from app.module.csv_spec import CsvSpec
class DevicePv3Service(Service):
    """ device_pv3 info handler """
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
    
    async def save_customer_map_card_case(self, check_customer_id: int, customer_id, card_case: dict, device_type: str):
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
                result = await conn.execute(GaragePv3Args.select()
                .where(GaragePv3Args.c.garage_id == garage_id))
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
        """ 新增PV3 場站層級參數 """
        if 1 == 1:
            try:
                result = await conn.execute(GaragePv3Args.insert().values(garage_device_bean))
            except Exception as e:
                raise PermissionError(e, "insert agrs error")
            else:
                return True

    async def update_garage_device_argument_by_garage_id(self, garage_device_bean: dict, conn):
        """ 更新PV3 場站層級參數"""
        if 1 == 1:
            try:
                result = await conn.execute(GaragePv3Args.update().values(garage_device_bean)
                .where(GaragePv3Args.c.garage_pv3_args_id == garage_device_bean['garage_pv3_args_id']))
            except Exception as e:
                raise PermissionError(e, "update agrs error")
            else:
                return True

    async def delete_garage_device_argument_by_garage_id(self, garage_id: int, conn):
        if 1 == 1:
            # async with self._db.acquire() as conn:
            result = await conn.execute(GaragePv3Args.delete()
            .where(GaragePv3Args.c.garage_id == garage_id))
            return True

    async def get_customer_device_argument_by_customer_id(self, customer_id: int, device_type):
        """ 取出之前該廠商該設備的客戶層級參數 如果無則回傳None"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                if device_type == 'PV3':
                    print('即將執行')
                    result = await conn.execute(CustomerIPV3Args.select()
                    .where(CustomerIPV3Args.c.customer_id == customer_id))
                    result = [dict(row.items()) async for row in result]
                    return None if len(result) == 0 else result[0]

    async def save_customer_device_args(self, check_customer_id: int, customer_id: int, bean: dict, device_type: str):
        """ 新增或修改 客戶層級參數 """
        if 1 == 1 :
            async with self._db.acquire() as conn:
                if "PV3" == device_type:
                    if await self.get_customer_device_argument_by_customer_id(customer_id, device_type) is None:
                        await self.add_customer_device_argument(customer_id, bean, device_type)
                        print("!!!!!!!!!!!!!!!!!!!!!!!新增")
                    else:
                        await self.update_customer_device_argument_by_customer_id(customer_id, bean, device_type)
                        print("修改!!!!!!!!!!!!!!!!!!!!!!")
                return True
               
    async def add_customer_device_argument(self, customer_id: int, customer_device_bean: dict, device: str):
        """ 新增 客戶層級參數 """
        if 1 == 1:
            if device == 'PV3':
                async with self._db.acquire() as conn:
                    result = await conn.execute(CustomerIPV3Args.insert().values(customer_device_bean))
                    return True

    async def update_customer_device_argument_by_customer_id(self, customer_id: int, customer_device_bean: dict, device: str):
        """ 更新pv3 客戶層級參數"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                if device == 'PV3':
                    result = await conn.execute(CustomerIPV3Args.update().values(customer_device_bean)
                    .where(CustomerIPV3Args.c.customer_pv3_args_id == customer_device_bean['customer_pv3_args_id']))
                    return True

    async def delete_customer_device_argument_by_customer_id(self, customer_id: int, device_type: str):
        if 1 == 1 :
            async with self._db.acquire() as conn:
                if device_type == 'PV3':
                    result = await conn.execute(CustomerIPV3Args.delete()
                    .where(CustomerIPV3Args.c.customer_id == customer_id))

    async def device_export(self, data: dict):
        async with self._db.acquire() as conn:
            customer_id = data['customer_id']
            garage_id = data['garage_id']
            device_pv3_args_id = data['device_pv3_args_id']
            garage_code = data['garage_code']
            customer_device = await self.get_customer_device_argument_by_customer_id(customer_id, 'PV3')
            garage_device = await self.get_garage_device_by_garage_id(garage_id)
            device = await self.get_device_by_device_id(device_pv3_args_id)
            await self.build_csv(customer_device, garage_device, device, garage_code)
            return True


    async def build_csv(self, customer_device, garage_device, device, garage_code):
        if 1 == 1:
            async with self._db.acquire() as conn:
                customer_code_sql = """ select customer_code from customer where customer_id = :customer_id """
                customer_code = await conn.execute(text(customer_code_sql), {'customer_id': self._user['customer_id']})
                customer_code = await customer_code.scalar()
                # 從系統設定檔取出 匯出csv所要存放路徑
                system_configuration_service = SystemConfigurationService(self._db, self._user)
                html_export_path = await system_configuration_service.get_system_configuration_by_key('html_pv3_export_csv')
                ftp_export_path = await system_configuration_service.get_system_configuration_by_key('ftp_pv3_export_csv')
                if html_export_path is None:
                    raise PermissionError("請檢查是否有設定系統pv3 html path ","system_configuration 找不到html所存路徑")
                if ftp_export_path is None:
                    raise PermissionError("請檢查是否有設定系統pv3 ftp path","system_configuration 找不到ftp所存路徑")
                csv_handler = CsvHandler()
                export_path = {'html': html_export_path['value'], 'ftp': ftp_export_path['value']}
                # 負責把物件組成指定格式交給CsvHandler匯出到指定目錄
                csv_spec = CsvSpec()
                ip = device['ip'].split('.')
                device_folder_name = ip[len(ip)-1]
                pv3_csv_data = csv_spec.get_pv3_export_csv_data(customer_device, garage_device, device, garage_code)
                pv_csv = pv3_csv_data['pv']
                host_csv = pv3_csv_data['host']
                for i in pv_csv:
                    csv_handler.export_csv(export_path, i, pv_csv[i], customer_code, garage_code, device_folder_name, 'pv')
                for i in host_csv:
                    csv_handler.export_csv(export_path, i, host_csv[i], customer_code, garage_code, device_folder_name, 'host')

    # FOR Kevin API 簡易測試版
    async def aaa(self, c, g, d):
        async with self._db.acquire() as conn:
            c_id = await conn.execute(select([Customer.c.customer_id]).where(Customer.c.customer_code == c))
            c_id = await c_id.scalar()
            print(c_id)
            cr = [dict(row.items()) async for row in await conn.execute(CustomerIPV3Args.select().where(CustomerIPV3Args.c.customer_id == c_id))]
            print(cr)
            re = {'customer_device': cr[0]}
            g_c = await conn.execute(select([Garage.c.garage_id]).where(Garage.c.garage_code == g))
            g_id = await g_c.scalar()
            print(g_id)
            gr = [dict(row.items()) async for row in await conn.execute(GaragePv3Args.select().where(GaragePv3Args.c.garage_id == g_id))]
            print(gr)
            re['garage_device'] = gr[0]
            dr = [dict(row.items()) async for row in await conn.execute(DevicePv3Args.().where(DevicePv3Args.c.ip == d))]
            print(dr) 
            re['device'] = dr[0]
            return re

    # ========================== 以上正式 分隔線============================

    async def add_device_argument(self, device_bean: dict):
        """ 新增 設備層級參數 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                print('準備新增囉')
                result = await conn.execute(DevicePv3Args.insert().values(device_bean))
                return True

    async def update_device_argument_by_device_pv3_args_id(self, device_bean: dict):
        """ 更新pv3 設備層級參數 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                print('準備更新囉')
                result = await conn.execute(DevicePv3Args.update().values(device_bean)
                .where(DevicePv3Args.c.device_pv3_args_id == device_bean['device_pv3_args_id']))
                return True

    async def get_device_by_device_id(self, device_id: int):
        """ 取出之前該廠商該設備的設備層級參數 如果無則回傳None"""
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(DevicePv3Args.select()
                .where(DevicePv3Args.c.device_pv3_args_id == device_id))
                result = [dict(row.items()) async for row in result]
                return None if len(result) == 0 else result[0]

    async def get_all_device_by_garage_id(self, garage_id):
        device_query_sql = """ select device_ibox_args_id as id, 'Ibox' as device_type, device_name, update_time, update_user
                               from device_ibox_args where garage_id = :ibox_garage_id union
                               select device_pv3_args_id as id, 'PV3' as device_type, device_name, update_time, update_user
                               from device_pv3_args where garage_id = :pv3_garage_id """
        if 1 == 1:
            id = {"ibox_garage_id": garage_id, "pv3_garage_id": garage_id}
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(text(device_query_sql), id)]
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
                    await self.update_device_argument_by_device_pv3_args_id(customer_id, bean)
                    print("修改!!!!!!!!!!!!!!!!!!!!!!")
                return True

    async def delete_device_by_device_id(self, device_id: int):
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(DevicePv3Args.delete()
                .where(DevicePv3Args.c.device_pv3_args_id == device_id))
                print('刪除成功!!!!!!!!!!!!!!!!!')
                return True
                
    async def delete_device_by_garage_id(self, garage_id: int):
        """ 刪除該廠站 所有設備層級參數 !!這應該要跟場站層級一起執行 """
        if 1 == 1:
            async with self._db.acquire() as conn:
                result = await conn.execute(DevicePv3Args.delete()
                .where(DevicePv3Args.c.garage_id == garage_id))
            return True


    