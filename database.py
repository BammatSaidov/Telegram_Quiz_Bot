import sqlite3
from config import DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            user_id INTEGER PRIMARY KEY,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_result(user_id, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO quiz_results (user_id, score) VALUES (?, ?)", (user_id, score))
    conn.commit()
    conn.close()

def get_result(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM quiz_results WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
