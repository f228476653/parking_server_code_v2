import json
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.device_pv_service import DevicePvService

class DevicePvController(Controller):

    async def add_device_pv(self, request):
        device_pv = DevicePvService(request.app['pmsdb'])
        post_data = await request.json()
        customer_id = request['login']['customer_id']
        result = await device_pv.add_device_pv(customer_id, post_data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def show_all_device_pv_by_garage_id(self, request):
        device_pv = DevicePvService(request.app['pmsdb'])
        customer_id = request['login']['customer_id']
        garage_id = request.match_info['garage_id']
        result = await device_pv.show_all_device_pv_by_garage_id(customer_id, garage_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def show_device_pv_by_device_id(self, request):
        device_pv = DevicePvService(request.app['pmsdb'])
        customer_id = request['login']['customer_id']
        device_pv_id = request.match_info['device_pv_id']
        result = await device_pv.show_device_pv_by_device_id(customer_id, device_pv_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def update_device_pv_by_device_pv_id(self, request):
        device_pv = DevicePvService(request.app['pmsdb'])
        post_data = await request.json()
        customer_id = request['login']['customer_id']
        result = await device_pv.update_device_pv_by_device_id(customer_id, post_data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
      
    async def delete_device_pv_by_device_pv_id(self, request):
        device_pv = DevicePvService(request.app['pmsdb'])
        post_data = await request.json()
        customer_id = request['login']['customer_id']
        result = await device_pv.delete_device_pv_by_device_pv_id(customer_id, post_data['device_pv_id'])
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
