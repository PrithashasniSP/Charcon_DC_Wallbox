# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client

#Configuration
#broker = '192.168.0.2'
broker = 'localhost'
port = 1883

lastSentTime = {}

#List of Topics
Topics = [
    "DCWallbox/HMI/PageName/AllPage",
    "DCWallbox/HMI/PageName/DeviceFailure",
    "DCWallbox/HMI/PageName/MissingConfig",
    "DCWallbox/HMI/PageName/HealthCheck",
    "DCWallbox/HMI/PageName/ReadyToCharge",
    "DCWallbox/HMI/PageName/ChargingInitPage",
    "DCWallbox/HMI/PageName/ChargingProgressPage",
]

for topic in Topics:
    lastSentTime[topic] = time.perf_counter()


# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, topic, msg):
    
    status = 1
    
    # Send topic with aleast 1s delay
    if time.perf_counter() > lastSentTime[topic] + 1: 
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        lastSentTime[topic] = time.perf_counter()
        
    
    return status
    
# def run():
#     client = connect_mqtt()
#     client.loop_start()
    
#     msg_count = 1
#     msg_content = "Hello!"
        
#     while True:
#         msg = f"Message no. {msg_count}\t{msg_content}"
#         status = publish(client, AllPage, msg)
#         if status == 0:
#             print(f"Send `{msg}` to topic `{AllPage}`")
#         else:
#             print(f"Failed to send message to topic {AllPage}")
        
#         msg_count += 1
#         if msg_count > 50:
#             break
        
#     client.loop_stop()


# if __name__ == '__main__':
#     run()
