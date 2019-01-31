from flask import Flask, render_template
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
db = TinyDB('db.json')
flow_rates=db.table('flow-rate')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    records = flow_rates.all()
    times = sorted([datetime.utcfromtimestamp(s["timestamp"]).strftime("%y-%m-%d %H:%M:%S")  for s in records])
    values = [s["value"] for s in records]
    return render_template('dashboard.html', times=times, values=values)