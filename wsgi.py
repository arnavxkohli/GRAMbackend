from api import app, ip

ip.push_public_ip()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)