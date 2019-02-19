from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from tinydb import TinyDB, Query, where
from datetime import datetime

app = Flask(__name__)
mqtt = Mqtt(app)
db = TinyDB('db.json')
flow_rates=db.table('flow-rate')
status=db.table('status')

app.config['MQTT_BROKER_URL'] = '10.0.0.7'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('water-monitor/#')
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    records = flow_rates.all()
    data = {}
    for record in records: # convert timestamp to strftime
        record["timestamp"] = datetime.utcfromtimestamp(record["timestamp"]).strftime("%y-%m-%d %H:%M:%S")
        if record["name"] in data:
            data[record["name"]].append(record)
        else:
            data[record["name"]] = [record]
    water_status = status.search(where('name') == 'water_status')
    return render_template('dashboard.html', data=data, num_devices=len(data), water_status=water_status)

@app.route('/settings', methods=['POST'])
def settings():
    print('#######################',request.form)
    return "success"

@app.route('/controls', methods=['POST'])
def controls():
    water_status = status.get(where('name') == 'water_status')["value"]
    water_status = not water_status
    status.upsert({'name':'water_status', 'value':water_status}, where('name') == 'water_status')
    print("publishing")
    mqtt.publish("water-monitor/control/water-main/switch", water_status)
    return str(water_status)


