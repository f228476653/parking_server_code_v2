import json, time
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.customer_service import CustomerService
from app.services.device_ibox_service import DeviceIboxService
from app.controllers.api_response import ApiResponse

class CustomerController(Controller):
    
    @authorize([], [])
    async def get_customers(self,request):
        """ get all customers """
        service = CustomerService(request.app['pmsdb'],request['login'])
        data = await service.get_customers()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_customer_by_id(self,request):
        """ get customer by customer_id """
        id=request.match_info['id']
        service = CustomerService(request.app['pmsdb'],request['login'])
        data = await service.get_customer_by_id(id)
        result = ApiResponse([dict(data)][0])
        return self.json_response(result.asdict())

    async def delete_customer_by_id(self,request):
        # TODO 要把delete method 要轉移到customer manager 
        db_service = CustomerService(request.app['pmsdb'],request['login'])
        id = request.match_info['id']
        result = await db_service.delete_customer_by_id(id)
        device_ibox = DeviceIboxService(request.app['pmsdb'], request['login'])
        result2 = await device_ibox.delete_customer_device_argument_by_customer_id(id)
        return self.json_response(result)


    async def add_customer(self,request):
        db_service = CustomerService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        customer = post_data.get('customer')
        customer['create_account_id']=request['login']['account_id']
        print(f'customer___controller---{customer}')
        result = await db_service.add_customer(customer)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def update_customer(self,request):
        db_service = CustomerService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        customer = post_data.get('customer')
        print(customer)
        customer['modified_account_id']=request['login']['account_id']
        result = await db_service.update_customer(customer,customer['customer_id'])
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())