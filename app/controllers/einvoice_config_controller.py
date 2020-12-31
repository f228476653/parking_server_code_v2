import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.einvoice_config_service import EinvoiceConfigService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class EinvoiceConfigController(Controller):

    async def get_garage_einvoice_config(self,request):
        db_service = EinvoiceConfigService(request.app['pmsdb'])
        garage_id=request.match_info['garage_id']
        result = await db_service.get_garage_einvoice_config(garage_id)
        api_response =ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def get_customer_level_einvoice_config(self,request):
        db_service = EinvoiceConfigService(request.app['pmsdb'])
        customer_id=request.match_info['customer_id']
        result = await db_service.get_customer_level_einvoice_config(customer_id)
        api_response =ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def add_customer_level_einvoice_config(self,request):
        db_service = EinvoiceConfigService(request.app['pmsdb'])
        post_data = await request.json()
        config = post_data.get('einvoice_configs')
        customer_id = post_data.get('customer_id')
        #config['create_account_id']=request['login']['account_id']
        #config['customer_id'] = request['login']['customer_id']
        one = await db_service.add_customer_level_einvoice_config(config,customer_id)
        api_response=ApiResponse(one)
        return self.json_response(api_response.asdict())
    
    async def update_customer_level_einvoice_config(self,request):
        db_service = EinvoiceConfigService(request.app['pmsdb'])
        post_data = await request.json()
        config = post_data.get('einvoice_configs')
        customer_id = post_data.get('customer_id')
        print(f'===----{customer_id}')
        #config['create_account_id']=request['login']['account_id']
        #config['customer_id'] = request['login']['customer_id']
        one = await db_service.update_customer_level_einvoice_config(config,customer_id)
        api_response=ApiResponse(one)
        return self.json_response(api_response.asdict())