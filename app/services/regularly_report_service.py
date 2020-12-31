import aiomysql.sa
from sqlalchemy import text
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import select
from app.config.models import Account, DayRevenueView, Garage
from app.services.service import Service
from app.services.system_configuration import SystemConfigurationService
from app.config.system_event_type import SystemEventType

class RegularlyReportService(Service):
    """ day_revenue data handler """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None

    def __init__(self, db, user):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    async def get_monthly_usage_report(self, garage_code, monthly):
        async with self._db.acquire() as conn:
            total_capacity = await(await conn.execute(select([Garage.c.total_capacity]).where(Garage.c.garage_code == garage_code))).scalar()
            print('**&*&*&*&*&*&', garage_code)
            print('該場站總車道數(total_capacity):', total_capacity)
            query_sql = """ select the_hour, truncate(ifnull((car_csum*100/:total_capacity), 0), 2) as car_csum from hour_car_csum where left(the_hour, 7) = :monthly and  garage_code = :garage_code order by the_hour """
            data = [dict(row.items()) async for row in await conn.execute(text(query_sql), {'total_capacity': total_capacity, 'monthly': monthly, 'garage_code': garage_code})]
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', data)
            return data

    async def get_monthly_revenue_report(self, garage_code, the_month, paid_type):
        async with self._db.acquire() as conn:
            monthly_revenue_report = {}
            print('start !!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if paid_type == 'all':
                monthly_revenue_report['icash_c'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'c', '02')
                monthly_revenue_report['icash_m'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'm', '02')
                monthly_revenue_report['ipass_c'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'c', '03')
                monthly_revenue_report['ipass_m'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'm', '03')
                monthly_revenue_report['yhdp_c'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'c', '05')
                monthly_revenue_report['yhdp_m'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'm', '05')
                monthly_revenue_report['cash_c'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'c', '99')
                monthly_revenue_report['cash_m'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'm', '99')
            else:
                monthly_revenue_report['paid_type_c'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'c', paid_type)
                monthly_revenue_report['paid_type_m'] = await self.get_monthly_revenue_sum_type(garage_code, the_month, 'm', paid_type)
            print('觀察')
            print('end !!!!!!!!!!!!!!!!!!!!!!!!!!')
            return monthly_revenue_report

    async def get_day_revenue_report(self, garage_code, the_day, paid_type):
        async with self._db.acquire() as conn:
            day_revenue_report = {}
            day_revenue_report['day_revenue'] = await self.get_day_revenue(garage_code, the_day, paid_type)
            day_revenue_report['day_revenue_sum'] = await self.get_day_revenue_sum(garage_code, the_day, paid_type)
            day_revenue_report['day_revenue_sum_c'] = await self.get_day_revenue_sum_type(garage_code, the_day, 'c', paid_type)
            day_revenue_report['day_revenue_sum_m'] = await self.get_day_revenue_sum_type(garage_code, the_day, 'm', paid_type)
            day_revenue_report['day_revenue_sum_t'] = await self.get_day_revenue_sum_type(garage_code, the_day, 't', paid_type)
            print('觀察')
            print(day_revenue_report['day_revenue'])
            print(day_revenue_report['day_revenue_sum'])
            print(day_revenue_report['day_revenue_sum_c'])
            print(day_revenue_report['day_revenue_sum_m'])
            print(day_revenue_report['day_revenue_sum_t'])
            print('end!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return day_revenue_report

    
    async def get_monthly_revenue_sum_type(self, garage_code: str,  the_month: str, car_type: str, paid_type: str):
        async with self._db.acquire() as conn:
            sql = """ select parking_date, sum(total_cnt) as total_cnt, sum(total) as total
                       from day_revenue_sum_type where left(parking_date, 7) = :parking_date
                       and garage_code = :garage_code and type = :car_type and paid_type = :paid_type
                       group by parking_date order by parking_date """
            where_clause = {"garage_code": garage_code, "parking_date": the_month, "car_type": car_type, "paid_type": paid_type}
            print('觀察sql::::::::::::::::', sql)
            data = [dict(row.items()) async for row in await conn.execute(text(sql), where_clause)]
            print(data)
            return data

    async def get_day_revenue(self, garage_code,  the_date, paid_type):
        async with self._db.acquire() as conn:
            sql = "select fee, sum(cnt) as cnt, sum(subtotal) as subtotal from day_revenue where garage_code = :garage_code and parking_date = :parking_date "
            where_clause = {"garage_code": garage_code, "parking_date": the_date}
            if not paid_type == "all":
                sql += " and paid_type = :paid_type"
                where_clause["paid_type"] = paid_type
            sql += " group by fee order by fee"
            print('觀察sql::::::::::::::::', sql)
            data = [dict(row.items()) async for row in await conn.execute(text(sql), where_clause)]
            print(type(data))
            print(data)
            return data

    async def get_day_revenue_sum(self, garage_code,  the_date, paid_type):
        async with self._db.acquire() as conn:
            sql = "select sum(total_cnt) as total_cnt, sum(total) as total from day_revenue_sum where garage_code = :garage_code and parking_date = :parking_date"
            where_clause = {"garage_code": garage_code, "parking_date": the_date}
            if not paid_type == "all":
                sql += " and paid_type = :paid_type"
                where_clause["paid_type"] = paid_type
            sql += " group by parking_date order by parking_date"
            print('觀察sql::::::::::::::::', sql)
            data = [dict(row.items()) async for row in await conn.execute(text(sql), where_clause)]
            print(data)
            return data

    async def get_day_revenue_sum_type(self, garage_code,  the_date, car_type, paid_type):
        async with self._db.acquire() as conn:
            sql = "select parking_date, sum(total_cnt) as total_cnt, sum(total) as total from day_revenue_sum_type where garage_code = :garage_code and parking_date = :parking_date and type = :car_type "
            where_clause = {"garage_code": garage_code, "parking_date": the_date, "car_type": car_type}
            if not paid_type == "all":
                sql += " and paid_type = :paid_type"
                where_clause["paid_type"] = paid_type
            sql += " group by parking_date order by parking_date"
            print('觀察sql::::::::::::::::', sql)
            data = [dict(row.items()) async for row in await conn.execute(text(sql), where_clause)]
            print(data)
            return data


