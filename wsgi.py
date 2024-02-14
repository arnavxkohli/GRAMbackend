from api import app


if __name__ == "__main__":
    # Run the app in production mode
    app.run(debug=False, host="0.0.0.0", port=8080)
