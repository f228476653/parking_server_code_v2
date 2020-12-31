
from aiohttp import web
from app.config.models import Account
from app.services.user_service import UserService
from app.services.device_ibox_service import DeviceIboxService 
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.controllers.controller import Controller

from .api_response import ApiResponse
from aiohttp_swagger import *

class LoginController(Controller):
    
    async def login(self,request):
        """
        Description login
        ---
        tags:
        - Login
        summary: Login
        description: user login.
        operationId: app.controllers.login_controller.login
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: login and get token
          required: true
          schema:
            type: object
            properties:
              account:
                type: string
                description: account
                example: root
              passwd:
                type: string
                description: password
                example: '@@123qwe'
              rem:
                type: boolean
                default: fasle
                description: remember me
            required:
                - account
                - passwd
                - rem
        responses:
        "200":
          {"data": {"is_customer_root": false, "role_id": 1, "customer_id": 0, "is_superuser": true, "token": "eyJpZCI6MiwidGVzdCI6InRlc3QiLCJleHAiOjE1ODk1NjgzMTd9.ZziCdUKbpGLg9pHotuBcvLve0JbnHmB6bUyAutVCxXA", "user_name": "", "account": "root", "account_id": 2}, "has_error": false, "message": "success"}
        """
        post_data = await request.json()
        account = post_data.get('account')
        password = post_data.get('passwd')
        rem = post_data.get('rem')
        if rem :
            jwt_exp_delta_seconds = request.app['jwt_exp_delta_seconds_remember_me']
        else:
            jwt_exp_delta_seconds = request.app['jwt_exp_delta_seconds']
        jwt_secret = request.app['jwt_secret']
        jwt_algorithm = request.app['jwt_algorithm']

        try:
            user_service = UserService(request.app['pmsdb'],None)
            result = await user_service.login(account,password,jwt_exp_delta_seconds,jwt_secret,jwt_algorithm)
            data={'is_customer_root':result['is_customer_root'], 'role_id':result['role_id'],'customer_id':result['customer_id'],'is_superuser':result['is_superuser'],'token':result['token'].decode('utf-8'),'user_name':result['user_name'],'account':result['account'],'account_id':result['account_id']}
            api_response=ApiResponse(data)
            return self.json_response(api_response.asdict())
        except UserNotExistError:
            api_response=ApiResponse({},True,"User does not exist")
            return self.json_response(api_response.asdict())
        except AuthenticationError:
            api_response=ApiResponse({},True,"Wrong credentials")
            return self.json_response(api_response.asdict())

    async def forget_passward_query_reset(self,request):
        """ forget password """
        print('save')
        user_service = UserService(request.app['pmsdb'],None)
        post_data = await request.json()
        email = post_data.get('email')
        jwt_secret = request.app['jwt_secret']
        jwt_algorithm = request.app['jwt_algorithm']
        jwt_exp_delta_seconds = 36000000
        result = await user_service.forget_passward_query_reset(email,jwt_secret,jwt_algorithm,jwt_exp_delta_seconds)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_reset_password_account(self,request):
        token=request.match_info['token']
        service = UserService(request.app['pmsdb'],None)
        data = await service.get_reset_password_account(token)
        result = ApiResponse(data)
        return self.json_response(result.asdict())


    async def aaa(self, request):
        """
        Description login
        ---
        tags:
        - Login
        summary: Test iBox API
        description: test iBox API.
        operationId: app.controllers.login_controller.aaa
        produces:
        - application/json
        parameters:
        - in: path
          name: c
          description: customer code
          required: true
          schema:
            type: string
        - in: path
          name: g
          description: acer garage code
          required: true
          schema:
            type: string
        - in: path
          name: d
          description: iBox IP
          required: true
          schema:
            type: string
        responses:
        "200":
            {
                "data": {
                    "customer_device": {
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
                    "garage_device": {
                        "garage_ibox_args_id": 1,
                        "garage_code": "23400",
                        "store_no": "323",
                        "pos_no": 1,
                        "eid_store_no": "3346",
                        "plid": "01E1",
                        "printer": 1,
                        "tax_id_num": "86517413",
                        "ntp_server": "103.18.128.60",
                        "update_time": "2018-06-21 03:57:08",
                        "update_user": "root",
                        "garage_id": 1
                    },
                    "device": {
                        "device_ibox_args_id": 1,
                        "device_name": "iBox一號",
                        "external_ip": "61.222.250.66",d
                        "station_inout": 1,
                        "ECC": 1,
                        "iPass": 1,
                        "iCash": 0,
                        "YHDP": 1,
                        "ip": "192.168.0.102",
                        "mac_ip": "255.255.255.255",
                        "eid_pos_no": "346Z",
                        "update_time": "2018-06-21 03:57:08",
                        "update_user": "root",
                        "garage_id": 1
                    }
                },
                "has_error": false,
                "message": "success"
            }

        """
        c = request.match_info['c']
        g = request.match_info['g']
        d = request.match_info['d']
        device = DeviceIboxService(request.app['pmsdb'], None)
        r = await device.aaa(c,g,d)
        a = ApiResponse(r)
        return self.json_response(a.asdict())
