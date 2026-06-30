import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    query TEXT NOT NULL,
    results_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""


def get_db_connection():
    os.makedirs(BASE_DIR, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.executescript(SCHEMA_SQL)
        connection.commit()


def create_user(username: str, password: str) -> bool:
    username = username.strip().lower()
    password_hash = generate_password_hash(password)

    with get_db_connection() as connection:
        try:
            connection.execute(
                "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                (username, password_hash, datetime.utcnow().isoformat()),
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_user_by_username(username: str):
    username = username.strip().lower()
    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None


def verify_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return None

    if check_password_hash(user["password"], password):
        return user
    return None


def save_search_history(user_id: int, query: str, results: list):
    results_json = json.dumps(results, ensure_ascii=False)
    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO history (user_id, query, results_json, created_at) VALUES (?, ?, ?, ?)",
            (user_id, query.strip(), results_json, datetime.utcnow().isoformat()),
        )
        connection.commit()


def get_history(user_id: int) -> list:
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT id, query, results_json, created_at FROM history WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()

        history = []
        for row in rows:
            history.append(
                {
                    "id": row["id"],
                    "query": row["query"],
                    "results": json.loads(row["results_json"]),
                    "created_at": row["created_at"],
                }
            )
        return history
