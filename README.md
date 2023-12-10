# Homebridge Collector SL 

Documentation on how to setup the serverless version of the Homebridge Collector. 

## Overview

This tool is a serverless version of the main Homebridge Data Collector Project. Its purpose is to periodically gather specific data from a Homebridge server, such as the current and target temperatures of connected devices, and store it in a local SQLite database. This software is perfect for those seeking an effortless, serverless approach to monitoring and storing Homebridge device data.

## Features

- **Automated data retrieval**: The script automates queries to a Homebridge server at intervals of 60 seconds by default.
- **Data storage in SQLite**: All retrieved data is stored in a SQLite database for easy management and analysis.
- **Straightforward configuration**: User data and endpoints are saved in a separate configuration file, simplifying the customization process.

## Setup and Configuration

1. **Clone Repository:** Copy this repository to your local computer.
    
2. **Install Dependencies:** Proceed with installing the necessary Python prerequisites listed in the `requirements.txt` file.
    
3. **Edit Configuration File**: Please edit the `config.json` file located in the root directory of the project.
    
4.  **Add User Data**: Next, please add your Homebridge server data to `config.json`. Make sure to follow this format:

```json
    {
    "username": "HOMEBRIDGE-USERNAME",
    "password": "HOMEBRIDGE-PASSWORD",
    "otp": "string",
    "login_url": "http://HOMEBRIDGE-IP-ADRESS:PORT/api/auth/login",
    "device_url": "http://HOMEBRDIGE-IP-ADRESS:PORT/api/accessories/UNIQUE-ID"
}
```


Replace `HOMEBRIDGE-USERNAME`, `HOMEBRIDGE-PASSWORD`, `HOMEBRIDGE-IP-ADRESS:PORT` and `UNIQUE-ID` with your actual data. 
## UNIQUE-ID

You can get your Devices `UNIQUE-ID`by  using the Swagger UI of your homebridge. 
Open  http://HOMEBRIDGE-IP-ADRESS:PORT/swagger in your browser to access the UI. 

A faster way would be through SSH or directly in the Homebridge Console in your Browser. 
Just paste the following curl command with your replaced data to get a Token:
```bash
curl -X 'POST' \
  'http://HOMEBRIDGE-IP-ADRESS:PORT/api/auth/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "HOMEBRIDGE-USERNAME",
  "password": "HOMEBRIDGE-PASSWORD",
  "otp": "string"
}'
```
 
Your respond should look like that: 
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6IkFkbWluaXN0cmF0b3IiLCJhZG1pbiI6dHJ1ZSwiaW5zdGFuY2VJZCI6IjJiMGNiYzZmOTg0NDc0ZWE3ZTRkZjBjN2FiOTE2NTVkNjg3OWRhYTIzODJkMjA4N2Y5ZDViZGY2NjMzNjI3NjUiLCJpYXQiOjE3MDIyMDU1NjUsImV4cCI6MTcwMjIzNDM2NX0.89M3FO4DpVR0Jgnj2YL7HpEgAXmylWmG0rvqfODeZ7g",
  "token_type": "Bearer",
  "expires_in": 28800
}
```
Then use the given token in the following command to  get a JSON respond with the data for all accessories. These files can get quite large and depending on the form of request often unformatted so I recommend you use some form of formatter. 

```json
curl -X 'GET' \
  'http://192.168.2.20:8181/api/accessories' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6IkFkbWluaXN0cmF0b3IiLCJhZG1pbiI6dHJ1ZSwiaW5zdGFuY2VJZCI6IjJiMGNiYzZmOTg0NDc0ZWE3ZTRkZjBjN2FiOTE2NTVkNjg3OWRhYTIzODJkMjA4N2Y5ZDViZGY2NjMzNjI3NjUiLCJpYXQiOjE3MDIyMjc0MzYsImV4cCI6MTcwMjI1NjIzNn0.msbNbg3c1hUUNlY1eeEMOOtfbfvb6GyzMiqRV1omIzM'
```

## Run the Script 

Start the script by typing 'python main.py'.

The script will begin gathering data from your Homebridge server and saving it in the database.
Please ensure you have the most recent version of Python installed.
This script is suitable for serverless environments and does not require a permanent server connection.
