
from aiohttp.web_request import Request
from aiohttp.web import middleware,json_response,Response
import sys, traceback
from app.controllers.api_response import ApiResponse
import json
from pprint import pprint
from app.util.custom_json_encoder import custom_json_handler,serialize_instance,keystore_json_handler,utc_json_handler
from keystore.exceptions import KeystoreExpiredError, KeystoreInvalidError
@middleware
async def error_middleware(request: Request, handler):
    try:
        response = await handler(request)
        
        return response
    # except KeyError as err:
    #     print(f'key Error : {err} ')
    #     api_response=ApiResponse(None,True,f'key Error : {err} ')
    #     result = json.dumps(api_response.asdict(),default=custom_json_handler)
    #     return Response(content_type="application/json",status=500,text=result)
    except KeystoreExpiredError as err:
        print(f'KeystoreExpiredError : {err} ')
        api_response=ApiResponse(None,True,f'Error : {err}')
        result = json.dumps(api_response.asdict(),default=custom_json_handler)
        return Response(content_type="application/json",status=500,text=result)
    except KeystoreInvalidError as err:
        print(f'KeystoreInvalidError : {err} ')
        api_response=ApiResponse(None,True,f'Error : {err}')
        result = json.dumps(api_response.asdict(),default=custom_json_handler)
        return Response(content_type="application/json",status=500,text=result)
    except Exception as ex:
        print(f'Generic Exception : {ex} ')
        api_response=ApiResponse(None,True,f'Error : {ex}')
        result = json.dumps(api_response.asdict(),default=custom_json_handler)

        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return Response(content_type="application/json",status=500,text=result)
       
        
    






