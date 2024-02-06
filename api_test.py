import requests

# Define the URL of your Flask server endpoint
signup_url = 'http://127.0.0.1:5000/user/signup'

# Define the JSON payload you want to send
data = {
    "email": "test4@example.com",
    "password": "123456"
}

# Send the POST request with JSON content
signup_response = requests.post(signup_url, json=data)

# Print the response from the server
print(signup_response.text)

# Define the URL of your Flask server endpoint
signin_url = 'http://127.0.0.1:5000/user/signin'

# Define the JSON payload you want to send
data = {
    "email": "test3@example.com",
    "password": "123456"
}

# Send the POST request with JSON content
signin_response = requests.post(signin_url, json=data)

# Print the response from the server
print(signin_response.text)
