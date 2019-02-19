from sensors import water_sensor
from controllers import Controller
from reader import Reader
from time import sleep
from paho.mqtt import client as mqtt
import time

sensors = []
controllers = []
readers = []


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("water-monitor/control/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic, str(msg.payload))
    for controller in controllers:
        if controller.name in msg.topic:
            print("controller action", controller.name)
            controller.set_state(msg.payload.decode("utf-8") )
            break


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.0.0.7", 1883, 60)

def on_read(name, value):
    client.publish("water-monitor/"+ name + "/flow-rate", payload=value, qos=2, retain=False)
    print("publish", "water-monitor/"+ name + "/flow-rate:", value)

reader1 = Reader("water-main", 20)
readers.append(reader1)

water_sensor1 = water_sensor(
    "water-main", read_rate=5, on_read=on_read, read=reader1.read)
water_sensor1.read_loop_start()

controller1 = Controller("water-main", 18)
controllers.append(controller1)


client.loop_start()

def teardown():
    for controller in controllers:
        controller.teardown()

    water_sensor1.read_loop_stop()
    client.loop_stop()
    client.disconnect()
try:
    while True:
        pass
except KeyboardInterrupt:
    teardown()

teardown()
    
