from sensors import water_sensor
from time import sleep
from paho.mqtt import client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("water-monitor/control/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.0.0.7", 1883, 60)


def on_read(name, value):
    client.publish(f"water-monitor/{name}/flow-rate",
                   payload=value, qos=2, retain=True)


water_sensor = water_sensor(
    "water-main", read_rate=5, on_read=on_read)
water_sensor.read_loop_start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while True:
    pass

water_sensor.read_loop_stop()
client.loop_stop()
client.disconnect