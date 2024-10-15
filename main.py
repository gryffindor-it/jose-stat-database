from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database Connection Dependency
def get_db():
    conn = sqlite3.connect('videogames.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Pydantic models
class Game(BaseModel):
    title: str
    playtime: int

class User(BaseModel):
    id: int = None # took me way to long to figure out how to make this optional
    username: str

# Initialize the database (you can call this once to create the schema)
# @app.lifespan()
# def startup():
@app.on_event("startup")
def startup():
    with sqlite3.connect("videogames.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            playtime INTEGER NOT NULL DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

# Add a new user
@app.post("/users/")
def create_user(user: User, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created successfully"}

# Add a game for a user
@app.post("/users/{user_id}/games/")
def add_game(user_id: int, game: Game, db: sqlite3.Connection = Depends(get_db)):
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.execute("INSERT INTO games (title, playtime, user_id) VALUES (?, ?, ?)", 
               (game.title, game.playtime, user_id))
    db.commit()
    return {"message": "Game added successfully"}

# Get all users
@app.get("/users/", response_model=list[User])
def get_users(db: sqlite3.Connection = Depends(get_db)):
    users = db.execute("SELECT * FROM users").fetchall()

    return [{"id": user[0], "username": user[1]} for user in users]

# Get specific user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    user = db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(id=user[0], username=user[1])

# Get all games for a specific user
@app.get("/users/{user_id}/games/")
def get_user_games(user_id: int, sort_by: str = None, db: sqlite3.Connection = Depends(get_db)):
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = "SELECT id, title, playtime FROM games WHERE user_id = ?"
    if sort_by == "title":
        query += " ORDER BY title"
    elif sort_by == "playtime":
        query += " ORDER BY playtime DESC"
    
    games = db.execute(query, (user_id,)).fetchall()
    return [{"id": game[0], "title": game[1], "playtime": game[2]} for game in games]

# Find common games between two users, and compare their playtimes
@app.get("/common-games/{user_id1}/{user_id2}")
def get_common_games(user_id1: int, user_id2: int, db: sqlite3.Connection = Depends(get_db)):
    # Check if both users exist
    user1 = db.execute("SELECT id FROM users WHERE id = ?", (user_id1,))
    user2 = db.execute("SELECT id FROM users WHERE id = ?", (user_id2,))

    if user1.fetchone() is None:
        raise HTTPException(status_code=404, detail="User 1 not found")
    
    if user2.fetchone() is None:
        raise HTTPException(status_code=404, detail="User 2 not found")

    # Query to find common games owned by both users by game title
    # I'm gonna be completely honest i have no idea how this query works, but it does
    query = """
    SELECT g.title, 
           MAX(CASE WHEN g.user_id = ? THEN g.playtime END) AS user1_playtime,
           MAX(CASE WHEN g.user_id = ? THEN g.playtime END) AS user2_playtime
    FROM games g
    WHERE g.user_id IN (?, ?)
    GROUP BY g.title
    HAVING user1_playtime IS NOT NULL AND user2_playtime IS NOT NULL
    """

    common_games = db.execute(query, (user_id1, user_id2, user_id1, user_id2)).fetchall()
    
    if not common_games:
        return {"message": "No common games found."}
    
    # Return the games along with both users playtime
    return [
        {
            "title": game[0],
            "user1_id": user_id1,
            "user1_playtime": game[1],
            "user2_id": user_id2,
            "user2_playtime": game[2],
        } for game in common_games
    ]


# Delete a game from a user
@app.delete("/users/{user_id}/games/{game_id}")
def delete_game(user_id: int, game_id: int, db: sqlite3.Connection = Depends(get_db)):
    # Check if the user exists
    cursor = db.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the game exists for the user
    cursor = db.execute("SELECT id FROM games WHERE id = ? AND user_id = ?", (game_id, user_id))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Game not found for this user")

    # Delete the game
    db.execute("DELETE FROM games WHERE id = ?", (game_id,))
    db.commit()  # Save changes to the database
    return {"message": "Game deleted successfully"}

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    # Check if the user exists
    cursor = db.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="User not found :(")

    # Delete all games for this user
    db.execute("DELETE FROM games WHERE user_id = ?", (user_id,))
    
    # Delete the user
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()  # Save changes to the database
    return {"message": "User and associated games deleted successfully :3"}