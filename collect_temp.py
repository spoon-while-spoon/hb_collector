import requests
import json
import time
from datetime import datetime, timedelta

def login():
    login_url = "http://192.168.2.20:8181/api/auth/login"
    credentials = {"username": "admin", "password": "admin", "otp": "string"}
    response = requests.post(login_url, json=credentials)
    response.raise_for_status()
    token_info = response.json()
    return token_info['access_token'], datetime.now() + timedelta(seconds=token_info['expires_in'])

def query_homebridge_api(token):
    url = "http://192.168.2.20:8181/api/accessories/34f747c785c7a0c34a651109d7ff14ca97622e7028a7a6587a9f7e8c4f41ec08"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()


token, token_expiry = login()

# API loop
while True:
    
    if datetime.now() >= token_expiry:
        token, token_expiry = login()

    query_homebridge_api(token)
    time.sleep(60)  # wait 60
