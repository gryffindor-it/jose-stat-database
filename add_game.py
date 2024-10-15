import requests

user_id = 1 # Replace with desired user ID

url = f"http://127.0.0.1:8000/users/{user_id}/games/"
data = {
    "title": "",  # Replace with desired game title
    "playtime": 0,  # Replace with desired playtime
    "user_id": user_id  # Use the user ID returned from creating the user
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Game added successfully:", response.json())
else:
    print("Failed to add game:", response.json())
