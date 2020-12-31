import aiomysql.sa
from sqlalchemy import text
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import select
from app.config.models import FeeRule, FeePara, Account, SpecialDay, DeviceIboxArgs
from app.services.service import Service
from app.module.csv_handler import CsvHandler
from app.services.system_configuration import SystemConfigurationService
from app.module.csv_spec import CsvSpec

class FeeService(Service):
    """ fee info handler """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None

    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    async def get_fee_args(self, garage_id, car_type):
        async with self._db.acquire() as conn:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            fee_rule = [dict(i.items()) async for i in await conn.execute(FeeRule.select().where(FeeRule.c.garage_id == garage_id)
            .where(FeeRule.c.car_type == car_type))]
            if len(fee_rule) == 0:
                return {"status": False}
            else:
                fee_rule = fee_rule[0]
                fee_para1 = [dict(i.items()) async for i in await conn.execute(FeePara.select()
                .where(FeePara.c.fee_rule_id == fee_rule['fee_rule_id']).where(FeePara.c.fee_para_mode == 'normal_day'))]
                fee_para2 = [dict(i.items()) async for i in await conn.execute(FeePara.select()
                .where(FeePara.c.fee_rule_id == fee_rule['fee_rule_id']).where(FeePara.c.fee_para_mode == 'holiday'))]
                fee_para1 = fee_para1[0]
                fee_para2 = fee_para2[0]
                data = {"status": True, "fee_rule": fee_rule, "fee_para1": fee_para1, "fee_para2": fee_para2}

                print('觀察回傳直')
                print(data)
                return data

    async def save_fee_args(self, fee_rule: dict, fee_para1: dict, fee_para2: dict):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            print('準備insert...')
            try:
                fee = await conn.execute(FeeRule.insert().values(fee_rule))
                fee_rule_id = fee.lastrowid
                fee_para1['fee_rule_id'] = fee_rule_id
                fee_para2['fee_rule_id'] = fee_rule_id
                await conn.execute(FeePara.insert().values(fee_para1))
                await conn.execute(FeePara.insert().values(fee_para2))
            except Exception as e:
                print(e)
                await trans.rollback()
            else:
                await trans.commit()
                return True

    async def update_fee_args(self, fee_rule: dict, fee_para1: dict, fee_para2: dict):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(FeeRule.update().values(fee_rule).where(FeeRule.c.fee_rule_id == fee_rule['fee_rule_id']))
                await conn.execute(FeePara.update().values(fee_para1).where(FeePara.c.fee_para_id == fee_para1['fee_para_id']))
                await conn.execute(FeePara.update().values(fee_para2).where(FeePara.c.fee_para_id == fee_para2['fee_para_id']))
            except Exception as e:
                print(e)
                await trans.rollback()
            else:
                await trans.commit()
                return True

    async def delete_fee_args(self, fee_rule_id: int):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(FeeRule.delete().where(FeeRule.c.fee_rule_id == fee_rule_id))
                await conn.execute(FeePara.delete().where(FeePara.c.fee_para_id == fee_rule_id))
                await conn.execute(FeePara.delete().where(FeePara.c.fee_para_id == fee_rule_id))
            except Exception as e:
                await trans.rollback()
            else:
                await trans.commit()
                return True

    async def export_fee_args(self, garage_id: str, car_type: str, driveway: int, data: dict):
        async with self._db.acquire() as conn:



            # get customer_code
            customer_code_sql = """ select customer_code from customer where customer_id = :customer_id """
            customer_code_result_proxy = await conn.execute(text(customer_code_sql), {'customer_id': self._user['customer_id']})
            customer_code = await customer_code_result_proxy.scalar()
            # get garage_code
            garage_code_sql = """ select garage_code from garage where garage_id = :garage_id """
            garage_code = await(await conn.execute(text(garage_code_sql), {'garage_id': garage_id})).scalar()
            # get device_car_type_group
            # 之後要用union把資料連起來
            print(data)
            # get export_path
            system_configuration_service = SystemConfigurationService(self._db, self._user)
            ftp_export_path = await system_configuration_service.get_system_configuration_by_key('ftp_device_export_csv')
            csv_handler = CsvHandler()
            csv_handler.export_fee_args_csv(ftp_export_path['value'], customer_code, garage_code, driveway, data)

    async def build_csv(self, garage_id: int, car_type: str):
        async with self._db.acquire() as conn:
            fee_rule = [dict(i.items()) async for i in await conn.execute(FeeRule.select()
            .where(FeeRule.c.car_type == car_type).where(FeeRule.c.garage_id == garage_id))]
            fee_rule = fee_rule[0]
            fee_rule_id = fee_rule['fee_rule_id']
            normal_day = [dict(i.items()) async for i in await conn.execute(FeePara.select().where(FeePara.c.fee_rule_id == fee_rule_id).where(FeePara.c.fee_para_mode == "normal_day"))]
            holiday = [dict(i.items()) async for i in await conn.execute(FeePara.select().where(FeePara.c.fee_rule_id == fee_rule_id).where(FeePara.c.fee_para_mode == "holiday"))]
            holiday = holiday[0]
            normal_day = normal_day[0]
            driveway = [dict(row.items()) async for row in await conn.execute(select([DeviceIboxArgs.c.ip])
            .where(DeviceIboxArgs.c.garage_id == garage_id).where(DeviceIboxArgs.c.type == car_type))]
            driveway = driveway[0]['ip'].split('.')
            driveway = driveway[len(driveway)-1]
            driveway = driveway.zfill(3)
            print('#############################################',driveway)
            csv_spec = CsvSpec()
            data = csv_spec.get_fee_args_export_csv_data(fee_rule, normal_day, holiday)
            print('剛組玩資料', data)
            await self.export_fee_args(garage_id, fee_rule['car_type'], driveway, data)
            

    async def get_special_day_list(self, year: int):
        async with self._db.acquire() as conn:
            print('aaaaaa')
            holiday = [dict(row.items()) async for row in await conn.execute(select([SpecialDay.c.date]).where(SpecialDay.c.year == year).where(SpecialDay.c.day_type == 1))]
            normal_day = [dict(row.items()) async for row in await conn.execute(select([SpecialDay.c.date]).where(SpecialDay.c.year == year).where(SpecialDay.c.day_type == 2))]
            print(holiday)
            print(normal_day)
            data = {'holiday': holiday, 'normal_day': normal_day}
            return data
