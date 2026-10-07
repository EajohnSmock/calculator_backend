import os
import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = (
    Path(__file__).resolve().parent.parent / 'calculator.db'
)


def get_db_path():
    configured_path = os.environ.get('CALCULATOR_DB_PATH')

    if configured_path:
        return Path(configured_path)

    return DEFAULT_DB_PATH


def get_connection():
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
                    DEFAULT (datetime('now', 'localtime'))
            )
            '''
        )
        connection.commit()


def insert_history(expression, result):
    with get_connection() as connection:
        cursor = connection.execute(
            '''
            INSERT INTO calculation_history (
                expression,
                result
            )
            VALUES (?, ?)
            ''',
            (expression, result)
        )
        history_id = cursor.lastrowid
        connection.commit()

        row = connection.execute(
            '''
            SELECT id, expression, result, created_at
            FROM calculation_history
            WHERE id = ?
            ''',
            (history_id,)
        ).fetchone()

    return dict(row)


def list_history():
    with get_connection() as connection:
        rows = connection.execute(
            '''
            SELECT id, expression, result, created_at
            FROM calculation_history
            ORDER BY id DESC
            '''
        ).fetchall()

    return [dict(row) for row in rows]


def delete_history(history_id):
    with get_connection() as connection:
        cursor = connection.execute(
            '''
            DELETE FROM calculation_history
            WHERE id = ?
            ''',
            (history_id,)
        )
        connection.commit()

    return cursor.rowcount > 0
