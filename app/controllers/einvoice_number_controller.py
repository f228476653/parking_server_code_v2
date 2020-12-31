import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.einvoice_number_service import EinvoiceService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class EinvoiceController(Controller):
    
    async def add_einvoice(self,request):
        db_service = EinvoiceService(request.app['pmsdb'])
        post_data = await request.json()
        data = post_data.get('einvoice')
        in_or_out = post_data.get('in_or_out')
        account_id=request['login']['account_id']
        #data['create_account_id']=request['login']['account_id']
        result = await db_service.add_einvoice(in_or_out,account_id,data)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def update_einvoice(self,request):
        db_service = EinvoiceService(request.app['pmsdb'])
        data = await request.json()
        data['update_user']=request['login']['account_id']
        result = await db_service.update_einvoice(data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())


    async def delete_einvoice(self,request):
        db_service = EinvoiceService(request.app['pmsdb'])
        parking_id=request.match_info['parking_id']
        in_or_out=request.match_info['in_or_out']
        account_id=request['login']['account_id']
        result = await db_service.delete_einvoice(in_or_out,parking_id,account_id)
        api_response =ApiResponse(result)
        return self.json_response(api_response.asdict())

