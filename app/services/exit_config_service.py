import aiomysql.sa
from sqlalchemy import desc, text
from app.services.systemlog_service import SystemlogService
from sqlalchemy.sql import and_,or_,not_, join, select, insert
from app.config.models import ExitConfig, Garage, ExitTypeConfigDetail
class ExitConfigService:
    """ handle exit_config page info """
    _db = None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    async def get_all_exit_config_by_customer_id(self, customer_id: int):
        """ 取得已設定場站的出場相關資訊 """
        exit_config={}
        async with self._db.acquire() as conn:
            query_column = """select e.description, e.exit_config_id, disabled, g.garage_id, g.garage_name, g.garage_code 
            from exit_config as e left join garage g 
            on g.garage_id = e.garage_id
            join customer a 
            on g.customer_id = a.customer_id
            where e.is_configured = 1 """
            customer_clause = "and a.customer_id = :customer_id"
            if customer_id != 0:
                query_column += customer_clause
            query_result = [dict(row.items()) async for row in await conn.execute(text(query_column), { 'customer_id' : customer_id})]
            exit_config['garage'] = query_result
            # 取得場站群組名稱
            exit_config['groupname'] = await self.get_garage_groupname_by_customer_id(customer_id)
            for i in query_result:
                # 取得場站 出場設定
                i['exit_type'] = await self.get_exit_types_by_exit_config_id(i['exit_config_id'])
            return exit_config

    async def get_garage_groupname_by_customer_id(self, customer_id):
        """ get distinct group_name """
        async with self._db.acquire() as conn:
            groups_sql = """select DISTINCT garage_group_name from garage_group g
            where garage_group_id in ( select garage_group_id
                                       from map_garage_to_garage_group m join garage g
                                       on g.garage_id = m.garage_id """
            if customer_id != 0:   
                customer_clause = "and g.customer_id = :customer_id )"
                groups_sql += customer_clause
            else:
                groups_sql += ")"
            group = [dict(row.items()) async for row in await conn.execute(text(groups_sql),{'customer_id' : customer_id})]
            result = []
            for i in group:
                result.append(i['garage_group_name'])
            return result

    async def get_garages_by_group_name(self, group_name):
        """ get group garage_info """
        condition_sql = '' if group_name.lower() == 'all' else ' where garage_group_name = :group_name '
        get_garage_sql =  """ select g.garage_id, g.garage_name, g.garage_code 
                                 from garage g right join (
                                                            select * from map_garage_to_garage_group 
                                                            where garage_group_id in (
                                                                                      select garage_group_id 
                                                                                      from garage_group """ + condition_sql + """)
                                                          ) as m 
                                 on g.garage_id = m.garage_id;"""
        async with self._db.acquire() as conn:
            result = [dict(row.items()) async for row in await conn.execute(text(get_garage_sql), {'group_name': group_name})]
            return result

    async def get_exit_types_by_exit_config_id(self, exit_config_id: int):
        async with self._db.acquire() as conn:
            return [dict(row.items()) async for row in await conn.execute(ExitTypeConfigDetail.select().where(ExitTypeConfigDetail.c.exit_config_id == exit_config_id).where(ExitTypeConfigDetail.c.exit_type_disabled == 0))]

    async def get_exit_type_info_by_garage_id(self, garage_id):
        """ 使用garage_id 取得 出場管理資訊"""
        garage_info = {}
        async with self._db.acquire() as conn:
            get_exit_config_info_sql = """  
                                   select e.description, g.garage_name, g.garage_code
                                   from garage as g left join exit_config as e
                                   on g.garage_id = e.garage_id
                                   where g.garage_id = :garage_id ;"""
            garage_info['garage'] = [dict(row.items()) async for row in await conn.execute(text(get_exit_config_info_sql), {"garage_id": garage_id})]
            for i in garage_info['garage']:
                garage_info['exit_type'] = await self.get_exit_types_by_exit_config_id(garage_id)
            return garage_info
            
    async def disable_exit_config_by_exit_config_id(self, disabled):
        async with self._db.acquire() as conn:
            result = await conn.execute(ExitConfig.update().values(disabled).where(ExitConfig.c.exit_config_id == disabled['exit_config_id']))
            return result.rowcount
    
    async def reset_exit_config_by_exit_config_id(self, init_data) -> bool:
        """ reset exit_config and exit_type_config_deatil"""
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result1 = await conn.execute(ExitConfig.update().values(init_data['exit_config_data']).where(ExitConfig.c.exit_config_id == init_data['exit_config_id']))
                result2 = await conn.execute(ExitTypeConfigDetail.update().values(init_data['exit_type_hidden']).where(ExitTypeConfigDetail.c.exit_config_id == init_data['exit_config_id']))
            except Exception as e:
                await trans.rollback()
                print(e)
                raise Exception() 
            else:
                await trans.commit()
                return True

    async def get_exit_config_detail_last_update(self , garage_id):
        async with self._db.acquire() as conn:
            sql = f"""select max(update_time) as time from exit_type_config_detail 
            where exit_config_id =(select exit_config_id from exit_config where garage_id =:garage_id) 
            and exit_type_disabled ='0' """
            max_time = await(await conn.execute(text(sql),{'garage_id':garage_id})).fetchone()
            max_time = max_time['time']
        return max_time is None and '1980-01-01 00:00:00' or max_time

    async def update_exit_type_by_exit_config_id(self, exit_type_data, insert_data):
        """ 新增或修改出場設定 """
        async with self._db.acquire() as conn:
            trans =await conn.begin()
            try:
                if (exit_type_data['exit_config']['exit_config_id'] == 0):
                    insert_exit_config_pk = await conn.execute(ExitConfig.insert().values(insert_data))
                # handle description column
                result1 = await conn.execute(ExitConfig.update().values(exit_type_data['exit_config']).where(ExitConfig.c.exit_config_id == exit_type_data['exit_config']['exit_config_id']))
                # delete exit_type_config_detail table
                if len(exit_type_data['exit_type_config_detail']['exit_type']) != 0 :
                    delete_exit_type_sql = """ delete from exit_type_config_detail where exit_type_config_detail_id = :exit_type_config_detail_id;"""
                    for i in exit_type_data['exit_type_config_detail']['exit_type_config_detail_id']:
                        result2 = await conn.execute(text(delete_exit_type_sql), {"exit_type_config_detail_id" : i})
                # insert exit_type_config_detail table 
                add_exit_type_sql = """ insert into exit_type_config_detail (exit_type, exit_config_id) values (:exit_type, :exit_config_id);"""
                for i in exit_type_data['exit_type_config_detail']['exit_type']:
                    result3 = await conn.execute(text(add_exit_type_sql), {'exit_type' : i, 'exit_config_id' : exit_type_data['exit_config']['exit_config_id']})
            except Exception as e:
                print('有錯')
                print(e)
                await trans.rollback()
                raise Exception() 
            else:
                await trans.commit()
                return True
