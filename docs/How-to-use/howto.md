**[/users/](http://localhost:8000/users/)**: shows all users (user IDs, usernames)
``` json
[
  {
    "id": ,
    "username": ""
  },
  {
    "id": ,
    "username": ""
  }
]
```
**[/users/{user_id}/](http://localhost:8000/users/1)**: one specific user by ID (user ID, username)
``` json
[
  {
    "id": ,
    "username": ""
  }
]
```
**[/users/{user_id}/games/](http://localhost:8000/users/1/games/)**: specific users games by ID (game ID, game title, playtime)
``` json
[
  {
    "id": ,
    "title": "",
    "playtime": 
  }
]
```
**[/common_games/{user_id_1}/{user_id_2}/](http://localhost:8000/common_games/1/2)**: compare games both users have, if there are no games in common "No common games found." (game title, user ID, playtime)
``` json
[
  {
    "title": "",
    "user1_id": ,
    "user1_playtime": ,
    "user2_id": ,
    "user2_playtime": 
  }
]
```
## sorting

**[?sort_by=playtime](http://localhost:8000/users/1/games/?sort_by=playtime)**: sorts games by playtime (descending)

**[?sort_by=title](http://localhost:8000/users/1/games/?sort_by=title)**: sorts games alphabetically (also by capilization)


## creating and deleting users and games

**add_user.py**: put in a username in the double quotes, you should get a response: <br>`"User created successfully:" or an error code`

**add_game.py**: specify by ID what user the game will be added to, specify title and playtime, you should get a response:<br> `"Game added successfully:" or an error code`

**remove_user.py**: specify user ID and run, you should get a response:<br> `"User deleted successfully:"` or `"Failed to delete user:"` (usually fails if user does not exist)

**remove_game.py**: specify user ID and game ID and run, you should get a response:<br> `"Game deleted successfully:"` or `"Failed to delete game:"` (usually fails is user/game does not exist)