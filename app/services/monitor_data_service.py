import pymysql.cursors
from app.services.systemlog_service import SystemlogService
from app.config.models import Garage_Ftp_Info
from sqlalchemy.sql import select

class MonitorDataService():
    """ monitor data from parser  """
    _db =None

    def __init__(self, db):
        self._db = db

    async def check_pms_pmsplus_diff(self):
        async with self._db.acquire() as conn:
            pms_plus_info = [dict(row.items()) async for row in  await conn.execute(Garage_Ftp_Info.select().where(Garage_Ftp_Info.c.is_active == '0')) ] 
            for d in pms_plus_info:
                print(f'----------------{d}')
                self.select_garage_db(d)

    def select_garage_db(connection_dict):
        # Connect to the database
        connection = pymysql.connect(host=connection_dict['ftp_ip'],
                        user=connection_dict['ftp_userid'],
                        password=connection_dict['ftp_pwd'],
                        db='db',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            connection.close()