import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.original_real_time_transaction_service import OriginalRealTimeTransactionService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class OriginalRealTimeTransactionController(Controller):


    async def query_transaction(self,request):
        db_service = OriginalRealTimeTransactionService(request.app['pmsdb'],request['login'])
        customer_id = request['login']['customer_id']
        post_data = await request.json()
        data = post_data.get('page_query')
        result = await db_service.query_transaction(data,customer_id)
        #print(result)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    
