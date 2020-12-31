import json
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.exit_config_service import ExitConfigService

class ExitConfigController(Controller):

    async def get_garage_groupname_by_customer_id(self, request):
        """ get all group_name """
        exit_config = ExitConfigService(request.app['pmsdb'])
        customer_id = request['login']['customer_id']
        all_setting_garage = await exit_config.get_garage_groupname_by_customer_id(customer_id)
        api_response = ApiResponse(all_setting_garage)
        return self.json_response(api_response.asdict())

    async def get_all_exit_config_by_customer_id(self, request):
        """ get all station """
        exit_config = ExitConfigService(request.app['pmsdb'])
        customer_id = request['login']['customer_id']
        all_setting_garage = await exit_config.get_all_exit_config_by_customer_id(customer_id)
        api_response = ApiResponse(all_setting_garage)
        return self.json_response(api_response.asdict())
    
    async def get_groupname_by_customer_id(self, request):
        exit_config = ExitConfigService(request.app['pmsdb'])
        customer_id = request['login']['customer_id']
        garage_group = await exit_config.get_groupname_by_customer_id(customer_id)
        api_response = ApiResponse(garage_group)
        return self.json_response(api_response.asdict())

    async def get_garages_by_group_name(self, request):
        """ get group garage """
        group_name=request.match_info['group_name']
        exit_config = ExitConfigService(request.app['pmsdb'])
        garage_name = await exit_config.get_garages_by_group_name(group_name)
        api_response = ApiResponse(garage_name)
        return self.json_response(api_response.asdict())
 
    async def get_exit_type_info_by_garage_id(self, request):
        garage_id = request.match_info['garage_id']
        exit_config = ExitConfigService(request.app['pmsdb'])
        garage_info = await exit_config.get_exit_type_info_by_garage_id(garage_id)
        api_response = ApiResponse(garage_info)
        return self.json_response(api_response.asdict())
    
    async def disable_exit_config_by_exit_config_id(self, request):
        exit_config = ExitConfigService(request.app['pmsdb'])
        disabled = await request.json()
        result = await exit_config.disable_exit_config_by_exit_config_id(disabled)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def reset_exit_config_by_exit_config_id(self, request):
        exit_config = ExitConfigService(request.app['pmsdb'])
        init_data = await request.json()
        init_data['exit_config_data'] = {'description' : '', 'is_configured' : 0}
        init_data['exit_config_data']['update_account_id'] = request['login']['account_id']
        init_data['exit_type_hidden'] = {'exit_type_disabled' : 1}
        result = await exit_config.reset_exit_config_by_exit_config_id(init_data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def update_exit_type_by_exit_config_id(self, request):
        exit_config = ExitConfigService(request.app['pmsdb'])
        post_data = await request.json()
        post_data['exit_config']['update_account_id'] = request['login']['account_id']
        post_data['exit_config']['is_configured'] = 1
        update_or_insert_data = []
        update_or_insert_data['exit_config'] = post_data['exit_config']
        update_or_insert_data['exit_type_config_detail'] = post_data['exit_type_config_detail']
        if_is_insert = []
        if_is_insert['update_account_id'] = request['login']['account_id']
        if_is_insert['garage'] = post_data['garage']
        result = await exit_config.update_exit_type_by_exit_config_id(update_or_insert_data, if_is_insert)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
