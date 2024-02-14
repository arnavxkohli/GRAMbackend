from api import app, ip

if __name__ == "__main__":
    ip.push_public_ip()
    app.run(debug=True, host="0.0.0.0", port=8080)