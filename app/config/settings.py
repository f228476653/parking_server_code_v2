"""Settings module."""

from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

class Settings:
    SETTINGS = None
    def _basepath(*args):
        return join(dirname(__file__), '../../', *args)

    async def load_environment(self,env="develop"):
        """Load env.{scope} file."""
        load_dotenv(Settings._basepath('config', 'env.{}'.format(
            environ.get('APP_ENV', env)
        )))
        
        self.SETTINGS = {
            'mongo': {
                'uri': environ.get('MONGO_URI'),
                'db': environ.get('MONGO_DB'),
            },
            'mysql':{
                'host': environ.get('MYSQL_HOST'),
                'dbname': environ.get('MYSQL_DBNAME'),
                'port': environ.get('MYSQL_PORT'),
                'username': environ.get('MYSQL_USERNAME'),
                'passwd': environ.get('MYSQL_PASSWD'),
                'autocommit': environ.get('MYSQL_AUTOCOMMIT')
            }
        }

        print(f'AioHttp Server is running in [ {env} ] Mode')
