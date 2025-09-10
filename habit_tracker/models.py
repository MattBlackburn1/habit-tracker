import sqlite3
from dataclasses import dataclass


@dataclass
class Habit:
    id: int | None
    name: str
    frequency: str
    created_at: str | None = None
    is_active: int = 1


def create_habit(conn, name, frequency):
    cur = conn.cursor()
    name = name.strip()
    if not name:
        raise ValueError("Habit name is required")

    frequency = frequency.lower()
    if frequency not in ("daily", "weekly"):
        raise ValueError("Frequency must be daily or weekly")

    cur.execute("INSERT INTO habits(name, frequency) VALUES(?, ?);", (name, frequency))
    habit_id = cur.lastrowid
    cur.execute(
        "SELECT id, name, frequency, created_at, is_active FROM habits WHERE id = ?;", (habit_id,)
    )
    row = cur.fetchone()
    return Habit(*row)


def list_habit(conn, include_inactive=False):
    cur = conn.cursor()
    items = []

    if include_inactive:
        sql = "SELECT id, name, frequency, created_at, is_active FROM habits ORDER BY id;"
    else:
        sql = (
            "SELECT id, name, frequency, created_at, is_active FROM habits "
            "WHERE is_active = 1 ORDER BY id;"
        )
        cur.execute(sql)

    row = cur.fetchall()
    items = [Habit(*r) for r in row]
    return items


def delete_habit(conn, habit_id):
    cur = conn.cursor()
    habit = int(habit_id)
    if habit <= 0:
        raise ValueError("Habit ID must be a positive integer")
    cur.execute("DELETE FROM habits WHERE id = ?;", (habit_id,))
    if cur.rowcount == 1:
        return True
    else:
        return False


def get_habit_by_name(conn: sqlite3.Connection, name: str) -> Habit | None:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, frequency, created_at, is_active FROM habits WHERE name = ?;",
        (name,),
    )
    row = cur.fetchone()
    return Habit(*row) if row else None
