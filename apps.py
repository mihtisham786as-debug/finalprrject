import sqlite3
from datetime import datetime
import pandas as pd

DB_FILE = "week8_users.db"

# ---------- Database Helpers ----------

def connect_db():
    return sqlite3.connect(DB_FILE)

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_date TEXT NOT NULL,
            is_active INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_sample_users():
    conn = connect_db()
    c = conn.cursor()
    sample_users = [
        ('alice', 'SecurePass123!', 'analytics', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1),
        ('bob', 'Password456', 'cyber', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1),
        ('charlie', 'MyPass789', 'admin', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO users (username, password, role, created_date, is_active) VALUES (?, ?, ?, ?, ?)",
        sample_users
    )
    conn.commit()
    conn.close()

def fetch_and_print_users():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    
    # Print table using pandas for nice formatting
    df = pd.DataFrame(users, columns=["ID", "Username", "Password", "Role", "Created Date", "Is Active"])
    print(df)

# ---------- Main ----------

if __name__ == "__main__":
    create_table()
    insert_sample_users()
    fetch_and_print_users()
