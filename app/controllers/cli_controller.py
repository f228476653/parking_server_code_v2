import json
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.cli_service import CliService
from app.controllers.api_response import ApiResponse
import time

class CliController(Controller):
    
    async def accounting_parse(self,request):
        """ parse csv file for example : parse csv files in the dir directory via http://localhost:5000/api/v1/cli/accounting_parse/dir """
        service = CliService(request.app['pmsdb'])
        
        id=request.match_info['csv']
        data = await service.accounting_parse(id)
        api_response=ApiResponse(True)
        return self.json_response(api_response.asdict())

    async def query_accounting(self,request):
        """ query account data via Query object """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.query_accounting(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def accounting_daily(self,request):
        """ query account data via Query object """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.accounting_daily(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def query_pms_diff_record(self,request):
        """ query pms diff records """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.query_pms_diff_record(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def query_amt_diff_record(self,request):
        """ query pms diff records """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.query_amt_diff_record(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def query_cps_diff_record(self,request):
        """ query pms diff records """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.query_cps_diff_record(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def query_parking_settlement_record(self,request):
        """ query pms diff records """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.query_parking_settlement_record(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def query_records_after_manual_close(self,request):
        """ get caculated records which were manually """
        post_data = await request.json()
        query = post_data.get('query')
        service = CliService(request.app['pmsdb'])
        data= await service.query_records_after_manual_close(query)
        result = ApiResponse(data)
        return self.json_response(result.asdict())

    async def delete_customer_by_id(self,request):
        db_service = CustomerService(request.app['pmsdb'])
        
        id=request.match_info['id']
        result = await db_service.delete_customer_by_id(id)
        return self.json_response(result)

    async def add_customer(self,request):
        db_service = CustomerService(request.app['pmsdb'])
        post_data = await request.json()
        
        customer = post_data.get('customer')
        customer['create_account_id']=request['login']['account_id']
        result = await db_service.add_customer(customer)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def update_customer(self,request):
        db_service = CustomerService(request.app['pmsdb'])
        post_data = await request.json()
      
        customer = post_data.get('customer')
        customer['modified_account_id']=request['login']['account_id']
        result = await db_service.update_customer(customer,customer['customer_id'])
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())
