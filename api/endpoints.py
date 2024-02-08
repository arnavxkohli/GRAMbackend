from flask import render_template, request, jsonify, session
from api import app, auth, db
from enum import Enum

sensors = Enum('sensors', ['magnetic', 'air_quality', 'temperature', 'infrared', 'ultrasonic'])


# main api route; return method and timestamp
@app.route("/", methods=["GET", "POST", "PUT"])
def root():
    return "GRAM server"


@app.route("/user/signup", methods=["POST"])
def signup():
    if ('user' in session):
        return f"{session['user']} has successfully signed up"
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
            return jsonify({ "status": "failed", "message": "An Error Occurred" }), 400


@app.route("/user/signin", methods=["GET"])
def signin():
    if ('user' in session):
        return f"{session['user']} has successfully logged in"
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
            return jsonify({ "status": "failed", "message": "An Error Occurred" }), 400


@app.route("/user/addbin", methods=["POST"])
def add_bin():
    data = request.json
    if 'uId' not in data:
        return jsonify({ "status": "failed", "message": "User ID not given" }), 400
    if 'binId' not in data:
        return jsonify({ "status": "failed", "message": "Bin ID not given" }), 400

    uId, binId = data["uId"], data["binId"]

    try:
        # Check if the binId exists for the given uId
        bin_exists = db.child("Users").child(uId).child(binId).get().val()

        # If binId does not exist for the uId, add it
        if not bin_exists:
            db.child("Users").child(uId).child(binId).set(True)
            return jsonify({ "status": "success", "message": "Bin added to User" }), 200
        else:
            return jsonify({ "status": "failed", "message": "Bin already associated with the User" }), 400
    except Exception as e:
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400


@app.route("/bin/fetch", methods=["GET"])
def fetch_sensors():
    uId = request.args.get('uId')
    binId = request.args.get('binId')
    sensor_type = request.args.get('sensor_type')

    if not uId:
        return jsonify({ "status": "failed", "message": "User ID not given" }), 400
    if not binId:
        return jsonify({ "status": "failed", "message": "Bin ID not given" }), 400
    if not sensor_type or sensor_type not in sensors.__members__:
        return jsonify({ "status": "failed", "message": "Invalid or missing sensor type" }), 400

    try:
        bin_exists = db.child("Users").child(uId).child(binId).get().val()
        if not bin_exists:
            return jsonify({ "status": "failed", "message": f"Given user ID: {uId} does not own bin {binId}" }), 400

        sensor_data = db.child("Bins").child(binId).child(sensor_type).get().val()
        if not sensor_data:
            return jsonify({ "status": "failed", "message": f"No data available for {sensor_type}" }), 400
        return jsonify({ "status": "success", "message": "Data fetched successfully", "data": sensor_data }), 200

    except Exception as e:
        print("Error fetching data from Firestore:", str(e))
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400
