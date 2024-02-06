from flask import render_template, request, jsonify, session
import pyrebase

from api import app, auth, db

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
            user = auth.create_user_with_email_and_password(email, password)
            
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
            user = auth.sign_in_with_email_and_password(email, password)
            
        except Exception as e:
            return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400
        else:
            if user:
                session['user'] = email
                return jsonify({ "status": "success", "message": "Sign In successful" }), 200
            else:
                return jsonify({ "status": "failed", "message": "An Error Occurred" }), 200
            
@app.route("/bin/init", methods=["GET","POST"])
def init_bin():
    if request.method == "POST":
        data = request.json
        userId = data.get('uid')
        binId = data.get('binId')
        
        # mm = magnetometer ir = InfraRed us = UltraSonic t = Temperature aq = Air Quality
        
        mm = data.get('mm_value')
        ir = data.get('ir')
        us = data.get('us')
        t = data.get('t')
        aq = data.get('aq')
        
        camera_value = "img.jpg" # future works
        
        try:
            data = {"binID": binId, "mm": mm, "ir": ir, "us":us, "t": t, "aq":aq}
            db.child("Bins").child(userId).set(data)
            
        except Exception as e:
            return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400
        else:
            return jsonify({ "status": "success", "message": "Bin initialised successfully" }), 200
            # else:
            #     return jsonify({ "status": "failed", "message": "An Error Occurred" }), 200



    