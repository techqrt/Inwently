# import json
# import os
# import traceback
# from multiprocessing import Process
#
# import django
# from django.http import HttpRequest
# from kafka import KafkaConsumer
# from rest_framework.request import Request
#
# from biller.config import Configurations
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biller.settings')
# django.setup()
#
# from kafka_consumer_producer.bind import Binder
#
#
# class KafkaTopicConsumer(Process):
#
#     def run(self):
#         consumer = KafkaConsumer(Configurations.kafka['topic'], bootstrap_servers=Configurations.kafka['host'])
#         try:
#             for message in consumer:
#                 message_load = json.loads(message.value)
#                 _request = HttpRequest()
#                 _request.method = message_load['method']
#                 _request.path = message_load['path']
#                 _request.content_type = 'application/json'
#                 request = Request(_request)
#                 request.body = message_load['body']
#                 Binder.bind(message_load['key'], request,message_load['uuid'])
#
#
#         except:
#             traceback.print_exc()
#             consumer.close()
#             kafka_topic_consumer = KafkaTopicConsumer()
#             kafka_topic_consumer.start()
