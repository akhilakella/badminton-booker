import os
from flask import Flask
import redis

# 1. This is the 'app' variable Gunicorn is looking for!
app = Flask(__name__)

# 2. Setup Redis using the environment variable you just added
redis_url = os.environ.get('REDIS_URL')
r = redis.from_url(redis_url)

# 3. Your Reset Code
RESET_CODE = "7777"

# 4. Your validation function
def validate_code(input_code):
    if input_code.isdigit() and len(input_code) == 4:
        return input_code == RESET_CODE
    return False

# 5. Add a basic route so you can test if it's working
@app.route('/')
def hello():
    return "Badminton Booker is Online!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
