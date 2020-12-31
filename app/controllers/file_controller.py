from app.controllers.controller import Controller
from app.services.file_service import FileService
from app.controllers.api_response import ApiResponse
from configparser import ConfigParser

class FileController(Controller):

    async def get_updated_date_by_garage_id(self,request):
      """
      Description Files
      ---
      tags:
      - Files
      summary: get pad files update time by garage_id
      description: get pad files update time by garage_id
      operationId: app.controllers.file_controller.get_updated_date_by_garage_id
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
        description: ID of customer
        required: true
        schema:
          type: integer
      - in: path
        name: garage_id
        description: ID of garage
        required: true
        schema:
          type: string
      - in: path
        name: file_server_name
        description: file server 參數,ex:poc/devel/production
        required: true
        schema:
          type: string           
      """
      garage_id=request.match_info['garage_id']
      customer_id=request.match_info['customer_id']
      file_server_name=request.match_info['file_server_name']
      path = 'file_path.ini'
      cfg = ConfigParser()
      cfg.read(path)
      file_server_path = cfg.get('file_server',file_server_name)
      service = FileService(request.app['pmsdb'],request['login'])
      data = await service.get_updated_date_by_garage_id(customer_id,garage_id,file_server_path)
      result = ApiResponse(data)
      return self.json_response(result.asdict())

    async def get_apk_by_garage_id(self,request):
      """
        Description Files
        ---
        tags:
        - Files
        summary: get pad apk by garage_id
        description: 如果場站資料夾有apk檔案則取場站資料夾下apk檔，如果場站資料夾沒有apk檔案則取客戶資料夾下的apk檔案
        operationId: app.controllers.file_controller.get_apk_by_garage_id
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
          description: ID of customer
          required: true
          schema:
            type: integer
        - in: path
          name: garage_id
          description: ID of garage
          required: true
          schema:
            type: string
        - in: path
          name: file_server_name
          description: file server 參數,ex:poc/devel/production
          required: true
          schema:
            type: string           
        """
      garage_id=request.match_info['garage_id']
      customer_id=request.match_info['customer_id']
      file_server_name=request.match_info['file_server_name']
      path = 'file_path.ini'
      cfg = ConfigParser()
      cfg.read(path)
      file_server_path = cfg.get('file_server',file_server_name)
      service = FileService(request.app['pmsdb'],request['login'])
      data = await service.get_apk_by_garage_id(customer_id,garage_id,file_server_path)
      result = ApiResponse(data)
      return self.json_response(result.asdict())

    async def file_upload(self,request):
        service = FileService(request.app['pmsdb'],request['login'])

        request_read = await request.read()

        """ 取得name，用以判斷檔案上傳位置 """
        # 截斷Content-Type
        function_name1 = request_read.split(b'"\r\nContent-Type:')[0]
        # 截斷filename="
        function_name2 = function_name1.split(b'"; filename="')[0]
        # 截斷name="
        function_name3 = function_name2.split(b'name="')[1]

        """ 取得filename """
        # 截斷Content-Type
        filename1 = request_read.split(b'"\r\nContent-Type:')[0]
        # 截斷filename="
        filename2 = filename1.split(b'filename="')[1]

        """ 取得檔案byte資料 """
        # 截斷檔案byte前面資料
        content1 = request_read.split(b'\r\n\r\n')[1]
        # 截斷檔案byte後面資料
        content2 = content1.split(b'\r\n------')[0]
        
        data = await service.file_upload(filename2, content2, function_name3)
        
        result = ApiResponse(data)
        return self.json_response(result.asdict())