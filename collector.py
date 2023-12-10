import requests
import json
import logging
import sqlite3
from datetime import datetime, timedelta
import time

# Configure logging to display messages with an INFO severity level or higher
logging.basicConfig(level=logging.INFO)

# Function to load configuration from the JSON file
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# Function to create a SQLite database and table for storing data
def create_database():
    conn = sqlite3.connect('homebridge_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS device_data 
                 (timestamp TEXT, device_id TEXT, current_temperature REAL, target_temperature REAL)''')
    conn.commit()
    conn.close()

# Main function to query the Homebridge API and store data
def main():
    # Load configuration data
    config = load_config()

    # Function to login and retrieve the access token
    def login():
        credentials = {
            "username": config["username"], 
            "password": config["password"], 
            "otp": config["otp"]
        }
        login_url = config["login_url"]
        response = requests.post(login_url, json=credentials)
        response.raise_for_status()
        token_info = response.json()
        return token_info['access_token'], datetime.now() + timedelta(seconds=token_info['expires_in'])

    # Function to insert data into the SQLite database
    def insert_data(timestamp, device_id, current_temperature, target_temperature):
        conn = sqlite3.connect('homebridge_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO device_data VALUES (?, ?, ?, ?)", 
                  (timestamp, device_id, current_temperature, target_temperature))
        conn.commit()
        conn.close()

    # Function to query the Homebridge API
    def query_homebridge_api(token):
        try:
            device_url = config["device_url"]
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(device_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            current_temperature = data['values']['CurrentTemperature']
            target_temperature = data['values']['TargetTemperature']

            insert_data(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "34f747c785c7", current_temperature, target_temperature)

        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")

    try:
        create_database()
        token, token_expiry = login()

        while True:  # Change to an infinite loop
            if datetime.now() >= token_expiry:
                token, token_expiry = login()
            
            query_homebridge_api(token)
            time.sleep(60)  # Wait for 60 seconds before the next iteration

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Execute the main function
main()
