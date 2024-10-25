### This is my first time making an actual readme so bear with me

everything to need to run this is in requirements.txt

```python pip install-r requirements.txt```

#### to start server
```uvicorn main:app --reload``` in terminal

server is by default at http://127.0.0.1:8000


#### Fastapi

**/users/**: shows all users (user IDs, usernames)
**/users/{user_id}/**: one specific user by ID (user ID, username)
**/users/{user_id}/games/**: specific users games by ID (game ID, game title, playtime)
**/common_games/{user_id_1}/{user_id_2}/**: compare games both users have, if there are no games in common "No common games found." (game title, user ID, playtime)

#### sorting
**?sort_by=playtime**: sorts games by playtime (descending)
**?sort_by=title**: sorts games alphabetically (also by capilization)


creating and deleting users and games

**add_user.py**: simply pick a username and run, you should get a response: "User created successfully:" or an error code
**add_game.py**: specify by ID what user the game will be added to, specify title and playtime, you should get a response: "Game added successfully:" or an error code
**remove_user.py**: specify user ID and run, you should get a response: "User deleted successfully:" or "Failed to delete user:" (usually fails if user does not exist)
**remove_game.py**: specify user ID and game ID and run, you should get a response: "Game deleted successfully:" or "Failed to delete game:" (usually fails is user/game does not exist)

