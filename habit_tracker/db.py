from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ENV_VAR = "HABIT_DB_PATH"
DEFAULT_DB_NAME = "habit_tracker.db"
DEFAULT_DB = Path(os.environ.get(ENV_VAR, DEFAULT_DB_NAME)).resolve()


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS habits(
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL UNIQUE,
      frequency TEXT NOT NULL CHECK(frequency IN ('daily','weekly')),
      created_at TEXT NOT NULL DEFAULT (date('now')),
      is_active INTEGER NOT NULL DEFAULT 1
    );"""
    )
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS logs(
      id INTEGER PRIMARY KEY,
      habit_id INTEGER NOT NULL,
      done_date TEXT NOT NULL,
      UNIQUE(habit_id, done_date),
      FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
    );"""
    )
    conn.commit()


@contextmanager
def session(db_path: Path | str | None = None):
    conn = connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
