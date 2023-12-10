import requests
import json
import logging
import sqlite3
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.INFO)

def create_database():
    conn = sqlite3.connect('homebridge_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS device_data 
                 (timestamp TEXT, device_id TEXT, current_temperature REAL, target_temperature REAL)''')
    conn.commit()
    conn.close()

def login():
    login_url = "http://192.168.2.20:8181/api/auth/login"
    credentials = {"username": "admin", "password": "admin", "otp": "string"}
    response = requests.post(login_url, json=credentials)
    response.raise_for_status()
    token_info = response.json()
    return token_info['access_token'], datetime.now() + timedelta(seconds=token_info['expires_in'])

def insert_data(timestamp, device_id, current_temperature, target_temperature):
    conn = sqlite3.connect('homebridge_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO device_data VALUES (?, ?, ?, ?)", 
              (timestamp, device_id, current_temperature, target_temperature))
    conn.commit()
    conn.close()

def query_homebridge_api(token):
    try:
        url = "http://192.168.2.20:8181/api/accessories/34f747c785c7a0c34a651109d7ff14ca97622e7028a7a6587a9f7e8c4f41ec08"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        current_temperature = data['values']['CurrentTemperature']
        target_temperature = data['values']['TargetTemperature']

      
        insert_data(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "34f747c785c7", current_temperature, target_temperature)

    except requests.RequestException as e:
        logging.error(f"API-Anfrage fehlgeschlagen: {e}")

def main():
    try:
        create_database()
        token, token_expiry = login()

        for _ in range(5): 
            if datetime.now() >= token_expiry:
                token, token_expiry = login()
            
            query_homebridge_api(token)
            time.sleep(60)  

    except Exception as e:
        logging.error(f"Ein Fehler ist aufgetreten: {e}")

main()