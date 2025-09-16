# python3.6

import random

from paho.mqtt import client as mqtt_client
import Signals


broker = '127.0.0.1'
port = 1883

#List of Topics
Topics = [
    "DCWallbox/HMI/PageName/ChargingProgressPageStop"
]


# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        Signals.StopChargingHMI = True

    for topic in Topics:
        client.subscribe(topic)
        client.on_message = on_message


def MQTT_Sub_Start():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
