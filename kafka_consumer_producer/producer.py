# import json
#
# from kafka import KafkaProducer
#
# from biller.config import Configurations
#
#
# class KafkaTopicProducer:
#
#     @staticmethod
#     def push(path, method, body, key, uuid):
#         prod = KafkaProducer(bootstrap_servers=Configurations.kafka['host'])
#         try:
#             message = json.dumps({'body': body, 'path': path, 'method': method, 'key': key, 'uuid': uuid})
#             message_bytes = message.encode('utf-8')
#             prod.send(Configurations.kafka['topic'], value=message_bytes)
#         except Exception:
#             prod.close()
#
#     @staticmethod
#     def check_kafka(func):
#         def check(*args, **kwargs):
#             if Configurations.kafka['enable']:
#                 result = func(*args, **kwargs)
#                 return result
#             return False
#
#         return check
