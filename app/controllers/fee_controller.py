import json
from datetime import datetime
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.managers.fee_manager import FeeManager

class FeeController(Controller):
 
    async def get_fee_args(self, request):
        fee_manager = FeeManager(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        car_type = request.match_info['car_type']
        fee_args = await fee_manager.get_fee_args(garage_id, car_type)
        api_response = ApiResponse(fee_args)
        return self.json_response(api_response.asdict())

    async def store_fee_args(self, request):
        #region
        """
        Description fee
        ---
        tags:
        - Fee
        summary: Fee
        description: store_fee args
        operationId: app.controllers.fee_controller.store_fee_args
        produces:
        - application/json
        parameters:
        - in: header
          description: login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: path
          name: customer_id
          description: custeomr table primary key
          required: true
          schema:
            type: integer
        - in: path
          name: device_type
          description: deviceType like iBox, PV3, Pad
          required: true
          schema:
            type: string
        responses:
          "200": {"data": true, "has_error": false, "message": "success"}
        """
        #endregion
        fee_manager = FeeManager(request.app['pmsdb'], request['login'])
        data = await request.json()
        result = await fee_manager.store_fee_args(data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def delete_fee_args(self, request):
        fee_manager = FeeManager(request.app['pmsdb'], request['login'])
        fee_rule_id = request.match_info['fee_rule_id']
        fee_args = await fee_manager.delete_fee_args(fee_rule_id)
        api_response = ApiResponse(fee_args)
        return self.json_response(api_response.asdict())

    async def get_special_day_list(self, request):
        fee_manager = FeeManager(request.app['pmsdb'], request['login'])
        year = request.match_info['year']
        data = await fee_manager.get_special_day_list(year)
        api_response = ApiResponse(data)
        return self.json_response(api_response.asdict())
      

