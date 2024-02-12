from flask import request, jsonify, session
from api import app, auth, db
from enum import Enum
from datetime import datetime

sensors = Enum('sensors', ['magnetic', 'air_quality', 'temperature', 'infrared', 'ultrasonic'])
AQ_THRESHOLD = 800
MAGNETIC_THRESHOLD = 800
US_THRESHOLD = 800


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

    uId, binId = data.get("uId"), data.get("binId")

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


@app.route("/bin/write", methods=["PUT"])
def write_to_db():
    binId = request.json.get("binId")
    sensor_type = request.json.get("sensor_type") # might need to change this later
    sensor_data = request.json.get("sensor_data")

    if not binId:
        return jsonify({ "status": "failed", "message": "Bin ID not given" }), 400
    if not sensor_type or sensor_type not in sensors.__members__:
        return jsonify({ "status": "failed", "message": "Invalid or missing sensor type" }), 400
    if not sensor_data:
        return jsonify({ "status": "failed", "message": "No sensor data provided" }), 400

    timestamp = datetime.now().strftime("%H:%M:%S")
    # TODO: use timestamp accordingly

    try:
        if sensor_type == "air_quality" and sensor_data > AQ_THRESHOLD:
                pass # TODO: implement air quality threshold exceeded message
        elif sensor_type == "magnetic" and sensor_data > MAGNETIC_THRESHOLD:
                pass # TODO: implement magnetic threshold exceeded message
        elif sensor_type == "ultrasonic" and sensor_data > US_THRESHOLD:
            pass # TODO: implement ultrasonic threshold exceeded message

        db.child("Bins").child(binId).child(sensor_type).set(sensor_data)
        return jsonify({ "status": "success", "message": "Data added to bin" }), 200

    except Exception as e:
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400
    
@app.route("/bin/fetch/bins", methods=["GET"])
def fetch_bins():
    uId = request.args.get('uId')
    
    if not uId:
        return jsonify({ "status": "failed", "message": "User ID not given" }), 400

    try:
        bins_exist = db.child("Users").child(uId).get().val()
        
        if not bins_exist:
            return jsonify({ "status": "failed", "message": f"Given user ID: {uId} does not own any bins" }), 400
        
        data_array = [value for value in bins_exist.values()]
        
        return jsonify({ "status": "success", "message": "Data fetched successfully", "data": data_array }), 200

    except Exception as e:
        print("Error fetching data from Firestore:", str(e))
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400