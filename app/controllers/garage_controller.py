import json
from datetime import datetime
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.garage_service import GarageService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler
from app.services.garage_management_service import GarageManagementService

class GarageController(Controller):
    
    async def add_garage(self,request):
        """
        Description Garage
        ---
        tags:
        - Garage
        summary: garageManagement
        description: add garage & garageDevcie
        operationId: app.controllers.GarageController.add_garage
        produces:
        - application/json
        parameters:
        - in: header
          description: login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          description: add garage & garageDevcie args
          name: body
          required: true
          schema:
            type: object
            properties:
            garage:
              type: object
              properties:
            iBox:
              type: object
              properties:
            device_type:
              type: array
            required:
                - garage
                - iBox
                - device_type
        responses:
            "200": 
              {
                "data": { "garage_id": 3 },
                "has_error": false,
                "message": "success"
              }
        """
        db_service = GarageManagementService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data = post_data.get('garage')
        data['create_account_id']=request['login']['account_id']
        #if not create by root , 只能建屬於自己的場站
        if request['login']['customer_id'] != 0:
            data['customer_id'] = request['login']['customer_id']
        result = await db_service.add_garage_and_garage_device_configuration(post_data)
        api_response=ApiResponse([dict(result)][0])
        return self.json_response(api_response.asdict())
        
    async def update_garage(self,request):
        """
        Description Garage
        ---
        tags:
        - Garage
        summary: garageManagement
        description: update garage & garageDevcie
        operationId: app.controllers.GarageController.update_garage
        produces:
        - application/json
        parameters:
        - in: header
          description: login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          description: update garage & garageDevcie args
          name: body
          required: true
          schema:
            type: object
            properties:
            garage:
              type: object
              properties:
            iBox:
              type: object
              properties:
            device_type:
              type: array
            required:
                - garage
                - iBox
                - device_type
        responses:
            "200": 
              {
                "data": 1,
                "has_error": false,
                "message": "success"
              }
        """
        db_service = GarageManagementService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        key = post_data.get('garage')
        key['modified_account_id']=request['login']['account_id']
        key['modified_date']=datetime.utcnow()
        result = await db_service.update_garage_and_garage_device_configuration(post_data)
        api_response=ApiResponse(1)
        return self.json_response(api_response.asdict())

    async def get_garages(self,request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        data = await db_service.get_garages()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_garage_by_id(self,request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        garage_id=request.match_info['garage_id']
        data = await db_service.get_garage_by_id(garage_id)
        api_response=ApiResponse([dict(data)][0])
        return self.json_response(api_response.asdict())

    async def get_garages_total(self,request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        data = await db_service.get_garages_total()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_garages_by_customer_id(self,request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        customer_id=request.match_info['customer_id']
        data = await db_service.get_garages_by_customer_id(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def delete_garage_by_id(self,request):
        db_service = GarageManagementService(request.app['pmsdb'],request['login'])
        id=request.match_info['id']
        account_id=request['login']['account_id']
        result = await db_service.delete_garage_and_garage_device_configuration(id,account_id)
        return self.json_response(result)

    async def get_garage_amount_by_customer_id(self, request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        customer_id = request.match_info['customer_id']
        result = await db_service.get_garage_amount_by_customer_id(customer_id)
        return self.json_response(result)

    async def is_garage_name_exit(self, request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        garage_name = request.match_info['garage_name']
        result = await db_service.is_garage_name_exit(garage_name)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_garages_by_garage_group_id(self, request):
        """ get group garage """
        garage_group_id=request.match_info['garage_group_id']
        account_id=request['login']['account_id']
        db_service = GarageService(request.app['pmsdb'],request['login'])
        garage = await db_service.get_garages_by_garage_group_id(garage_group_id,account_id)
        api_response = ApiResponse(garage)
        return self.json_response(api_response.asdict())

    async def is_garage_code_exist(self, request):
        """ check garage_code is exist  """
        garage_code=request.match_info['garage_code']
        print('即將執行')
        account_id=request['login']['account_id']
        db_service = GarageService(request.app['pmsdb'],request['login'])
        print('aaaaaaaa')
        result = await db_service.is_garage_code_exist(garage_code, account_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_pad_garage_args_garage_id(self, request):
        db_service = GarageService(request.app['pmsdb'],request['login'])
        garage_id = request.match_info['garage_id']
        result = await db_service.get_pad_garage_args_garage_id(garage_id)
        api_response=ApiResponse([dict(result)][0])
        return self.json_response(api_response.asdict())

    async def update_garage_capacity(self, request):
      #region comment
      """
        Description Garage
        ---
        tags:
        - Garage
        summary: Garage
        description: update garage capacity information.
        operationId: app.controllers.garage_controller.update_garage_capacity
        produces:
        - application/json
        parameters:
        - in: header
          description: login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: update garage capacity information.
          required: true
          schema:
            type: object
            properties:
              current_capacity_sedan:
                type: int
                description: current capaicity of sedan
                example: 10
              current_capacity_suv:
                type: int
                description: current capaicity of suv
                example: 10
              current_capacity_bicycle:
                type: int
                description: current capaicity of bicycle
                example: 10
              current_capacity_motocycle:
                type: int
                description: current capaicity of motocycle
                example: 10
              current_capacity_truck:
                type: int
                description: current capaicity of truck
                example: 10
              current_capacity_bus:
                type: int
                description: current capaicity of bus
                example: 10
              current_capacity_bus:
                type: int
                description: current capaicity of bus
                example: 10
              current_capacity_total:
                type: int
                description: current capaicity of total ,which is ignoring type of parking lot
                example: 10
              gov_id:
                type: string
                description: government provided code/id
                example: 10
              current_capacity_updatetime:
                type: date
                description: the update timestamp,please udpate with UTC (UTC)
                example: '2017-01-01 10:53:54'
              garage_id:
                type: int
                description: garage id provide by system
                example: '1'
            required:
                - current_capacity_updatetime
                - garage_id
                - current_capacity_total
        responses:
        "200":
          {
    "data": 0 //update row count,
    "has_error": false,
    "message": "success"
}
        """
      #endregion
      db_service = GarageService(request.app['pmsdb'],request['login'])
      post_data = await request.json()
      result = await db_service.update_garage_capacity(
        post_data.get('current_capacity_sedan')
        ,post_data.get('current_capacity_suv')
        ,post_data.get('current_capacity_bicycle')
        ,post_data.get('current_capacity_motocycle')
        ,post_data.get('current_capacity_truck')
        ,post_data.get('current_capacity_bus')
        ,post_data.get('current_capacity_total')
        ,post_data.get('gov_id')
        ,request['login'].account_id
        ,post_data.get('current_capacity_updatetime')
        ,post_data.get('garage_id')
      )
      api_response = ApiResponse(result)
      return self.json_response(api_response.asdict())




    
