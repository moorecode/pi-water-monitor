from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from tinydb import TinyDB, Query, where
from datetime import datetime
import json

app = Flask(__name__)
mqtt = Mqtt(app)
db = TinyDB('db.json')
flow_rates = db.table('flow-rate')
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
    payload = json.loads(message.payload.decode())
    print(payload)
    flow_rates.insert(payload)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    records = flow_rates.all()
    leak_threshold = status.get(where('name') == 'leak_threshold')
    if leak_threshold:
        leak_threshold = float(leak_threshold.get("value", 9999999))
    else: leak_threshold = 9999999
    water_cost_per_l = 2.60/1000 # https://www.teampoly.com.au/2018/06/15/water-prices-in-australia/ (Canberra low)
    data = {}
    leaks = []
    usage_sum = 0
    for record in records: # convert timestamp to strftime
        record_time = record['timestamp']
        record['timestamp'] = datetime.utcfromtimestamp(record['timestamp']).strftime('%y-%m-%d %H:%M:%S')
        usage_sum += record['value']
        record['plot'] = (record['value']/record['duration']) * 60 # L per min
        if record['plot'] > leak_threshold:
            record_copy = record.copy()
            record_copy['timestamp'] = datetime.utcfromtimestamp(record_time).strftime('%a %H:%M:%S')
            record_copy['plot'] = record_copy['plot'] - leak_threshold
            leaks.append(record_copy)
        if record['name'] in data:
            data[record['name']].append(record)
        else:
            data[record['name']] = [record]
    water_status = status.search(where('name') == 'water_status')
    monthly_cost = usage_sum*water_cost_per_l*30
    return render_template('dashboard.html', data=data, num_devices=len(data), 
    water_status=water_status, leaks=leaks, usage_sum=usage_sum, monthly_cost=monthly_cost)

@app.route('/settings', methods=['POST'])
def settings():
    print(request.form)
    if 'read_rate' in request.form:
        read_rate = request.form['read_rate']
        status.upsert({'name': 'read_rate', "value":read_rate}, where('name') == 'read_rate')
        mqtt.publish('water-monitor/control/water-main/read_rate', read_rate)
    if 'leak_threshold' in request.form:
        leak_threshold = request.form['leak_threshold']
        status.upsert({'name': 'leak_threshold', "value":leak_threshold}, where('name') == 'leak_threshold')
    return 'success'

@app.route('/controls', methods=['POST'])
def controls():
    water_status = status.get(where('name') == 'water_status')
    if water_status:
        water_status = water_status.get('value', 'True')
    water_status = not water_status
    status.upsert({'name':'water_status', 'value':water_status}, where('name') == 'water_status')
    mqtt.publish('water-monitor/control/water-main/switch', water_status)
    return str(water_status)


