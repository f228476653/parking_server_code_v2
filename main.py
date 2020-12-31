"""Main script."""
import logging; logging.basicConfig(level=logging.INFO)
from os import environ

import argparse
import asyncio

from aiohttp import web
from app.config.application import app_config, show_db_version
from app.middlewares import MIDDLEWARES
from app.config.routes import map_routes
from aiohttp_swagger import *
#import uvloop

asyncio.set_event_loop_policy(None)
#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def main(args=()):
    """Start app."""
    parser = argparse.ArgumentParser(description='Run application.')

    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='application port.'
    )

    parser.add_argument(
        '--demo',
        help='populate demo data',
        action='store_true'
    )

    parser.add_argument(
        '--init',
        help='generate table scheme and insert default value',
        action='store_true'
    )

    parser.add_argument(
        '--prod',
        action='store_true',
    )

    parser.add_argument(
         '--env',
        type=str,
        default='develop',
        help='application port.'
    )

    parser.add_argument(
        '--db',
        type=str,
        nargs='+',
        help='handle db schema version'
    )

    parser.add_argument(
        '-v',
        action='store_const',
        const='kevin',
        help='show db schema version'
    )

    parser.add_argument(
        '-p',
        action='store_const',
        const='pmsplus-server',
        help='fast enable env.pms_plus_kevin'
    )

    args = parser.parse_args()
    
    app = web.Application(
        logger=logging,
        middlewares=MIDDLEWARES,
        client_max_size=20480**2
    )
    app['command_args'] = args

    app_config(app) #configre app ,like database, environment settings
    map_routes(app) #for cors requirest syncronized in order 
    if app['command_args'].v:
        show_db_version()
    else:
        setup_swagger(app, api_base_url='/', swagger_url="/api/doc", description="api/v1/doc")
        web.run_app(
            app,
            port=args.port,
            access_log=None
        )

if __name__ == '__main__':
    main()

