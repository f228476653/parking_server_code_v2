import json,re,shutil
from collections import OrderedDict
from app.controllers.controller import Controller
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.commutation_ticket_service import CommutationTicketService
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler
from configparser import ConfigParser
import os

class CommutationTicketController(Controller):
    async def update_commutation_ticket(self,request):
        """
        Description CommutationTicket
        ---
        tags:
        - CommutationTicket
        summary: import Commutation Ticket Data
        description: 由ＰＭＳ＋派送定期票資料
        operationId: app.controllers.commutation_ticket_controller.update_commutation_ticket
        produces:
        - application/json
        parameters:
        - in: header
          description: login Token
          name: Authorization
          schema:
            type: string
          required: true          
        """
        service = CommutationTicketService(request.app['pmsdb'])
        customer_commutation_path = self.read_config()
        execute_id = request['login']['account_id']
        for path in customer_commutation_path:
            data = await service.update_commutation_ticket(path,execute_id)
            if data:
                self.move_files_to_bakcup_directory(path)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    def read_config(self):
        customer_commutation_path=[]
        path = 'file_path.ini'
        cfg = ConfigParser()
        cfg.read(path)
        customer_root_path = cfg.get('excel_path','commutation_ticket_excel_path')
        customer_folder_list = os.listdir(customer_root_path)
        print(customer_folder_list)
        for folder in customer_folder_list:
            path = os.path.join(customer_root_path,folder,'commutation_ticket')
            if os.path.isdir(path):
                print('true')
                customer_commutation_path.append(path)
            print(customer_commutation_path)
        return customer_commutation_path

    def move_files_to_bakcup_directory(self,path):
        back_path = path + '/back_up'
        if not os.path.exists(back_path):
            os.makedirs(back_path)
        pattern ="^\w+[-]\w+[-]\d+[-]\w+.xlsx$"
        print(back_path)
        filelist = os.listdir(path)
        print(filelist)
        for f in filelist:
            if(re.match(pattern,f)):
                shutil.copy(path + '/' + f, path + '/back_up/' + f)
                print(path + '/' + f)
                print(path + '/back_up/' + f)
                os.remove(path + '/' + f)
