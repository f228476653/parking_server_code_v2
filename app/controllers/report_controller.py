from app.controllers.controller import Controller
from app.services.report_service import ReportService
from app.controllers.api_response import ApiResponse

class ReportController(Controller):

    async def get_report(self,request):
        """ get customer by customer_id """
        garage_id=request.match_info['garage_id']
        customer_id=request.match_info['customer_id']
        service = FileService(request.app['pmsdb'],request['login'])
        data = await service.get_updated_date_by_garage_id(customer_id,garage_id)
        result = ApiResponse(data)
        return self.json_response(result.asdict())
