import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.clock_in_and_out_service import ClockInAndOutService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class ClockInAndOutController(Controller): 
    async def add_clock_record(self,request):
        db_service = ClockInAndOutService(request.app['pmsdb'])
        post_data = await request.json()
        post_data['create_account_id']=request['login']['account_id']
        result = await db_service.add_clock_record(post_data)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

