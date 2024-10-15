import requests

user_id = 1  # Replace with the actual user ID
game_id = 1  # Replace with the actual game ID you want to delete
url = f"http://127.0.0.1:8000/users/{user_id}/games/{game_id}"
response = requests.delete(url)

if response.status_code == 200:
    print("Game deleted successfully:", response.json())
else:
    print("Failed to delete game:", response.json())