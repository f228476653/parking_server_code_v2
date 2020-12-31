import json
# from kafka import KafkaConsumer
# from kafka import KafkaProducer
# from kafka.errors import KafkaError
from datetime import datetime
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.kafaka_service import KafkaService


class KafkaController(Controller):
    
    async def kafka_producer(self, request):
        #region
        """
        Description Kafka
        ---
        tags:
        - producer
        summary: kafka producer
        description: test kafka
        operationId: app.controllers.kafka_controller.kafka_producer
        produces:
        - application/json
        parameters:
        - in: header
          description: header login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: body
          name: body
          description: customer device data
          required: true
          schema:
            type: object
            properties:
              data:
                type: string
                example: hello everybody~
        responses:
            "200": {"data": true, "has_error": false, "message": "success"}
        """
        pass
        #endregion
        # producer = KafkaProducer(bootstrap_servers="172.18.0.2:9092",
        #                         acks = 1,
        #                         retries = 3)
        # post_data = await request.json()
        # print('觀察post_data')
        # data = post_data['data']
        # now = datetime.now()
        # now_string = ': ' + str(now)
        # data += now_string
        # print('現在要執行kafka_producer')
        # message = bytes(data, 'utf-8')
        # print('開始送訊息....')
        # print('訊息內容:', data)
        # future = producer.send('kevin_topic', message, key=b'1')
        # producer.flush()
        # producer.close()
        # print('producer 結束...')
        # api_response = ApiResponse(data)
        # return self.json_response(api_response.asdict())

    async def kafka_consumer(self,request):
      pass
        # service = KafkaService('127.0.0.1','32768','topic',None)
        # a =service.consume_data()
        # data =  a.__next__()
        # print(data)
        # api_response = ApiResponse(data)
        # return self.json_response(api_response.asdict())