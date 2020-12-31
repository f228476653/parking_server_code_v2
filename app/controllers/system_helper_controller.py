import json
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.csvparser.system_config_parser_service import SystemConfigParserService
from app.csvparser.parking_parser_service import ParkingParserService
from app.csvparser.trx_data_parser_service import TrxDataParserService
from app.csvparser.real_time_transaction_parser_service import RealTimeTransactionParserService
from app.csvparser.lane_parser_service import LaneParserService
from app.csvparser.parking_in_out_record_parser_service import ParkingInOutRecordParserService
from app.csvparser.einvoice_number_data_parser_service import EinvoiceNumberDataParserService
from app.controllers.api_response import ApiResponse
from app.services.monitor_data_service import MonitorDataService
import time

class SystemHelperController(Controller):
    
    @authorize([], [])
    async def parse_system_config(self,request):
        """ parse csv file for example : parse csv files in the directory """
        service = SystemConfigParserService(request.app['pmsdb'])
        data = await service.parse('csvs/config')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())


    @authorize([], [])
    async def parse_parking_data(self,request):
        """ parse csv file for example : parse csv files in the dir directory via http://localhost:5000/api/v1/parse/parse_parking_data/ """
        service = ParkingParserService(request.app['pmsdb'])
        data = await service.parse('csvs/parking')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    @authorize([], [])
    async def parse_trxdata_data(self,request):
        """ parse csv file for example : parse csv files in the dir directory via http://localhost:5000/api/v1/parse/parse_trxdata_data/"""
        service = TrxDataParserService(request.app['pmsdb'])
        data = await service.parse('csvs/trx_data')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    @authorize([], [])
    async def parse_real_time_transaction_data(self,request):
        """ parse csv file for example : parse csv files in the directory"""
        service = RealTimeTransactionParserService(request.app['pmsdb'])
        account_id = request['login']['account_id']
        data = await service.parse('csvs/in/',account_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    @authorize([], [])
    async def parse_lane_data(self,request):
        """ parse csv file for example : parse csv files in the directory """
        service = LaneParserService(request.app['pmsdb'])
        data = await service.parse('csvs/lane')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    
    @authorize([], [])
    async def parse_e_invoice_number_data(self,request):
        """ parse csv file for example : parse csv files in the directory """
        service = EinvoiceNumberDataParserService(request.app['pmsdb'])
        data = await service.parse('csvs/einvoice_number_data')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    @authorize([], [])
    async def parse_parking_in_out_record(self,request):
        """ parse csv file for example : parse csv files in the directory """
        service = ParkingInOutRecordParserService(request.app['pmsdb'])
        data = await service.parse('csvs/parking_in_out_record')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    @authorize([], [])
    async def check_data_from_parser_result(self,request):
        """ check data from parser : if total in pms and pms_plus is match  """
        service = MonitorDataService(request.app['pmsdb'])
        data = await service.check_pms_pmsplus_diff('csvs/parking_in_out_record')
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
