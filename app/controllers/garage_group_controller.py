import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.garage_group_service import GarageGroupService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class GarageGroupController(Controller):
    
    async def add_garage_group(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data = post_data.get('garage_group')
        garages = post_data.get('garages')
        data['create_account_id']=request['login']['account_id']
        result = await db_service.add_garage_group(data,garages)
        api_response=ApiResponse([dict(result)][0])
        return self.json_response(api_response.asdict())

    async def get_garage_groups(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        data = await db_service.get_garage_groups()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_garage_groups_by_customer_id(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        customer_id =request.match_info['customer_id']
        data = await db_service.get_garage_groups_by_customer_id(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_garage_groups_by_account_id(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        account_id = request['login']['account_id']
        data = await db_service.get_garage_groups_by_account_id(account_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_map_garage_to_garage_group_by_garage_group_id(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        id = request.match_info['id']
        data = await db_service.get_map_garage_to_garage_group_by_garage_group_id(id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_garage_group_by_id(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        garage_group_id =request.match_info['id']
        data = await db_service.get_garage_group_by_id(garage_group_id)
        result = ApiResponse([dict(data)][0])
        return self.json_response(result.asdict())
        
    async def update_garage_group(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data = post_data.get('garage_group')
        garages = post_data.get('garages')
        data['create_account_id']=request['login']['account_id']
        data['modified_account_id']=request['login']['account_id']
        result = await db_service.update_garage_group(data, garages)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_garages(self,request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        data = await db_service.get_garages()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_garages_total(self,request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        data = await db_service.get_garages_total()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())


    async def delete_garage_group_by_id(self,request):
        db_service = GarageGroupService(request.app['pmsdb'],request['login'])
        id=request.match_info['id']
        account_id=request['login']['account_id']
        result = await db_service.delete_garage_group_by_id(id,account_id)
        return self.json_response(result)
        

    

    
