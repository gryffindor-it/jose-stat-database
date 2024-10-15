import requests

user_id = 1  # Replace with the actual user ID you want to delete
url = f"http://127.0.0.1:8000/users/{user_id}"
response = requests.delete(url)

if response.status_code == 200:
    print("User deleted successfully:", response.json())
else:
    print("Failed to delete user:", response.json())