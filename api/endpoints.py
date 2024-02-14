from flask import request, jsonify, session
from api import app, auth, db, ip
from enum import Enum

sensors = Enum('sensors', ['magnetic', 'air_quality', 'ToF', 'battery_detected', 'fire_detected'])


def encode_email(email):
    return email.replace('.', ',').replace('@', '_')


@app.before_first_request
def initialize():
    ip.push_public_ip()


# main api route; return method and timestamp
@app.route("/", methods=["GET", "POST", "PUT"])
def root():
    return "GRAM server"


@app.route("/user/signup", methods=["POST"])
def signup():
    if ('user' in session):
        return jsonify({ "status": "success", "message": "User already signed up" }), 200
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
            db.child("Users").child(encode_email(email)).child("binCount").set(0)
            return jsonify({ "status": "success", "message": "Sign Up successful" }), 200
        else:
            return jsonify({ "status": "failed", "message": "An Error Occurred" }), 400


@app.route("/user/signin", methods=["POST"])
def signin():
    if ('user' in session):
        return jsonify({ "status": "success", "message": "User already signed in" }), 200
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


@app.route("/user/addbin", methods=["PUT"])
def add_bin():
    data = request.json
    if 'uId' not in data:
        return jsonify({ "status": "failed", "message": "User ID not given" }), 400
    if 'binName' not in data:
        return jsonify({ "status": "failed", "message": "Bin Name not given" }), 400

    uId, binName = encode_email(data.get("uId")), data.get("binName")

    try:
        binId = f'id{db.child("Users").child(uId).child("binCount").get().val() + 1}'
        db.child("Users").child(uId).child("Bins").child(binId).set(binName)
        db.child("Users").child(uId).child("binCount").set(int(binId[2:]))
        return jsonify({ "status": "success", "message": "Bin added to User" }), 200
    except Exception as e:
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400


@app.route("/user/getbins", methods=["GET"])
def get_bins():
    uId = encode_email(request.args.get('uId'))
    if not uId:
        return jsonify({ "status": "failed", "message": "User ID not given" }), 400

    try:
        # Get all bins associated with the given uId
        user_bins = db.child("Users").child(uId).child("Bins").get().val()

        if user_bins:
            # Construct a dictionary from the user_bins data
            bins_dict = {bin_id: bin_name for bin_id, bin_name in user_bins.items()}

            return jsonify({ "status": "success", "data": bins_dict }), 200
        else:
            return jsonify({ "status": "success", "message": "No bins associated with the user" }), 400

    except Exception as e:
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400


@app.route("/bin/fetch", methods=["GET"])
def fetch_sensors():
    uId = encode_email(request.args.get('uId'))
    binId = request.args.get('binId')
    sensor_type = request.args.get('sensor_type')

    if not uId:
        return jsonify({ "status": "failed", "message": "User ID not given" }), 400
    if not binId:
        return jsonify({ "status": "failed", "message": "Bin ID not given" }), 400
    if not sensor_type or sensor_type not in sensors.__members__:
        return jsonify({ "status": "failed", "message": "Invalid or missing sensor type" }), 400

    try:
        bin_exists = db.child("Users").child(uId).child("Bins").child(f"id{request.args.get('binId')}").get().val()
        if not bin_exists:
            return jsonify({ "status": "failed", "message": f"Given user ID: {uId} does not own bin {binId}" }), 400

        sensor_data = db.child("Bins").child(binId).child(sensor_type).get().val()
        if not sensor_data:
            return jsonify({ "status": "failed", "message": f"No data available for {sensor_type}" }), 400
        return jsonify({ "status": "success", "message": "Data fetched successfully", "data": sensor_data }), 200

    except Exception as e:
        print("Error fetching data from Firestore:", str(e))
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400


@app.route('/logout')
def logout():
    try:
        session.clear()
        return jsonify({ "status": "success", "message": "Sign Out successful" }), 200
    except Exception as e:
        return jsonify({ "status": "error", "type": type(e).__name__, "message": str(e)}), 400