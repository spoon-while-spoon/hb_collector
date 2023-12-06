import requests
import json

def query_homebridge_api():
    url = "http://192.168.2.20:8181/api/accessories/34f747c785c7a0c34a651109d7ff14ca97622e7028a7a6587a9f7e8c4f41ec08"

    try:
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6IkFkbWluaXN0cmF0b3IiLCJhZG1pbiI6dHJ1ZSwiaW5zdGFuY2VJZCI6IjJiMGNiYzZmOTg0NDc0ZWE3ZTRkZjBjN2FiOTE2NTVkNjg3OWRhYTIzODJkMjA4N2Y5ZDViZGY2NjMzNjI3NjUiLCJpYXQiOjE3MDE4MTM3MDMsImV4cCI6MTcwMTg0MjUwM30.lJ3mQ3H1Ep0-thxtnsE6sI1o81kmm1zWxp7gX5s_vl0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        print("Response Status Code:", response.status_code)
        
        data = response.json()
        
       # print("JSON Response:", json.dumps(data))
    
        current_temperature = data['values']['CurrentTemperature']
        target_temperature = data['values']['TargetTemperature']
        
        print("Current Temperature:", current_temperature)
        print("Target Temperature:", target_temperature)
        
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

query_homebridge_api()
