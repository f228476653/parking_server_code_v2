import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.pms_data_uplaod_service import PmsDataUploadService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class PmsDataUploadController(Controller):
    
    async def add_pms_parking(self,request):
        db_service = PmsDataUploadService(request.app['pmsdb'])
        post_data = await request.json()
        #create_account = request['login']['account_id']
        result = await db_service.add_pms_parking(post_data,0)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def add_pms_lane(self,request):
        db_service = PmsDataUploadService(request.app['pmsdb'])
        post_data = await request.json()
        #create_account = request['login']['account_id']
        result = await db_service.add_pms_lane(post_data,0)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def add_pms_einvoice_number(self,request):
        db_service = PmsDataUploadService(request.app['pmsdb'])
        post_data = await request.json()
        #create_account = request['login']['account_id']
        result = await db_service.add_pms_einvoice_number(post_data,0)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def add_pms_trx_data(self,request):
        db_service = PmsDataUploadService(request.app['pmsdb'])
        post_data = await request.json()
        #create_account = request['login']['account_id']
        result = await db_service.add_pms_trx_data(post_data,0)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())


    
    
