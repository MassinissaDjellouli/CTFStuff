import random
import time
from paho.mqtt import client as mqtt_client

broker = ''
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc,props):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        
        client.subscribe('#', qos=1)

    def on_message(client, userdata, message):
        print('Topic: %s | QOS: %s  | Message: %s' % (message.topic, message.qos, message.payload))


    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.on_message = on_message
    return client

client = connect_mqtt()
client.loop_start()
while 1:
    continue