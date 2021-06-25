import kafka
import time

bootstrap_servers = ['localhost:9092']
topicName = 'First'
producer = kafka.KafkaProducer(bootstrap_servers = bootstrap_servers)
for i in range(100):
    producer.send(topicName, bytearray('hello from Python '+str(i),encoding='utf-8'))
    time.sleep(2)
    producer.flush()
