import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.shift_checkout_service import ShiftCheckoutService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class ShiftCheckoutController(Controller):
    
    async def add_shift_checkout(self,request):
        db_service = ShiftCheckoutService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        post_data['create_account_id']=request['login']['account_id']
        result = await db_service.add_shift_checkout(post_data)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_shift_checkout_by_condition(self,request):
        db_service = ShiftCheckoutService(request.app['pmsdb'],request['login'])
        data = await request.json()
        data['query']['account_id'] = request['login']['account_id']
        result = await db_service.get_shift_checkout_by_condition(data['query'])
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())


    
    
