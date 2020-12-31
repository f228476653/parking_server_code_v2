import json
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.device_pad_service import DevicePadService

class DevicePadController(Controller):
    
    async def get_device_pad_by_garage_id(self, request):
        device_pad = DevicePadService(request.app['pmsdb'])
        garage_id = request.match_info['garage_id']
        result = await device_pad.get_device_pad_by_garage_id(garage_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
    