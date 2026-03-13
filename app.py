from flask import Flask, send_from_directory, jsonify, request
import json, os

app = Flask(__name__, static_folder='public')

DATA_FILE = 'bookings.json'

DEFAULT_DATA = {
    "monday": [
        {"time": "6:40 – 7:20 pm", "players": [{"name": "Akhil", "booked": False}, {"name": "Sumedh", "booked": False}]},
        {"time": "7:20 – 8:00 pm", "players": [{"name": "Pujitha", "booked": False}, {"name": "Advaith", "booked": False}]},
        {"time": "8:00 – 8:40 pm", "players": [{"name": "Praneeth", "booked": False}, {"name": "Hasini", "booked": False}]},
    ],
    "wednesday": [
        {"time": "6:40 – 7:20 pm", "players": [{"name": "Akhil", "booked": False}, {"name": "Sumedh", "booked": False}]},
        {"time": "7:20 – 8:00 pm", "players": [{"name": "Pujitha", "booked": False}, {"name": "Advaith", "booked": False}]},
        {"time": "8:00 – 8:40 pm", "players": [{"name": "Praneeth", "booked": False}, {"name": "Hasini", "booked": False}]},
    ],
    "thursday": [
        {"time": "6:40 – 7:20 pm", "players": [{"name": "Akhil", "booked": False}, {"name": "Sumedh", "booked": False}]},
        {"time": "7:20 – 8:00 pm", "players": [{"name": "Pujitha", "booked": False}, {"name": "Advaith", "booked": False}]},
        {"time": "8:00 – 8:40 pm", "players": [{"name": "Praneeth", "booked": False}, {"name": "Hasini", "booked": False}]},
    ],
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return json.loads(json.dumps(DEFAULT_DATA))

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('public', 'manifest.json')

@app.route('/sw.js')
def sw():
    return send_from_directory('public', 'sw.js')

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
    d = json.loads(json.dumps(DEFAULT_DATA))
    save_data(d)
    return jsonify({"ok": True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
