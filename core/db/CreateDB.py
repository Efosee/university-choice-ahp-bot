import sqlite3

with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER,
    chat_id INTEGER,
    username NVARCHAR(30),
    first_name TEXT DEFAULT NULL,
    last_name TEXT DEFAULT NULL,
    banned BOOLEAN DEFAULT 0,
    UNIQUE (user_id, chat_id))""")
