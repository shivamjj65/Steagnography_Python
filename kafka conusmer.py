import os.path
from datetime import datetime
import yaml
from kafka import KafkaConsumer
import config_loader

bootstrap_servers = config_loader.read('''data['kafka']['bootstrap_servers']''')
topicName = config_loader.read('''data['kafka']['topic']''')

consumer = KafkaConsumer(topicName, bootstrap_servers=bootstrap_servers, auto_offset_reset="earliest", auto_commit_interval_ms=1)

dir_path = config_loader.read('''data['environment']['receive_path']''')
offset = config_loader.read('''data['last_offset']['offset']''')

date = datetime.now().strftime("%Y_%m_%d-%I-%M_%S")

if not os.path.isdir(config_loader.read('''data['environment']['receive_path']''')):
    os.mkdir(config_loader.read('''data['environment']['receive_path']'''))

with open(os.path.join(dir_path, date+".PNG"), "ab") as file:    # receiving messages from the consumer and writing
                                                                 # to an image file with current timestamp
    for message in consumer:
        if message.offset > offset:

            if message.value == b'start':
                print('start offset')
                continue
                # print(message)

            elif message.value == b'stop':                        # saves the last offset read by the consumer
                print("end offset")
                # print(message)
                with open('config.yaml', 'r+') as config_file:
                    data = yaml.safe_load(config_file)
                    data['last_offset']['offset']= message.offset

                with open('config.yaml', 'w') as config_file:
                    new_data = yaml.dump(data, config_file)

                exit(0)

            else:
                file.write(message.value)
                # print(message.offset)

