# from kafka import KafkaProducer
# from kafka import KafkaConsumer
# from kafka.errors import KafkaError
import json

class KafkaService:
    pass
    # def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
    #     self.kafkaHost = kafkahost
    #     self.kafkaPort = kafkaport
    #     self.kafkatopic = kafkatopic
    #     self.groupid = groupid
    #     self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,
    #                                   bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
    #         kafka_host=self.kafkaHost,
    #         kafka_port=self.kafkaPort ))

    # def consume_data(self):
    #     try:
    #         for message in self.consumer:
    #             # print json.loads(message.value)
    #             yield message
    #     except KeyboardInterrupt as e:
    #         print (e)