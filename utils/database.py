import sqlite3
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


def __init__(self):
    self.conn = sqlite3.connect('university.db', check_same_thread=False)
    self._init_db()

def _init_db(self):
    with self.conn:
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query_text TEXT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')

def log_query(self, user_id: int, query_text: str, response: str) -> bool:
    try:
        self.conn.execute('''
            INSERT INTO queries (user_id, query_text, response)
            VALUES (?, ?, ?)
        ''', (user_id, query_text, response))
        self.conn.commit()
        return True
    except Exception as e:
        print(f"DB Error: {str(e)}")
        return False