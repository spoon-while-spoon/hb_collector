import requests
import json
import logging
import sqlite3
from datetime import datetime, timedelta
import time

# Configure logging to display messages with an INFO severity level or higher
logging.basicConfig(level=logging.INFO)

# Function to create a SQLite database and table for storing data
def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('homebridge_data.db')
    c = conn.cursor()
    # Create a table named 'device_data' if it doesn't exist with specific columns
    c.execute('''CREATE TABLE IF NOT EXISTS device_data 
                 (timestamp TEXT, device_id TEXT, current_temperature REAL, target_temperature REAL)''')
    # Commit changes and close the connection to the database
    conn.commit()
    conn.close()

# Function to login and retrieve the access token
def login():
    # API endpoint for login
    login_url = "http://192.168.2.20:8181/api/auth/login"
    # Credentials for login (username, password, and one-time password)
    credentials = {"username": "admin", "password": "admin", "otp": "string"}
    # Post request to the login endpoint with the credentials
    response = requests.post(login_url, json=credentials)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    # Parse the response JSON to get the token information
    token_info = response.json()
    # Return the access token and its expiry time
    return token_info['access_token'], datetime.now() + timedelta(seconds=token_info['expires_in'])

# Function to insert data into the SQLite database
def insert_data(timestamp, device_id, current_temperature, target_temperature):
    # Connect to the SQLite database
    conn = sqlite3.connect('homebridge_data.db')
    c = conn.cursor()
    # Insert the provided data into the 'device_data' table
    c.execute("INSERT INTO device_data VALUES (?, ?, ?, ?)", 
              (timestamp, device_id, current_temperature, target_temperature))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Main function to query the Homebridge API and store data
def query_homebridge_api(token):
    try:
        # API endpoint for querying the Homebridge accessory
        url = "http://192.168.2.20:8181/api/accessories/34f747c785c7a0c34a651109d7ff14ca97622e7028a7a6587a9f7e8c4f41ec08"
        # Set the authorization header with the bearer token
        headers = {"Authorization": f"Bearer {token}"}
        # Send a GET request to the API
        response = requests.get(url, headers=headers)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        # Parse the JSON response
        data = response.json()
        
        # Extract the required values (current and target temperatures)
        current_temperature = data['values']['CurrentTemperature']
        target_temperature = data['values']['TargetTemperature']

        # Store the extracted values in the database
        insert_data(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "34f747c785c7", current_temperature, target_temperature)

    except requests.RequestException as e:
        # Log any request-related errors
        logging.error(f"API request failed: {e}")

# Test run main function
def main():
    try:
        # Create the database and table
        create_database()
        # Login to the API and retrieve the token and its expiry time
        token, token_expiry = login()

        # Loop to run the process 5 times
        for _ in range(5):
            # Renew the token if it has expired
            if datetime.now() >= token_expiry:
                token, token_expiry = login()
            
            # Query the Homebridge API and store the data
            query_homebridge_api(token)
            # Wait for 60 seconds before the next iteration
            time.sleep(60)

    except Exception as e:
        # Log any exceptions
        logging.error(f"An error occurred: {e}")

# Execute the main function
main()