import json, asyncio
from datetime import datetime
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.device_ibox_service import DeviceIboxService
from app.managers.device_manager import DeviceManager
# from aiohttp_sse import sse_response

class DeviceController(Controller):
 
    async def get_customer_device_by_customer_id(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: customerDevice
        description: get customerDeviceArgs
        operationId: app.controllers.device_controller.get_customer_device_by_customer_id
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
        "200":
          {
            "data": {
                "iBox": {
                    "customer_ibox_args_id": 1,
                    "market_code": "P21",
                    "cashier_no": "A110",
                    "system_id": "42",
                    "comp_id": "29",
                    "machine": "4D3C2B1A",
                    "ipass_water_lv_host": "192.168.0.101",
                    "ipass_water_lv_port": 8988,
                    "socket_ip": "10.20.1.74",
                    "transaction_system_id": "00",
                    "loc_id": "02",
                    "transaction_terminal_no": "471F6241",
                    "tid": "00000002",
                    "mid": "0000000000000000",
                    "YHDP_water_lv": 3000,
                    "YHDP_water_lv_host": "192.168.0.101",
                    "YHDP_water_lv_port": 6666,
                    "nii": 667,
                    "client_pv": "192.168.53.201,192.168.53.202",
                    "time_sync_period": 24,
                    "update_time": "2018-06-21 03:57:08",
                    "update_user": "root",
                    "customer_id": 0
                },
                "card_case": {
                    "customer_map_card_case_id": 1,
                    "device_type": "iBox",
                    "enable_card_case": 7,
                    "customer_id": 0
                }
            },
            "has_error": false,
            "message": "success"
          }
        """
        #endregion
        device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
        check_customer_id = request['login']['customer_id']
        device_type = request.match_info['device_type']
        customer_id = request.match_info['customer_id']
        customer_args = {}
        # 取得該廠商 該設備所使啟用的卡種資訊 如果沒有則回傳None
        card_case =  await device_ibox.get_customer_map_card_case_by_customer_id_and_device_type(customer_id, device_type)
        customer_args[device_type] = await device_ibox.get_customer_device_argument_by_customer_id(customer_id, device_type)
        customer_args['card_case'] = card_case
        api_response = ApiResponse(customer_args)
        return self.json_response(api_response.asdict())

    async def add_or_update_customer_device_args(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: customerDevice
        description: add_or_update customerDeviceArgs
        operationId: app.controllers.device_controller.add_or_update_customer_device_args
        produces:
        - application/json
        parameters:
        - in: header
          description: header login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: customer device data
          required: true
          schema:
            type: object
            properties:
              device_type:
                type: string
                example: iBox
              customer_id:
                type: integer
                example: 0
              card_case:
                type: object
                example:
                  customer_id: 0
                  customer_map_card_case_id: 1
                  device_type: "iBox"
                  enable_card_case: 7
              bean:
                type: object
                example:
                  YHDP_water_lv: 3000
                  YHDP_water_lv_host: "192.168.0.101"
        responses:
            "200": {"data": true, "has_error": false, "message": "success"}
        """
        #endregion
        device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
        check_customer_id = request['login']['customer_id']
        post_data = await request.json()
        customer_id = post_data['customer_id']
        if customer_id != check_customer_id and check_customer_id != 0:
            # 代表不是該廠商或超級帳號
            raise PermissionError("check_account_has_authorization_to_use_save_customer_device_args", "not permit to quesry other customer's data")
        device_type = post_data['device_type']
        result = True
        if 'card_case' in post_data:
            card_case = post_data['card_case']       
            result1 = await device_ibox.save_customer_map_card_case(check_customer_id, customer_id, card_case, device_type)
            result = result & result1
        if 'bean' in post_data:
            bean = post_data['bean']
            bean['update_user'] = request['login']['account']
            bean['update_time'] = datetime.now()
            result2 = await device_ibox.save_customer_device_args(check_customer_id, customer_id, bean, device_type)
            result = result & result2
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    # async def delete_customer_device_argument_by_customer_id(self, request):
    #     """
    #     Description Device
    #     ---
    #     tags:
    #     - Device
    #     summary: customerDevice
    #     description: delete customerDeviceArgs
    #     operationId: app.controllers.device_controller.delete_customer_device_argument_by_customer_id
    #     produces:
    #     - application/json
    #     parameters:
    #     - in: header
    #       description: login Token
    #       name: Authorization
    #       schema:
    #         type: string
    #       required: true
    #     - in: path
    #       name: device_type
    #       required: true
    #       schema:
    #         type: string
    #     - in: path
    #       name: device_id
    #       description: device primaryKey
    #       required: true
    #       schema:
    #         type: string
    #     responses:
    #         "200": {"data": true, "has_error": false, "message": "success"}
    #     """
    #     device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
    #     check_customer_id = request['login']['customer_id']
    #     customer_id = request.match_info('customer_id')
    #     result = await device_ibox.delete_customer_device_argument_by_customer_id(customer_id)
    #     api_response = ApiResponse(result)
    #     return self.json_response(api_response.asdict())

    async def get_garage_device_by_garage_id(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: garageDevice
        description: get garageDeviceArgs
        operationId: app.controllers.device_controller.get_garage_device_by_garage_id
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
          name: garage_id
          description: garage primaryKey
          required: true
          schema:
            type: string
        - in: path
          name: device_type
          required: true
          schema:
            type: string
        responses:
            "200": 
              {
                "data": {
                    "garage_ibox_args_id": 1,
                    "garage_code": "23400",
                    "store_no": "323",
                    "pos_no": 1,
                    "eid_store_no": "3346",
                    "plid": "01E1",
                    "printer": 1,
                    "tax_id_num": "86517413",
                    "ntp_server": "103.18.128.60",
                    "update_time": "2018-06-20 15:02:02",
                    "update_user": "root",
                    "garage_id": 1
                },
                "has_error": false,
                "message": "success"
              }
        """
        #endregion
        device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
        check_customer_id = request['login']['customer_id']
        device_type = request.match_info['device_type']
        garage_id = request.match_info['garage_id']
        if device_type == "iBox":
            garage_args = await device_ibox.get_garage_device_by_garage_id(garage_id)
        if device_type == 'PV3':
            print('施工中....')
        if device_type == 'Pad':
            print('施工中....')
        api_response = ApiResponse(garage_args)
        return self.json_response(api_response.asdict())

    # async def add_or_update_garage_device_args(self, request):
    #     device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
    #     check_customer_id = request['login']['customer_id']
    #     post_data = await request.json()
    #     device_type = post_data['device_type']
    #     if device_type == "iBox":
    #         iBox = post_data['iBox']
    #         result = await device_ibox.save_garage_device_args(iBox)
    #     api_response = ApiResponse(result)
    #     if device_type == 'PV3':
    #         print('施工中....')
    #     if device_type == 'Pad':
    #         print('施工中....')
    #     return self.json_response(api_response.asdict())

    async def is_enable_card_type_by_customer_id(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: customerDevice
        description: check card type
        operationId: app.controllers.device_controller.is_enable_card_type_by_customer_id
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
          description: customer primaryKey
          required: true
          schema:
            type: string
        - in: path
          name: device_type
          required: true
          schema:
            type: string
        responses:
            "200": 
              {
                "data": {
                    "customer_map_card_case_id": 1,
                    "device_type": "iBox",
                    "enable_card_case": 7,
                    "customer_id": 0
                },
                "has_error": false,
                "message": "success"
              }
        """
        #endregion
        device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
        check_customer_id = request['login']['customer_id']
        customer_id = request.match_info['customer_id']
        device_type = request.match_info['device_type']
        if customer_id == check_customer_id or check_customer_id == 0:
            result = await device_ibox.get_customer_map_card_case_by_customer_id_and_device_type(customer_id, device_type)
            api_response = ApiResponse(result)
            return self.json_response(api_response.asdict())
        else:
            raise PermissionError("check_account_has_authorization_to_use_enable_card_type","not permit to quesry other customer's data")

    async def add_or_update_device(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: Device
        description: add_or_update DeviceArgs
        operationId: app.controllers.device_controller.add_or_update_device
        produces:
        - application/json
        parameters:
        - in: header
          description: header login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: customer device data
          required: true
          schema:
            type: object
            properties:
              device_type:
                type: string
                example: iBox
              bean:
                type: object
                example:
                  ip: "2.2.2.2"
                  mac_ip: "2.2.2.2"
                  garage_id: 2
        responses:
            "200": {"data": true, "has_error": false, "message": "success"}
        """
        #endregion
        post_data = await request.json()
        device_type = post_data['device_type']
        bean = post_data['bean']
        customer_id = request['login']['customer_id']
        bean['update_user'] = request['login']['account']
        bean['update_time'] = datetime.now()
        print('準備新增或修改@@@@@@@@@@@@@@@@@@',bean)
        if device_type == 'iBox':
            device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
            if 'device_ibox_args_id' in bean:
                result = await device_ibox.update_device_argument_by_device_ibox_args_id(bean)
            else:
                check = await device_ibox.is_duplicate_ip_from_same_garage(bean['garage_id'], bean['ip'])
                if(check):
                    raise Exception('同場站相同IP 請更換')
                result = await device_ibox.add_device_argument(bean)
        elif device_type == 'PV3':
            print('PV3施工中...')
        elif device_type == 'Pad':
            print('Pad施工中...')
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_device_by_device_id(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: Device
        description: get deviceArgs
        operationId: app.controllers.device_controller.get_device_by_device_id
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
          name: device_type
          description: customer primaryKey
          required: true
          schema:
            type: string
        - in: path
          name: device_id
          required: true
          schema:
            type: integer
        responses:
            "200": 
              {
                "data": {
                    "customer_map_card_case_id": 1,
                    "device_type": "iBox",
                    "enable_card_case": 7,
                    "customer_id": 0
                },
                "has_error": false,
                "message": "success"
              }
        """
        #endregion
        device_type = request.match_info['device_type']
        device_id = request.match_info['device_id']
        if device_type == 'iBox':
            device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
            result = await device_ibox.get_device_by_device_id(device_id)
        elif device_type == 'PV3':
            print('PV3施工中...')
        elif device_type == 'Pad':
            print('Pad施工中...')
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_all_device_by_garage_id(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: Device
        description: get deviceArgs
        operationId: app.controllers.device_controller.get_all_device_by_garage_id
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
          name: garage_id
          description: garage primaryKey
          required: true
          schema:
            type: string
        responses:
            "200": 
              {
                "data": [
                    {
                    "id": 1,
                    "device_type": "iBox",
                    "device_name": "iBox一號",
                    "update_time": "2018-06-20 15:02:02",
                    "update_user": "root"
                    }
                ],
                "has_error": false,
                "message": "success"
              }
        """
        #endregion
        # TODO 之後應該也要有一個device_management 來處理 不然這邊要用union取出所有設備 這呼叫device_ibox_service 感覺不對
        device = DeviceIboxService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        result = await device.get_all_device_by_garage_id(garage_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def delete_device_by_device_id(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: Device
        description: delete deviceArgs
        operationId: app.controllers.device_controller.delete_device_by_device_id
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
          name: device_type
          required: true
          schema:
            type: string
        - in: path
          name: device_id
          description: device primaryKey
          required: true
          schema:
            type: integer
        responses:
            "200": 
              {
                "data": true,
                "has_error": false,
                "message": "success"
              }
        """
        #endregion
        device = DeviceIboxService(request.app['pmsdb'], request['login'])
        device_id = request.match_info['device_id']
        device_type = request.match_info['device_type']
        # TODO 這邊應該要丟給deivce_management_service 處理 之後要改程式
        if device_type == "iBox":
            result = await device.delete_device_by_device_id(device_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def device_export(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: Device
        description: export device csv to aws
        operationId: app.controllers.device_controller.device_export
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
          description: export device csv data to aws
          name: body
          required: true
          schema:
            type: object
            properties:
            data:
                type: object
                properties:
                customer_id:
                    type: string
                    description: customer_id
                device_ibox_args_id:
                    type: string
                    description: device_ibox_args_id
                garage_code:
                    type: string
                    description: garage_code
                garage_id:
                    type: string
                    description: garage_id
            device_type:
                type: string
                example: 'iBox'
            car_type:
                type: string
                example: 'c'
            required:
                - data
                - device_type
        responses:
            "200": {"data": true, "has_error": false, "message": "success"}
        """
        #endregion
        post_data = await request.json()
        device_type = post_data['device_type']
        car_type = post_data['car_type']
        data = post_data['data']
        # print('觀察data.. ', data)
        device_manager = DeviceManager(request.app['pmsdb'], request['login'])
        result = await device_manager.device_export(data, device_type, car_type)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def add_device_event(self,request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: add_device_event
        description: add device event
        operationId: app.controllers.device_controller.add_device_event
        produces:
        - application/json
        parameters:
        - in: header
          description: header login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: device event data
          required: true
          schema:
            type: object
            properties:
                device_event:
                    type: object
                    required: true
                    properties:
                        event_category:
                            type: string
                            example: PV
                        event_type:
                            type: string
                            example: error
                        message:
                            type: string
                            example: some text
                        event_source:
                            type: string
                            example: pv3
                        source_ip_address:
                            type: string
                            example: 192.168.0.1
                        field_01:
                            type: string
                            example: field 01 text
                        field_02:
                            type: string
                            example: field 02 text
                        field_03:
                            type: string
                            example: field 03 text
                        field_04:
                            type: string
                            example: field 04 text
                        field_05:
                            type: string
                            example: field 05 text
        responses:
            "200": {"data": true, "has_error": false, "message": "success"}
        """
        #endregion
        post_data = await request.json()
        device_event = post_data['device_event']
        device_manager = DeviceManager(request.app['pmsdb'], request['login'])
        result = await device_manager.add_device_event(device_event)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_device_event(self,request):
        #region
        """
        Description get all users according to a logged on user
        ---
        tags:
        - Device
        summary: get device event list
        description: get device event list.
        operationId: app.controllers.device_controller.get_device_event
        produces:
        - application/json
        parameters:
        - in: header
          name: Authorization
          schema:
            type: string
          required: true
        responses:
        "200":
          class::api_response
        """
        #endregion
        device_manager = DeviceManager(request.app['pmsdb'], request['login'])
        result = await device_manager.get_device_event()
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def get_device_event_sse(self,request):
        # event_id = 0
        # loop = request.app.loop
        # async with sse_response(request) as resp:

        #     while True:
        #         try:
        #             data = 'Server Time :' + str(event_id)
        #             await resp.send(data)
        #             await asyncio.sleep(2, loop=loop)
        #             event_id=event_id+1
        #         except concurrent.futures._base.CancelledError as ee:
        #             print('sse cancelled')
        #             pass
        #         except ConnectionResetError as e:
        #             print('reset error')
        #             pass
        #         else:
        #             print('else')
        #             pass
        # return resp
        return 0
        

    

    async def is_duplicate_ip_from_same_garage(self, request):
        #region
        """
        Description check ip use or not
        ---
        tags:
        - Device
        summary: check ip use or not
        description: is duplicate ip from same garage 
        operationId: app.controllers.device_controller.is_duplicate_ip_from_same_garage
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
          name: garage_id
          description: garage primaryKey
          required: true
          schema:
            type: int
        - in: path
          name: ip
          required: true
          schema:
            type: string
        """
        #endregion
        device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        ip = request.match_info['ip']
        result = await device_ibox.is_duplicate_ip_from_same_garage(garage_id, ip)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def download_device_parameter(self, request):
        #region
        """
        Description Device
        ---
        tags:
        - Device
        summary: Device
        description: download device parameter
        operationId: app.controllers.device_controller.download_device_parameter
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
          description: export device csv data to aws
          name: body
          required: true
          schema:
            type: object
            properties:
            data:
                type: object
                properties:
                customer_id:
                    type: string
                    description: customer_id
                device_ibox_args_id:
                    type: string
                    description: device_ibox_args_id
                garage_code:
                    type: string
                    description: garage_code
                garage_id:
                    type: string
                    description: garage_id
            device_type:
                type: string
                example: 'iBox'
            car_type:
                type: string
                example: 'c'
            required:
                - data
                - device_type
        responses:
            "200": {"data": true, "has_error": false, "message": "success"}
        """
        #endregion
        post_data = await request.json()
        device_type = post_data['device_type']
        car_type = post_data['car_type']
        data = post_data['data']
        device_manager = DeviceManager(request.app['pmsdb'], request['login'])
        result = await device_manager.download_device_parameter(data, device_type, car_type)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

