import requests
from api import db

def push_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            print('Success!!!')
            db.child("IP").set(response.text)
        else:
            print("Error: Unable to get IP address")
    except Exception as e:
        return f"Error: {e}"

