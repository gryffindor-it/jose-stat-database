import requests

url = "http://127.0.0.1:8000/users/"

data = {
    "username": ""  # Replace with desired username
}

# Make the POST request
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # If the request was successful
    print("User created successfully:", response.json())
else:
    # If there was an error
    print(f"Failed to create user. Status code: {response.status_code}")
    print("Response:", response.json())

