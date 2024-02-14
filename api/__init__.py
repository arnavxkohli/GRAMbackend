from flask import Flask
from flask_cors import CORS
import pyrebase
import requests

firebase_client_config = {
    "apiKey": "AIzaSyB5oYH_7CMXhDwPdMudUlhpNWrjmADxX6o",
    "authDomain": "gram-d45eb.firebaseapp.com",
    "databaseURL": "https://gram-d45eb-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "gram-d45eb",
    "storageBucket": "gram-d45eb.appspot.com",
    "messagingSenderId": "503701848987",
    "appId": "1:503701848987:web:2d97d058966bddc920973e"
}


# Initialize Firebase client
pb = pyrebase.initialize_app(firebase_client_config)

auth = pb.auth()

db = pb.database()

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


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = "ea9873ab493d0c43d24d89ee1f96080b91521d3c6ae0e0199a673ffef92e2021" #GRAM sha256 hash

    with app.app_context():
        push_public_ip()

    return app

app = create_app()

from api import endpoints




