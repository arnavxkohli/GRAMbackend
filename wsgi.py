from api import app, ip

@app.before_first_request
def initialize():
    ip.push_public_ip()

if __name__ == "__main__":
    # Run the app in production mode
    app.run(debug=False, host="0.0.0.0", port=8080)
