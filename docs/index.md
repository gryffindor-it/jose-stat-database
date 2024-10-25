# What's this?

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## SQLite database with FastAPI

This is a database i created to store game stats, to be used with the friend finder chat app.

I used SQLite for the databse, and Fastapi for the api.

The idea behind this was to integrate it with friend finder, to display game stats on user profiles.
A big reason for this was to be able to find friends based on what game you had in common, let's say you want to find someone who likes to play minecraft, you would be able to search for other people who play minecraft and add them as a friend.

## What can we do with it?

The database stores a username and an id for each user.
It also stores games and gives them a unique id, and each game has playtime in hours.

Every user has their own games and their own playtime in each game.

My api lets you:

- Get information on all users
- Get information about a specific user
- Get information about a specific users' games
- compare the games of 2 specific users and their playtimes
    - Sort by playtime
    - Sort alphabetically by title
- Add new users
- Add new games to specific users
- Delete users
- Delete specific games from specific users
- Delete all games from a specific user

## What does it not do?

Something i wanted to do but sadly couldn't figure out was integration with steamapi.<br>
Instead of having to manually add your own games and your playtime, the code could just simply fetch everything from steam.<br>
I still wanted you to be able to add your own games, in case of games that arent on steam.

## Plans for the future

If we end up expanding on this project I'd really like to add integration with steamapi.

