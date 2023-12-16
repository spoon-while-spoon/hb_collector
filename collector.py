import requests
import logging
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to create a MySQL database and table for storing data
def create_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS device_data 
                             (timestamp TEXT, device_id TEXT, current_temperature REAL, target_temperature REAL)''')
            connection.commit()
            cursor.close()
    except Error as e:
        logging.error(f"Error connecting to MySQL DB: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to login and retrieve the access token
def login():
    credentials = {
        "username": os.getenv('API_USERNAME'), 
        "password": os.getenv('API_PASSWORD'), 
        "otp": os.getenv('API_OTP')
    }
    login_url = os.getenv('API_LOGIN_URL')
    response = requests.post(login_url, json=credentials)
    response.raise_for_status()
    token_info = response.json()
    return token_info['access_token'], datetime.now() + timedelta(seconds=token_info['expires_in'])

# Function to insert data into the MySQL database
def insert_data(timestamp, device_id, current_temperature, target_temperature):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO device_data VALUES (%s, %s, %s, %s)", 
                           (timestamp, device_id, current_temperature, target_temperature))
            connection.commit()
            cursor.close()
    except Error as e:
        logging.error(f"Error connecting to MySQL DB: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to query the Homebridge API
def query_homebridge_api(token):
    try:
        device_url = os.getenv('API_DEVICE_URL')
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(device_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        current_temperature = data['values']['CurrentTemperature']
        target_temperature = data['values']['TargetTemperature']

        insert_data(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "34f747c785c7", current_temperature, target_temperature)

    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")

def main():
    try:
        create_database()
        token, token_expiry = login()

        while True:  
            if datetime.now() >= token_expiry:
                token, token_expiry = login()
            
            query_homebridge_api(token)
            time.sleep(60)  # Wait for 60 seconds before the next iteration

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Execute the main function
if __name__ == "__main__":
    main()
