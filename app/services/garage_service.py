
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account,Role,Permission,GaragePadArgs,Map_Role_Permission,Garage,Map_Garage_To_Garage_Group,GarageGroup

from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler

class GarageService:
    """ every thing about garage"""
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

    async def get_garages(self):
        """get garage list"""
        print(self._user.is_superuser)
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                # garages = [dict(row.items()) async for row in await conn.execute(Garage.select().order_by(desc(Garage.c.create_date)))]
                sql = """ SELECT g.*, c.company_name FROM garage AS g LEFT JOIN customer AS c ON g.customer_id = c.customer_id ORDER BY g.create_date DESC"""
                garages = [dict(row.items()) async for row in await conn.execute(text(sql))]
            else:
                garages = await self.get_garages_by_customer_id(self._user.customer_id)
            return garages

    async def get_garages_by_garage_name(self, garage_name: str):
        """get garage list"""
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                # garages = [dict(row.items()) async for row in await conn.execute(Garage.select().order_by(desc(Garage.c.create_date)))]
                sql = """ SELECT g.*, c.company_name FROM garage AS g LEFT JOIN customer AS c ON g.customer_id = c.customer_id ORDER BY g.create_date DESC"""
                garages = [dict(row.items()) async for row in await conn.execute(text(sql))]
            else:
                garages = await self.get_garages_by_customer_id(self._user.customer_id)
            return garages

    async def is_garage_name_exit(self, garage_name:str):
        """ to check an account is exist or not """
        async with self._db.acquire() as conn:
            result= [dict(row.items()) async for row in await conn.execute(
                    Garage.select().where((Garage.c.garage_name == garage_name)))
                ]
            return len(result) >0 and True or False

    async def get_garages_by_customer_id(self,customer_id):
        """ get all garages """
        async with self._db.acquire() as conn:
            # garage = [dict(row.items()) async for row in await conn.execute(Garage.select().where(Garage.c.customer_id == customer_id).order_by(desc(Garage.c.create_date)))]
            sql = """ SELECT g.*, c.company_name FROM garage AS g LEFT JOIN customer AS c ON g.customer_id = c.customer_id WHERE g.customer_id=:customer_id ORDER BY g.create_date DESC"""
            garage = [dict(row.items()) async for row in await conn.execute(text(sql),{'customer_id':customer_id})]
            return garage

    async def get_garages_total(self):
        """ get all garages count"""
        async with self._db.acquire() as conn:
            s = await (await conn.execute(Garage.count())).scalar()
            return s
    
    async def get_garage_by_id(self,id):
        """ get permission by id """
        async with self._db.acquire() as conn:
            queryResult= await conn.execute(Garage.select().where((Garage.c.garage_id == id)))
            result= await queryResult.fetchone()
            return result

    async def get_garages_by_garage_group_id(self,garage_group_id,account_id ) ->[Garage]:
        """get garages by garage_group_id"""
        async with self._db.acquire() as conn:
            if not self._user.is_superuser and garage_group_id =='all':
                sql = """select * from garage where garage_id in (
	                            select garage_id from map_garage_to_garage_group where garage_group_id in(
		                            select garage_group_id from map_garage_group_to_account where account_id=:account_id 
	                            )
                            )
                    """
                queryResult= [dict(row.items()) async for row in await conn.execute(text(sql),{'account_id':account_id})]
                return queryResult
            elif  garage_group_id == 'all' and self._user.is_superuser:
                sql = """select * from garage"""
                queryResult=  [dict(row.items()) async for row in await conn.execute(sql)]
            else:
                sql = "select * from garage where garage_id in (select garage_id from map_garage_to_garage_group where garage_group_id=:garage_group_id)"
                queryResult=  [dict(row.items()) async for row in await conn.execute(text(sql),{'garage_group_id':garage_group_id})]
         
            return queryResult

    async def get_garage_amount_by_customer_id(self,customer_id):
        async with self._db.acquire() as conn:
            queryResult = await conn.execute(Garage.count().where(Garage.c.customer_id == customer_id))
            result= await queryResult.scalar()
            return result

    async def add_garage(self,garage, conn2):
        self._syslog['create_account_id']=garage['create_account_id']
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']=  json.dumps(garage,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        # async with self._db.acquire() as conn:
        result = await conn2.execute(Garage.insert().values(garage))
        # r = await self.get_garage_by_id(result.lastrowid)
        # 不使用lastrowid 因為交易完成前會得到None 無法使用transaction 來insert garage_ibox_args;
        r = [dict(i.items()) async for i in await conn2.execute('SELECT LAST_INSERT_ID() as garage_id')]
        # ex: r = [{'garage_id': 4}]
        return r

    async def update_garage(self,garage) -> int:
        self._syslog['create_account_id']=garage['modified_account_id']
        self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
        self._syslog['event_message']= json.dumps(garage,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Garage.update().values(garage).where(Garage.c.garage_id == garage['garage_id']))
            return result.rowcount

    async def delete_garage_by_id(self, id, account_id, conn) -> bool:
        self._syslog['create_account_id']=account_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']= 'delete_garage_by_id: id = : '+ id
        result = await self._log_service.addlog(self._syslog)
        #async with self._db.acquire() as conn:
        result = await conn.execute(Garage.delete().where((Garage.c.garage_id == id)))
        result2 = await conn.execute(Map_Garage_To_Garage_Group.delete().where((Map_Garage_To_Garage_Group.c.garage_id == id)))
        return True
    
    async def get_garage_latest_update_date_by_garage_id(self,garage_id:int):
        result = await self.get_garage_by_id(garage_id)
        return result is None and '1980-01-01 00:00:00' or str(result[48])

    async def get_garage_by_garage_code(self, garage_code: str, account_id):
        self._syslog['create_account_id'] = account_id
        self._syslog['event_id'] = SystemEventType.SELECT_GARAGE_BY_CODE.value
        self._syslog['event_message'] = 'query garage by garage_code : garage_code = : '+ garage_code
        result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            garage = await conn.execute(Garage.select().where(Garage.c.garage_code == garage_code))
            return garage

    async def is_garage_code_exist(self, garage_code: str, account_id) -> bool:
        garage = await self.get_garage_by_garage_code(garage_code, account_id)
        return True if garage.rowcount != 0 else False

    async def get_garage_pad_args_last_update(self,garage_id):
        args = await self.get_pad_garage_args_garage_id(garage_id)
        print(type(args))
        print(args)
        return args['update_time'] is None and '1980-01-01 00:00:00' or args['update_time']

    async def get_pad_garage_args_garage_id(self,garage_id):
        async with self._db.acquire() as conn:
            args = await(await conn.execute(GaragePadArgs.select().where(GaragePadArgs.c.garage_id == garage_id))).fetchone()
            return args


    async def update_garage_capacity(self,current_capacity_sedan, current_capacity_suv, current_capacity_bicycle, current_capacity_motocycle
        , current_capacity_truck, current_capacity_bus, current_capacity_total, gov_id, current_capacity_update_account_id
        , current_capacity_updatetime, garage_id) -> int:
        async with self._db.acquire() as conn:
            params = {
                'current_capacity_sedan':current_capacity_sedan
                ,'current_capacity_suv':current_capacity_suv
                ,'current_capacity_bicycle':current_capacity_bicycle
                ,'current_capacity_motocycle':current_capacity_motocycle
                ,'current_capacity_truck':current_capacity_truck
                ,'current_capacity_bus':current_capacity_bus
                ,'current_capacity_total':current_capacity_total
                ,'gov_id':gov_id
                ,'current_capacity_update_account_id':current_capacity_update_account_id
                ,'current_capacity_updatetime':current_capacity_updatetime
                ,'garage_id':garage_id
            }
            result = await conn.execute(text("""
                update garage set current_capacity_sedan=:current_capacity_sedan
                ,current_capacity_suv =:current_capacity_suv
                ,current_capacity_bicycle=:current_capacity_bicycle
                ,current_capacity_motocycle=:current_capacity_motocycle
                ,current_capacity_truck=:current_capacity_truck
                ,current_capacity_bus=:current_capacity_bus
                ,current_capacity_total=:current_capacity_total
                ,gov_id=:gov_id
                ,current_capacity_update_account_id=:current_capacity_update_account_id
                ,current_capacity_updatetime=:current_capacity_updatetime
                where garage_id=:garage_id
                """),params
                )
            return result.rowcount