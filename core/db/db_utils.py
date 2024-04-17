import sqlite3
from dataclasses import dataclass

# Декоратор упращает подключение к базе данных
def connect_to_db(db_file):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                return func(*args, **kwargs, cursor=cursor)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator

@dataclass
class UserDB:
    user_id: int
    chat_id: int
    username: str = None
    first_name: str = None
    last_name: str = None
    banned: bool = False

def convert_userdb(user: UserDB) -> tuple:
    return tuple(user.__dict__.values())

@connect_to_db('database.db')
def check_user(user_id: int, *, cursor: sqlite3.Cursor):
    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

@connect_to_db('database.db')
def write_user(user: UserDB, *, cursor: sqlite3.Cursor):
    cursor.execute("""
    INSERT INTO Users (user_id, chat_id, username, first_name, last_name, banned) 
    VALUES (?, ?, ?, ?, ?, ?)""", convert_userdb(user))

@connect_to_db('database.db')
def check_ban(user_id: int, *, cursor: sqlite3.Cursor):
    if check_user(user_id) == None:
        return False
    cursor.execute('SELECT banned FROM Users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()[0]

@connect_to_db('database.db')
def ban_user(user_id: int, *, cursor: sqlite3.Cursor):
    if check_user(user_id) == None:
        return False
    if not check_ban(user_id):
        cursor.execute('UPDATE Users SET banned = 1 WHERE user_id = ?', (user_id,))
        return True
    return False

@connect_to_db('database.db')
def unban_user(user_id: int, *, cursor: sqlite3.Cursor):
    if check_user(user_id) == None:
        return False
    if check_ban(user_id):
        cursor.execute('UPDATE Users SET banned = 0 WHERE user_id = ?', (user_id,))
        return True
    return False

@connect_to_db('database.db')
def delete_user(user_id: int, *, cursor: sqlite3.Cursor):
    if check_user(user_id) == None:
        return False
    cursor.execute("""DELETE FROM Users WHERE user_id = ?""", (user_id,))
    return True