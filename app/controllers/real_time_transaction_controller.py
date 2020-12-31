import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.real_time_transaction_service import RealTimeTransactionService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler

class RealTimeTransactionController(Controller):
    
    async def add_transaction(self,request):
        """
        Description 新增進出交易資料
        ---
        tags:
        - real_time_transaction
        summary: 新增進出交易資料
        description: 新增進出交易資料
        operationId: app.controllers.real_time_transaction_controller.add_transaction
        produces:
        - application/json
        parameters:
        - in: header
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: parking_id,exit_type_config_detail_id and pay_datetime is required also if in_or_out=1
          required: true
          schema:
            type: object
            properties:
              transaction:
                type: object
                description: wrapped class
                properties:
                    in_or_out:
                        type: string
                        description: 進離場類別(0:進場、1:離場)
                        example: '0'
                    parking_type:
                        type: string
                        description: 臨時車或月租車(0:臨停車、1:月租車)
                        example: '0'
                    card_id_16:
                        type: string
                        description: 票卡卡號(如:票證卡片卡號、停車卡卡號、token ID)(卡內碼mifire)
                        example: 245234524
                    in_or_out_datetime:
                        type: string
                        description: 進/出場日期時間
                        example: '2018-01-08 23:59:00'
                    pay_datetime:
                        type: string
                        description: 付費時間
                        example: '2018-01-08 23:59:00'
                    card_type:
                        type: string
                        description: 卡別(01:ECC,02:愛金,03:KRTC,05:遠鑫,99:人工結帳….)
                        example: '01'
                    receivable:
                        type: string
                        description: 應收費用
                        example: '40'
                    real_fees:
                        type: string
                        description: 實際費用
                        example: '40'
                    before_pay_balance:
                        type: string
                        description: 扣款前卡片餘額
                        example: '140'
                    is_disability :
                        type: string
                        description: 是否為身障計費(>0:身障計費規則id,0:否)
                        example: '0'
                    vehicle_identification_number :
                        type: string
                        description: 車牌號碼  
                        example: 'EF-3782'
                    device_ip :
                        type: string
                        description: device的ip
                        example: '192.168.0.200'
                    garage_id:
                        type: string
                        description: 場站ID
                        example: '1'
                    customer_id:
                        type: string
                        description: 業者ID
                        example: '1'
                    discount_type:
                        type: string
                        description: '0: 無優惠，1: 身障優惠，2: 折扣優惠'
                        example: '1'
                    discount_amount:
                        type: string
                        description: 優惠金額
                        example: '20'
                    status_number:
                        type: string
                        description: 狀態碼(交易正常:0 異常:1)
                        example: '1'
                    vehicle_type:
                        type: string
                        description: 車種 0:unknown,1:汽車,2:機車,3:卡車,4:腳踏車,5:沙石車,6:小貨車,7:休旅車,8:箱型車,9:電動機車,10:電動汽車,11:大客車,12:小巴,13:拖板車 
                        example: '0'
                    card_id_appearance:
                        type: string
                        description: 卡片外碼
                        example: '1'
                    is_autoload:
                        type: string
                        description: 是否開啟自動加值功能(1:開啟,0:無) 
                        example: '1'
                    autoload_amout:
                        type: string
                        description: 自動加值金額 
                        example: '0'
                    parking_id:
                        type: string
                        description: 車輛進場時parking_id
                        example: '0'
                    create_account_id:
                        type: string
                        description: 新增者帳號ID
                        example: '0'
                    exit_type_config_detail_id:
                        type: string
                        description: 出場設定ID
                        example: '0'
                    exit_type_config_detail_remarks:
                        type: string
                        description: 出場設定備註
                        example: '地主'
                    record_status :
                        type: int
                        description: 資料狀態 (0:作廢,1:正常,2:補開)
                        example: 1
                    device_type :
                        type: int
                        description: 設備種類, 0:未知,1:pv3,2:pv,3:pad,4:ibox,5:abs
                        example: 3
                    tax_id_number :
                        type: string
                        description: 公司統編
                        example: '12333344'
                    tax_id_number_buyer :
                        type: string
                        description: 買受人統編
                        example: '93339999'
            required:
                - in_or_out(入場)
                - pakring_type(入場)
                - card_id_16(入場)
                - receivable(入/出場)
                - card_type(入場)
                - real_fees(入/出場)
                - before_pay_balance(入場)
                - garage_id(入/出場)
                - card_id_appearance(入場)
                - in_or_out_datetime(入/出場)
                - is_autoload(入場)
                - vehicle_identification_number(入場)
                - is_disability(入場)
                - vehicle_type(入場)
                - garage_id(入場)
                - parking_id(出場)
                - is_autoload(出場)
                - pay_datetime(出場)
        responses:
        "200":
          class::api_response
        """
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data = post_data.get('transaction')
        #data['create_account_id']=request['login']['account_id']
        result = await db_service.add_transaction(data)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_transaction(self,request):
        """
        """
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data= post_data.get('page_query')
        data = await db_service.get_transaction(data)
        return self.json_response(ApiResponse(data).asdict())

    async def get_transaction_pad(self,request):
        """
        Description real time transaction
        ---
        tags:
        - real_time_transaction
        summary: get pad real time transaction
        description: get pad real time transaction
        operationId: app.controllers.real_time_transaction_controller.get_transaction_pad
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
          description: get pad real time transaction
          required: true
          schema:
            type: object
            properties:
                page_query:
                    type: object
                    required: true
                    properties:
                        paid_time_begin:
                            type: string
                            example: '2018-08-30 00:00:00'
                        paid_time_end:
                            type: string
                            example: '2018-09-30 00:00:00'
                        exit_time_begin:
                            type: string
                            example: '2018-08-30 00:00:00'
                        exit_time_end:
                            type: string
                            example: '2018-09-30 00:00:00'
                        vehicle_identification_number:
                            type: string
                            example: RF-4f43
                        enter_time_begin:
                            type: string
                            example: '2018-08-30 00:00:00'
                        enter_time_end:
                            type: string
                            example: '2018-09-30 00:00:00'
                        exit_type_config_detail_name:
                            type: string
                            example: ''
                        real_fee:
                            type: string
                            example: 40
                        einvoice_number:
                            type: string
                            example: RE09389304
                        create_user_name:
                            type: string
                            example: YEN
                        vehicle_type:
                            type: string
                            example: c
                        abnormal:
                            type: string
                            example: check
                        garage_id:
                            type: string
                            example: 1
                        garage_group_id:
                            type: string
                            example: 1        
        """
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data= post_data.get('page_query')
        data = await db_service.get_transaction_pad(data )
        return self.json_response(ApiResponse(data).asdict())

    async def delete_transaction_by_id(self,request):
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        parking_id = request.match_info['parking_id']
        garage_id = request.match_info['garage_id']
        account_id = request['login']['account_id']
        result = await db_service.delete_transaction_by_id(parking_id,account_id,garage_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_transaction_by_checkout_no(self,request):
        #region
        """
        Description get checkout data
        ---
        tags:
        - real_time_transaction
        summary: get checkout data
        description: get checkout data
        operationId: app.controllers.real_time_transaction_controller.get_transaction_by_checkout_no
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
          name: checkout_no
          description: no of shift checkout
          required: true
          schema:
            type: string
        - in: path
          name: garage_id
          description: id of garage 
          required: true
          schema:
            type: string
        """
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        checkout_no=request.match_info['checkout_no']
        garage_id=request.match_info['garage_id']
        data = await db_service.get_transaction_by_checkout_no(checkout_no,garage_id)
        return self.json_response(ApiResponse(data).asdict())

    async def cancel_parking(self,request):
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        parking_id=request.match_info['parking_id']
        data = await db_service.cancel_parking(parking_id)
        return self.json_response(ApiResponse(data).asdict())

    async def get_transaction_by_garage_code(self, request):
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        #pagination = post_data['pagination']
        query_clause = post_data['page_query']
        #print('**************************', pagination)
        print('**************************', query_clause)
        data = await db_service.get_transaction_by_garage_code(query_clause)
        return self.json_response(ApiResponse(data).asdict())

    async def add_complete_transaction(self,request):
        """
        Description 
        ---
        tags:
        - real_time_transaction
        summary: 新增已完成交易之交易資料
        description: 新增已完成交易之交易資料
        operationId: app.controllers.real_time_transaction_controller.add_complete_transaction
        produces:
        - application/json
        parameters:
        - in: header
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: real time transaction data
          required: true
          schema:
            type: object
            properties:
              transaction:
                type: object
                description: wrapped class
                properties:
                    enter_datetime:
                        type: string
                        description: 進場日期時間
                        example: '2018-01-08 23:59:00'
                    exit_datetime:
                        type: string
                        description: 出場日期時間
                        example: '2018-01-09 23:59:00'
                    in_device_ip :
                        type: string
                        description: 進場device的ip
                        example: '192.168.0.200'
                    out_device_ip :
                        type: string
                        description: 出場device的ip
                        example: '192.168.0.200'
                    garage_id:
                        type: string
                        description: 場站ID
                    status_number:
                        type: string
                        description: 狀態碼(交易正常:0 異常:1)
                        example: '1'
                    vehicle_type:
                        type: string
                        description: 車種 0:unknown,1:汽車,2:機車,3:卡車,4:腳踏車,5:沙石車,6:小貨車,7:休旅車,8:箱型車,9:電動機車,10:電動汽車,11:大客車,12:小巴,13:拖板車 
                        example: '0'
                    card_id_appearance:
                        type: string
                        description: 卡片外碼
                        example: 'DFG9379DS'
                    is_autoload:
                        type: string
                        description: 是否開啟自動加值功能(1:開啟,0:無) 
                        example: '1'
                    autoload_amout:
                        type: string
                        description: 自動加值金額 
                        example: '0'
                    record_status :
                        type: int
                        description: 資料狀態 (0:作廢,1:正常,2:補開)
                        example: 1
                    tax_id_number :
                        type: string
                        description: 公司統編
                        example: '12333344'
                    tax_id_number_buyer :
                        type: string
                        description: 買受人統編
                        example: '93339999'
                    parking_type:
                        type: string
                        description: 臨時車或月租車(0:臨停車、1:月租車)
                        example: '0'
                    card_id_16:
                        type: string
                        description: 票卡卡號(如:票證卡片卡號、停車卡卡號、token ID)(卡內碼mifire)
                        example: 245234524
                    pay_datetime:
                        type: string
                        description: 付費時間
                        example: '2018-01-08 23:59:00'
                    card_type:
                        type: string
                        description: 卡別(01:ECC,02:愛金,03:KRTC,05:遠鑫,99:人工結帳….)
                        example: '01'
                    receivable:
                        type: string
                        description: 應收費用
                        example: '40'
                    real_fees:
                        type: string
                        description: 實際費用
                        example: '40'
                    before_pay_balance:
                        type: string
                        description: 扣款前卡片餘額
                        example: '140'
                    is_disability :
                        type: string
                        description: 是否為身障計費(>0:身障計費規則id,0:否)
                        example: '0'
                    discount_type:
                        type: string
                        description: '0: 無優惠，1: 身障優惠，2: 折扣優惠'
                        example: '1'
                    discount_amount:
                        type: string
                        description: 優惠金額
                        example: '20'
                    autoload_amout:
                        type: string
                        description: 自動加值金額 
                        example: '0'
                    parking_id:
                        type: string
                        description: 車輛進場時parking_id
                        example: '0'
                    device_type :
                        type: int
                        description: 設備種類, 0:未知,1:pv3,2:pv,3:pad,4:ibox,5:abs
                        example: 3
            required:
                - pakring_type
                - card_id_16
                - receivable
                - card_type
                - real_fees
                - before_pay_balance
                - garage_id
                - card_id_appearance
                - in_or_out_datetime
                - is_autoload
                - vehicle_identification_number
                - is_disability
                - vehicle_type
                - is_autoload
                - pay_datetime
        responses:
        "200":
          class::api_response
        """
        db_service = RealTimeTransactionService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        data = post_data.get('transaction')
        #data['create_account_id']=request['login']['account_id']
        result = await db_service.add_complete_transaction(data)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())
    


        

    
