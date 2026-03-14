from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO, emit
import json, os, redis

app = Flask(__name__, static_folder='public')
app.config['SECRET_KEY'] = 'courtbooker2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

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

    # Broadcast to all connected clients instantly
    socketio.emit('bookings_updated', data)

    return jsonify({"ok": True, "data": data})

@app.route('/api/bookings', methods=['POST'])
def update_bookings():
    data = request.get_json()
    save_data(data)
    socketio.emit('bookings_updated', data)
    return jsonify({"ok": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    data = json.loads(json.dumps(DEFAULT_DATA))
    save_data(data)
    socketio.emit('bookings_updated', data)
    return jsonify({"ok": True})

@socketio.on('connect')
def on_connect():
    emit('bookings_updated', load_data())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
