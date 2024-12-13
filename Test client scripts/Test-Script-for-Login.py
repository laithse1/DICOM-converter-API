import requests

# Define the API URL for login
LOGIN_URL = "http://127.0.0.1:8000/login"

# Define login credentials
data = {
    "username": "admin",  # Replace with your valid username
    "password": "password"  # Replace with your valid password
}

# Send the POST request with credentials
response = requests.post(LOGIN_URL, data=data)

# Check the response
if response.status_code == 200:
    token = response.json().get("access_token")
    print("Login Successful!")
    print("JWT Token:", token)
else:
    print("Login Failed!")
    print("Status Code:", response.status_code)
    print("Error:", response.json())
