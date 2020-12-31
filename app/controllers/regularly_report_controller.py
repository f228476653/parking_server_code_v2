import json
from datetime import datetime
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.regularly_report_service import RegularlyReportService

class RegularlyReportController(Controller):
    async def get_day_revenue_report(self, request):
        """
        Description 
        ---
        tags:
        - Regularly report
        summary: day revenue
        description: get day revenue by day,paid_type
        operationId: app.controllers.regularly_report_service.get_day_revenue
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
          name: garage_code
          description: query garage
          required: true
          schema:
            type: string
        - in: path
          name: the_day
          description: query date
          required: true
          schema:
            type: string
        - in: path
          name: paid_type
          description: paid_type
          required: true
          schema:
            type: string
        responses:
            "200": 
              {
                "data": [{
                            "fee": 40,
                            "cnt": "5",
                            "subtotal": "200"
                        }],
                "has_error": false,
                "message": "success"
               }
        """
        day_revenue = RegularlyReportService(request.app["pmsdb"], request['login'])
        garage_code = request.match_info["garage_code"]
        the_day = request.match_info["the_day"]
        paid_type = request.match_info["paid_type"]
        result = await day_revenue.get_day_revenue_report(garage_code, the_day, paid_type)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_monthly_revenue_report(self, request):
        """
        Description 
        ---
        tags:
        - Regularly report
        summary: monthly revenue report
        description: get monthly revenue report by garage_code, month, paid_type
        operationId: app.controllers.regularly_report_service.get_monthly_revenue_report
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
          name: garage_code
          description: query garage
          required: true
          schema:
            type: string
        - in: path
          name: the_month
          description: query month
          required: true
          schema:
            type: string
        - in: path
          name: paid_type
          description: paid_type
          required: true
          schema:
            type: string
        """
        monthly_revenue = RegularlyReportService(request.app["pmsdb"], request['login'])
        garage_code = request.match_info["garage_code"]
        the_month = request.match_info["the_month"]
        paid_type = request.match_info["paid_type"]
        result = await monthly_revenue.get_monthly_revenue_report(garage_code, the_month, paid_type)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_monthly_usage_report(self, request):
        #region
        """
        Description 
        ---
        tags:
        - Regularly report
        summary: monthly usage report
        description: get monthly usage report by garage_code, monthly
        operationId: app.controllers.regularly_report_service.get_monthly_usage_report
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
          name: garage_code
          description: garage_code
          required: true
          schema:
            type: string
        - in: path
          name: monthly
          description: monthly
          required: true
          schema:
            type: string
        """
        #endregion
        monthly_usage = RegularlyReportService(request.app["pmsdb"], request['login'])
        garage_code = request.match_info["garage_code"]
        monthly = request.match_info["monthly"]
        print('觀察一下', garage_code)
        print('and... ', monthly)
        result = await monthly_usage.get_monthly_usage_report(garage_code, monthly)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())


