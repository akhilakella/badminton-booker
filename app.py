from flask import Flask, send_from_directory, jsonify, request
import json, os, redis

app = Flask(__name__, static_folder='public')

REDIS_URL = os.environ.get('REDIS_URL')
rdb = redis.from_url(REDIS_URL) if REDIS_URL else None
REDIS_KEY = 'courtbooker:bookings'
ATT_KEY = 'courtbooker:attendance'

DEFAULT_DATA = {
    "monday": [
        {"time": "6:40 \u2013 7:20 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "7:20 \u2013 8:00 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "8:00 \u2013 8:40 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
    ],
    "wednesday": [
        {"time": "6:40 \u2013 7:20 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "7:20 \u2013 8:00 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "8:00 \u2013 8:40 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
    ],
    "thursday": [
        {"time": "6:00 \u2013 6:40 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "6:40 \u2013 7:20 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
        {"time": "7:20 \u2013 8:00 pm", "players": [{"name": "", "booked": False, "court": None}, {"name": "", "booked": False, "court": None}]},
    ],
}

DEFAULT_ATT = {
    "monday":    {"Phani": False, "Sunil": False, "Niranjan": False, "Mohan": False, "Sainath": False, "Pavan": False},
    "wednesday": {"Phani": False, "Sunil": False, "Niranjan": False, "Mohan": False, "Sainath": False, "Pavan": False},
    "thursday":  {"Phani": False, "Sunil": False, "Niranjan": False, "Mohan": False, "Sainath": False, "Pavan": False},
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

def load_att():
    if rdb:
        val = rdb.get(ATT_KEY)
        if val:
            return json.loads(val)
    return json.loads(json.dumps(DEFAULT_ATT))

def save_att(data):
    if rdb:
        rdb.set(ATT_KEY, json.dumps(data))

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

@app.route('/api/update-player', methods=['POST'])
def update_player():
    body = request.get_json()
    day = body.get('day')
    slot_idx = body.get('slotIdx')
    player_idx = body.get('playerIdx')
    player = body.get('player')
    if day not in DEFAULT_DATA or slot_idx is None or player_idx is None:
        return jsonify({"ok": False, "error": "Invalid request"}), 400
    data = load_data()
    data[day][slot_idx]['players'][player_idx] = player
    save_data(data)
    return jsonify({"ok": True, "data": data})

@app.route('/api/bookings', methods=['POST'])
def update_bookings():
    data = request.get_json()
    # Reject empty or suspiciously small payloads that would wipe data
    if not data or not isinstance(data, dict) or len(str(data)) < 100:
        return jsonify({"ok": False, "error": "Rejected empty payload"}), 400
    save_data(data)
    return jsonify({"ok": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    save_data(json.loads(json.dumps(DEFAULT_DATA)))
    return jsonify({"ok": True})

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    return jsonify(load_att())

@app.route('/api/attendance', methods=['POST'])
def update_attendance():
    body = request.get_json()
    day = body.get('day')
    name = body.get('name')
    present = body.get('present')
    att = load_att()
    if day not in att:
        att[day] = {}
    att[day][name] = present
    save_att(att)
    return jsonify({"ok": True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
