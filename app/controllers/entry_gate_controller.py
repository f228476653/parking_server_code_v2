import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.entry_gate_servcie import EntryGateService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class EntryGateController(Controller):
    
    async def add_entry_gate(self,request):
        
        db_service = EntryGateService(request.app['pmsdb'])
        post_data = await request.json()
        data = post_data.get('entry_gate')
        data['create_account_id']=request['login']['account_id']
        result = await db_service.add_entry_gate(data)
        api_response=ApiResponse([dict(result)][0])
        return self.json_response(api_response.asdict())
        
    async def update_entry_gate(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        
        post_data = await request.json()
        key = post_data.get('entry_gate')
        key['create_account_id']=request['login']['account_id']
        key['modified_account_id']=request['login']['account_id']
        result = await db_service.update_entry_gate(key)
        api_response=ApiResponse([dict(result)][0])
        return self.json_response(api_response.asdict())

    async def get_entry_gates(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        data = await db_service.get_entry_gates()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_entry_gates_total(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        data = await db_service.get_entry_gates_total()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_entry_gates_by_customer_id(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        customer_id=request.match_info['customer_id']
        data = await db_service.get_entry_gates_by_customer_id(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_entry_gates_by_garage_id(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        id=request.match_info['id']
        data = await db_service.get_entry_gates_by_garage_id(id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_entry_gates_by_id(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        id=request.match_info['id']
        data= await db_service.get_entry_gate_by_id(id)
        result = ApiResponse([dict(data)][0])
        return self.json_response(result.asdict())

    async def get_entry_gates_exist_by_garage_id(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        garage_id=request.match_info['garage_id']
        sn=request.match_info['sn']
        data = await db_service.get_entry_gates_by_garage_id_sn(garage_id,sn)
        if len(data) > 0:
            data= True
        else:
            data = False
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def delete_entry_gate_by_id(self,request):
        db_service = EntryGateService(request.app['pmsdb'])
        id=request.match_info['id']
        account_id=request['login']['account_id']
        result = await db_service.delete_entry_gate_by_id(id,account_id)
        return self.json_response(result)

    
    