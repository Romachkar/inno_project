import sqlite3
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('edu_tutor.db', check_same_thread=False)
        self._init_db()

    def _init_db(self):
        try:
            with self.conn:
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        query_text TEXT,
                        response TEXT,
                        achievements TEXT,  # Новое поле для достижений
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        full_name TEXT,
                        is_blocked BOOLEAN DEFAULT 0,
                        block_reason TEXT,
                        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

                self.conn.commit()

        except sqlite3.Error as e:
            logger.error(f"Ошибка при инициализации БД: {str(e)}")
            self.conn.rollback()

    def log_query(self, user_id: int, query_text: str, response: str, achievements: str = "") -> bool:
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO queries (user_id, query_text, response, achievements, created_at)
                    VALUES (?, ?, ?, ?, datetime('now'))
                ''', (user_id, query_text, response, achievements))
                self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Ошибка сохранения запроса: {str(e)}")
            self.conn.rollback()
            return False

    def get_user_plans(self, user_id: int) -> List[Dict]:
        try:
            with self.conn:
                cursor = self.conn.execute('''
                    SELECT id, query_text, response, achievements,
                           strftime('%Y-%m-%d %H:%M', created_at) as formatted_date
                    FROM queries 
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))

                return [{
                    'id': row[0],
                    'query_text': row[1],
                    'response': row[2],
                    'achievements': row[3] or "",
                    'timestamp': row[4]
                } for row in cursor.fetchall()]

        except sqlite3.Error as e:
            logger.error(f"Ошибка получения истории: {str(e)}")
            return []

    def clear_user_history(self, user_id: int) -> bool:
        try:
            with self.conn:
                self.conn.execute('DELETE FROM queries WHERE user_id = ?', (user_id,))
                self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Ошибка очистки истории: {str(e)}")
            self.conn.rollback()
            return False


db = Database()