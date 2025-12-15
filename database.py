# database.py
import sqlite3
import os

DB_FILE = "homework.db"

# -------------------------------------------------------------
# Initialize database + table
# -------------------------------------------------------------
def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            checked INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# -------------------------------------------------------------
# Add a homework item
# -------------------------------------------------------------
def add_homework(task, checked=False):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO homework (task, checked) VALUES (?, ?)",
        (task, int(checked))
    )
    conn.commit()
    conn.close()


# -------------------------------------------------------------
# Delete an item by ID
# -------------------------------------------------------------
def delete_homework(hw_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM homework WHERE id=?", (hw_id,))
    conn.commit()
    conn.close()


# -------------------------------------------------------------
# Update homework (checked/unchecked)
# -------------------------------------------------------------
def update_status(hw_id, checked):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "UPDATE homework SET checked=? WHERE id=?",
        (int(checked), hw_id)
    )
    conn.commit()
    conn.close()


# -------------------------------------------------------------
# Get all homework items
# ---------
