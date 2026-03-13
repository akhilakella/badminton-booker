from flask import Flask, send_from_directory, jsonify, request
import json, os, redis

app = Flask(__name__, static_folder='public')

REDIS_URL = os.environ.get('REDIS_URL')
rdb = redis.from_url(REDIS_URL) if REDIS_URL else None
REDIS_KEY = 'courtbooker:bookings'

DEFAULT_DATA = {
    "monday": [
        {"time": "6:40 – 7:20 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "7:20 – 8:00 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "8:00 – 8:40 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
    ],
    "wednesday": [
        {"time": "6:40 – 7:20 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "7:20 – 8:00 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "8:00 – 8:40 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
    ],
    "thursday": [
        {"time": "6:00 – 6:40 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "6:40 – 7:20 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "7:20 – 8:00 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
    ],
}

def load_data():
    if rdb:
        val = rdb.get(REDIS_KEY)
        if val:
            return json.loads(val)
    return json.loads(json.dumps(DEFAULT_DATA))

def save_data(data):
    if rdb:
        rdb.set(REDIS_KEY, json.dumps(data))

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('public', 'manifest.json')

@app.route('/sw.js')
def sw():
    return send_from_directory('public', 'sw.js')

@app.route('/icon-192.svg')
def icon():
    return send_from_directory('public', 'icon-192.svg')

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(load_data())

@app.route('/api/bookings', methods=['POST'])
def update_bookings():
    data = request.get_json()
    save_data(data)
    return jsonify({"ok": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    save_data(json.loads(json.dumps(DEFAULT_DATA)))
    return jsonify({"ok": True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
