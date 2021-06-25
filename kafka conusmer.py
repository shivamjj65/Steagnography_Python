from kafka import KafkaConsumer
import sys

bootstrap_servers = ['localhost:9092']
topicName = 'First'
consumer = KafkaConsumer(topicName,bootstrap_servers=bootstrap_servers,auto_offset_reset="latest",group_id='group_1')
for message in consumer:
    print(message.value)