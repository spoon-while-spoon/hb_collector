# Homebridge Sensor Data Collector

## Overview
The Homebridge Sensor Data Collector is a Python-based tool for periodically collecting sensor data from Homebridge-enabled devices. The script interfaces with the Homebridge API to retrieve data, such as temperature readings, and stores it in a SQLite database for further analysis and usage. This tool is ideal for home automation enthusiasts and professionals looking to monitor and analyze data from their Homebridge devices.

## Features
Fetches sensor data from Homebridge API.
Stores data in a local SQLite database.
Easy to set up and run using Docker.

## Prerequisites

- Docker
- Homebridge setup with accessible API

## Setup and Configuration

### 1. Configure Homebridge API Access
Before running the script, ensure your Homebridge API is set up and accessible. You will need the following information:

- Homebridge username and password
- Homebridge API URL and Device URL

### 2. Configuration File (config.json)
Edit the config.json file with your Homebridge details:

```json
{
    "username": "YOUR_HOMEBRIDGE_USERNAME",
    "password": "YOUR_HOMEBRIDGE_PASSWORD",
    "otp": "YOUR_ONE_TIME_PASSWORD_IF_USED",
    "login_url": "http://YOUR_HOMEBRIDGE_IP:PORT/api/auth/login",
    "device_url": "http://YOUR_HOMEBRIDGE_IP:PORT/api/accessories/YOUR_DEVICE_UNIQUE_ID"
}
```
- Replace `YOUR_HOMEBRIDGE_USERNAME` and `YOUR_HOMEBRIDGE_PASSWORD` with your Homebridge credentials.
- Adjust `YOUR_HOMEBRIDGE_IP` and `PORT` to match your Homebridge server address and port.
- For `YOUR_DEVICE_UNIQUE_ID`, refer to your Homebridge device's unique identifier.

### Obtaining Device Unique ID using Swagger UI

To obtain the unique ID of your device through the Homebridge API using Swagger UI, you need to first get an authentication token and then use this token to access the device information. Here’s how to do it step-by-step:

Step 1: Getting an Authentication Token
-  **Access Swagger UI:** Open your web browser and navigate to the Swagger UI for your Homebridge instance. The URL typically looks like `http://YOUR_HOMEBRIDGE_IP:PORT/swagger#`

- Use /api/auth/login Endpoint: 
In Swagger UI, find and select the /api/auth/login endpoint. This endpoint is used for authenticating and obtaining a token.

- Enter Credentials: In the request body section of this endpoint, enter your Homebridge username, password, and one-time password (OTP) if used. It should look like this:

```json
{
  "username": "admin",
  "password": "admin",
  "otp": "optional-otp"
}
```

Execute Request: Click the 'Execute' button to send the request.

Copy the Token: Once the request is successful, you will receive a response that includes the access_token. Copy this token as it will be used in the next step.

Example Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "Bearer",
  "expires_in": 28800
}
```
Using Curl: Alternatively, you can use a curl command in a terminal or SSH session to get the token. Here's an example of the curl command:

```bash
curl -X 'POST' \
  'http://192.168.2.20:8181/api/auth/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
      "username": "admin",
      "password": "admin",
      "otp": "optional-otp"
  }'
```

Step 2: Getting the Unique Device ID
Navigate to /api/accessories Endpoint: In Swagger UI, locate the /api/accessories endpoint.

Use the Token: In the authorization section of this endpoint, enter the token you obtained earlier. It should be included as a Bearer token in the header.

Execute Request: Click 'Execute' to send the request with the token.

Find the Unique ID: The response will include a list of all connected Homebridge accessories. Look through the list to find the unique ID of the device you are interested in.

Curl Command: You can also use curl for this request:

```bash 
curl -X 'GET' \
  'http://192.168.2.20:8181/api/accessories' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Replace YOUR_ACCESS_TOKEN with the token you obtained.

 ### Automation in the Script
 
In the collector.py script, the process of requesting and renewing the access token is automated. The script logs in to the Homebridge API using the credentials provided in config.json and stores the received token. Before each API call, it checks if the token is near expiration and automatically renews it if necessary. This ensures continuous and uninterrupted access to the API for data collection without manual intervention.

### 3. Building and Running with Docker

Run the following commands to build and run the Docker container:

```bash
docker build -t homebridge-collector .
docker run -d homebridge-collector
```

### Data Storage
Sensor data collected from the Homebridge API is stored in a SQLite database (homebridge_data.db) within the Docker container. This database can be queried for data analysis and monitoring purposes.

### Contributing
Contributions to enhance this project are welcome. Please fork the repository and submit pull requests for review.












I need you to add a further description on how to get the uniqueId of your device using the SwaggerUi first du get a token via /api/auth/login and then to call the /api/accessories to get all deivces xconnected to the homebridge to find thier UniqueID. 

/api/auth/login
Exchange a username and password for an authentication token.

Parameters
Cancel
Reset
No parameters

Request body

application/json
{
  "username": "admin",
  "password": "admin",
  "otp": "string"
}
Execute
Clear
Responses
Curl

curl -X 'POST' \
  'http://192.168.2.20:8181/api/auth/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
  "password": "admin",
  "otp": "string"
}'
Request URL
http://192.168.2.20:8181/api/auth/login
Server response
Code	Details
201	
Response body
Download
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6IkFkbWluaXN0cmF0b3IiLCJhZG1pbiI6dHJ1ZSwiaW5zdGFuY2VJZCI6IjJiMGNiYzZmOTg0NDc0ZWE3ZTRkZjBjN2FiOTE2NTVkNjg3OWRhYTIzODJkMjA4N2Y5ZDViZGY2NjMzNjI3NjUiLCJpYXQiOjE3MDI0MTUwOTMsImV4cCI6MTcwMjQ0Mzg5M30.KRivjovNWYHFcoJTES9zi2I3H15DRBPKZ4avOYrE48k",
  "token_type": "Bearer",
  "expires_in": 28800
}
Response headers
 connection: keep-alive 
 content-length: 368 
 content-security-policy: default-src 'self';script-src 'self' 'unsafe-inline' 'unsafe-eval';style-src 'self' 'unsafe-inline';img-src 'self' data: https://raw.githubusercontent.com https://user-images.githubusercontent.com;connect-src 'self' https://openweathermap.org https://api.openweathermap.org wss://192.168.2.20:8181 ws://192.168.2.20:8181 
 content-type: application/json; charset=utf-8 
 date: Tue,12 Dec 2023 21:04:53 GMT 
 keep-alive: timeout=72 
 origin-agent-cluster: ?1 
 referrer-policy: no-referrer 
 vary: Origin 
 x-content-type-options: nosniff 
 x-dns-prefetch-control: off 
 x-download-options: noopen 
 x-permitted-cross-domain-policies: none 
 x-xss-protection: 0 
Responses
Code	Description	Links
201

Accessories


GET
/api/accessories
Return a list of Homebridge accessories.


Homebridge must be running in "insecure" mode to access the accessory list.

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
