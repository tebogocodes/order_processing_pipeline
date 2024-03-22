from flask import Flask, request, jsonify
import requests
import logging
from threading import Thread
from functools import wraps
from collections import defaultdict

app = Flask(__name__)

SERVICE_NOW_BASE_URL = "https://your-service-now-url"
USER = "your-username"
PWD = "your-password"

# Store seen imsis to avoid duplicate calls
seen_imsis = defaultdict(bool)

# Decorator to make the function run in a separate thread
def async_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper

# Function to call the second service
@async_thread
def call_second_service(imsi):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = SERVICE_NOW_BASE_URL + f"/api/mws/5g/service_event"
    params = {
        "imsi": imsi,
        "state": "active"
    }
    response = requests.get(url, auth=(USER, PWD), headers=headers, params=params)
    logging.debug(f"Response from second service: {response.text}")

# Main endpoint
@app.route("/service_live", methods=["POST"])
def service_live():
    imsi = request.form.get('imsi')
    if imsi is None:
        return jsonify({'message': 'imsi is required'}), 400

    if not seen_imsis[imsi]:
        seen_imsis[imsi] = True
        call_second_service(imsi)

    return jsonify({'message': 'Success'}), 200