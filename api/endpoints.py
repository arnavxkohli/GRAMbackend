from flask import render_template, request, jsonify, session
from firebase_admin import auth
import pyrebase

from api import app, auth_client, db

# main api route; return method and timestamp
@app.route("/", methods=["GET", "POST", "PUT"])
def root():
    return "GRAM webpage"

@app.route("/user/signup", methods=["GET","POST"])
def signup():
    if ('user' in session):
        return f"{session['user']} has successfully signed up"
    if request.method == "POST":
        data = request.json
        email = data.get('email')
        password = data.get('password')
        try:
            user = auth_client.create_user_with_email_and_password(email, password)
            
        except Exception as e:
            return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400
        else:
            if user:
                session['user'] = email
                return jsonify({ "status": "success", "message": "Sign Up successful" }), 200
            else:
                return jsonify({ "status": "failed", "message": "An Error Occurred" }), 200
            
            
@app.route("/user/signin", methods=["GET","POST"])
def signin():
    if ('user' in session):
        return f"{session['user']} has successfully logged in"
    if request.method == "POST":
        data = request.json
        email = data.get('email')
        password = data.get('password')
        try:
            # Sign in the user with email and password using Pyrebase
            user = auth_client.sign_in_with_email_and_password(email, password)
            
        except Exception as e:
            return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400
        else:
            if user:
                session['user'] = email
                return jsonify({ "status": "success", "message": "Sign In successful" }), 200
            else:
                return jsonify({ "status": "failed", "message": "An Error Occurred" }), 200


    