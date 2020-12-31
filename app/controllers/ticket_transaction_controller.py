import json
import os
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.monitor_data_service import MonitorDataService

from app.services.ticket_transaction_icash_service import TicketTransactionICashService
from app.services.ticket_transaction_ipass_service import TicketTransactionIPassService
from app.services.ticket_transaction_happycash_service import TicketTransactionHappyCashService

class TicketTransactionController(Controller):

    """ ICash 愛金卡 """
    # 交易檔包檔
    @authorize([], [])
    async def icash_pack(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await service.pack(os.path.join('csvs', 'in'))
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 交易檔上傳
    @authorize([], [])
    async def icash_upload(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await service.upload()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 回饋檔、剔退檔下載
    @authorize([], [])
    async def icash_download_feedback_files(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "feedback_files")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 黑名單下載
    @authorize([], [])
    async def icash_download_black_list(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "black_list")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 回饋檔、剔退檔匯入
    @authorize([], [])
    async def icash_feedback_files_import(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await service.feedback_data_import_db()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 查詢場站交易檔參數資料
    @authorize([], [])
    async def icash_query_garage(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        data = await service.icash_query_garage_parameter(garage_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 新增場站交易檔參數資料 (有啟用票種 & 欄位有填值)
    @authorize([], [])
    async def icash_insert_garage(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        garage_code = data['garage']['garage_code']
        customer_id = data['garage']['customer_id']
        create_user_id = request['login']['account_id']
        icash_bean = data.get('iCash')
        result = await service.icash_insert_garage_parameter(icash_bean, garage_code, customer_id, create_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 更新場站交易檔參數資料
    @authorize([], [])
    async def icash_update_garage(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        garage_id = data['garage']['garage_id']
        customer_id = data['garage']['customer_id']
        update_user_id = request['login']['account_id']
        # 未啟用票種
        if data.get('iCash') is None:
            result = await service.icash_update_garage_parameter_disabled_status(garage_id, customer_id, update_user_id)
        # 有啟用票種 & 欄位有填值
        elif data.get('iCash'):
            icash_bean = data.get('iCash')
            result = await service.icash_update_garage_parameter_enabled_status(icash_bean, garage_id, customer_id, update_user_id)
        # 有啟用票種 & 欄位未填值
        else:
            result = await service.icash_update_garage_parameter_disabled_status(garage_id, customer_id, update_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 刪除場站交易檔參數資料
    @authorize([], [])
    async def icash_delete_garage(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        data = await service.icash_delete_garage_parameter(garage_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 業者交易檔參數資料查詢
    @authorize([], [])
    async def icash_query_customer(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        data = await service.icash_query_customer_parameter(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 新增業者交易檔參數資料 (有啟用票種 & 欄位有填值)
    @authorize([], [])
    async def icash_insert_customer(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        customer_code = data['customer']['customer_code']
        create_user_id = request['login']['account_id']
        icash_bean = data.get('iCash')
        result = await service.icash_insert_customer_parameter(icash_bean, customer_code, create_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 更新業者交易檔參數資料
    @authorize([], [])
    async def icash_update_customer(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        customer_id = data['customer']['customer_id']
        update_user_id = request['login']['account_id']
        # 有啟用票種 & 欄位有填值
        if len(data.get('iCash')) != 0:
            icash_bean = data.get('iCash')
            result = await service.icash_update_customer_parameter_enabled_status(icash_bean, customer_id, update_user_id)
        # 未啟用票種 || 有啟用票種但未填值
        elif len(data.get('iCash')) == 0:
            result = await service.icash_update_customer_parameter_disabled_status(customer_id, update_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 刪除業者交易檔參數資料
    @authorize([], [])
    async def icash_delete_customer(self, request):
        service = TicketTransactionICashService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        data = await service.icash_delete_customer_parameter(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    """ IPass 一卡通 """
    # 交易檔包檔
    @authorize([], [])
    async def ipass_pack(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.pack(os.path.join('csvs', 'in'))
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 交易檔上傳
    @authorize([], [])
    async def ipass_upload(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.upload()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 回饋檔下載
    @authorize([], [])
    async def ipass_download_feedback_files(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "feedback_files")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 黑名單 3小時增量檔下載
    @authorize([], [])
    async def ipass_download_black_list_KBLI(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "black_list_KBLI")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 黑名單下載
    @authorize([], [])
    async def ipass_download_black_list_KBLN(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "black_list_KBLN")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 關閉自動加值名單下載
    @authorize([], [])
    async def ipass_download_close_autoload_list(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "close_autoload_list")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 回饋檔匯入
    @authorize([], [])
    async def ipass_feedback_files_import(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await service.feedback_data_import_db()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 查詢場站交易檔參數資料
    @authorize([], [])
    async def ipass_query_garage(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        data = await service.ipass_query_garage_parameter(garage_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 新增場站交易檔參數資料 (有啟用票種 & 欄位有填值)
    @authorize([], [])
    async def ipass_insert_garage(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await request.json()
        garage_code = data['garage']['garage_code']
        customer_id = data['garage']['customer_id']
        create_user_id = request['login']['account_id']
        ipass_bean = data.get('iPass')
        result = await service.ipass_insert_garage_parameter(ipass_bean, garage_code, customer_id, create_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 更新場站交易檔參數資料
    @authorize([], [])
    async def ipass_update_garage(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await request.json()
        garage_id = data['garage']['garage_id']
        customer_id = data['garage']['customer_id']
        update_user_id = request['login']['account_id']
        # 未啟用票種
        if data.get('iPass') is None:
            result = await service.ipass_update_garage_parameter_disabled_status(garage_id, customer_id, update_user_id)
        # 有啟用票種 & 欄位有填值
        elif data.get('iPass'):
            ipass_bean = data.get('iPass')
            result = await service.ipass_update_garage_parameter_enabled_status(ipass_bean, garage_id, customer_id, update_user_id)
        # 有啟用票種 & 欄位未填值
        else:
            result = await service.ipass_update_garage_parameter_disabled_status(garage_id, customer_id, update_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 刪除場站交易檔參數資料
    @authorize([], [])
    async def ipass_delete_garage(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        data = await service.ipass_delete_garage_parameter(garage_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 查詢業者交易檔參數資料
    @authorize([], [])
    async def ipass_query_customer(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        data = await service.ipass_query_customer_parameter(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 新增業者交易檔參數資料 (有啟用票種 & 欄位有填值)
    @authorize([], [])
    async def ipass_insert_customer(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await request.json()
        customer_code = data['customer']['customer_code']
        create_user_id = request['login']['account_id']
        ipass_bean = data.get('iPass')
        result = await service.ipass_insert_customer_parameter(ipass_bean, customer_code, create_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 更新業者交易檔參數資料
    @authorize([], [])
    async def ipass_update_customer(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        data = await request.json()
        customer_id = data['customer']['customer_id']
        update_user_id = request['login']['account_id']
        # 有啟用票種 & 欄位有填值
        if len(data.get('iPass')) != 0:
            ipass_bean = data.get('iPass')
            result = await service.ipass_update_customer_parameter_enabled_status(ipass_bean, customer_id, update_user_id)
        # 未啟用票種 || 有啟用票種但未填值
        elif len(data.get('iPass')) == 0:
            result = await service.ipass_update_customer_parameter_disabled_status(customer_id, update_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 刪除業者交易檔參數資料
    @authorize([], [])
    async def ipass_delete_customer(self, request):
        service = TicketTransactionIPassService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        data = await service.ipass_delete_customer_parameter(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    """ HappyCash 遠鑫卡(有錢卡) """
    # 交易檔包檔
    @authorize([], [])
    async def happycash_pack(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await service.pack(os.path.join('csvs', 'in'))
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 交易檔上傳
    @authorize([], [])
    async def happycash_upload(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await service.upload()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 回饋檔下載
    @authorize([], [])
    async def happycash_download_feedback_files(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "feedback_files")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    # 黑名單下載
    @authorize([], [])
    async def happycash_download_black_list(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await service.download(os.path.join('csvs', 'out'), "black_list")
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 回饋檔匯入
    @authorize([], [])
    async def happycash_feedback_files_import(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await service.feedback_data_import_db()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 查詢場站交易檔參數資料
    @authorize([], [])
    async def happycash_query_garage(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        data = await service.happycash_query_garage_parameter(garage_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 新增場站交易檔參數資料 (有啟用票種 & 欄位有填值)
    @authorize([], [])
    async def happycash_insert_garage(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        garage_code = data['garage']['garage_code']
        customer_id = data['garage']['customer_id']
        create_user_id = request['login']['account_id']
        happycash_bean = data.get('happyCash')
        result = await service.happycash_insert_garage_parameter(happycash_bean, garage_code, customer_id, create_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 刪除場站交易檔參數資料
    @authorize([], [])
    async def happycash_delete_garage(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        garage_id = request.match_info['garage_id']
        data = await service.happycash_delete_garage_parameter(garage_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 更新場站交易檔參數資料
    @authorize([], [])
    async def happycash_update_garage(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        garage_id = data['garage']['garage_id']
        customer_id = data['garage']['customer_id']
        update_user_id = request['login']['account_id']
        # 未啟用票種
        if data.get('happyCash') is None:
            result = await service.happycash_update_garage_parameter_disabled_status(garage_id, customer_id, update_user_id)
        # 有啟用票種 & 欄位有填值
        elif data.get('happyCash'):
            happycash_bean = data.get('happyCash')
            result = await service.happycash_update_garage_parameter_enabled_status(happycash_bean, garage_id, customer_id, update_user_id)
        # 有啟用票種 & 欄位未填值
        else:
            result = await service.happycash_update_garage_parameter_disabled_status(garage_id, customer_id, update_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 查詢業者交易檔參數資料
    @authorize([], [])
    async def happycash_query_customer(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        data = await service.happycash_query_customer_parameter(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 新增業者交易檔參數資料 (有啟用票種 & 欄位有填值)
    @authorize([], [])
    async def happycash_insert_customer(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        customer_code = data['customer']['customer_code']
        create_user_id = request['login']['account_id']
        happycash_bean = data.get('happyCash')
        result = await service.happycash_insert_customer_parameter(happycash_bean, customer_code, create_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    # 刪除業者交易檔參數資料
    @authorize([], [])
    async def happycash_delete_customer(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        data = await service.happycash_delete_customer_parameter(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    # 更新業者交易檔參數資料
    @authorize([], [])
    async def happycash_update_customer(self, request):
        service = TicketTransactionHappyCashService(request.app['pmsdb'], request['login'])
        data = await request.json()
        customer_id = data['customer']['customer_id']
        update_user_id = request['login']['account_id']
        # 有啟用票種 & 欄位有填值
        if len(data.get('happyCash')) != 0:
            happycash_bean = data.get('happyCash')
            result = await service.happycash_update_customer_parameter_enabled_status(happycash_bean, customer_id, update_user_id)
        # 未啟用票種 || 有啟用票種但未填值
        elif len(data.get('happyCash')) == 0:
            result = await service.happycash_update_customer_parameter_disabled_status(customer_id, update_user_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())