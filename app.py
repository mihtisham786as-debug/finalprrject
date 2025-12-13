import sqlite3
import pandas as pd
import os
import bcrypt

USERS_FILE = "users.txt"
DB_FILE = "intelligence_platform.db"

#  Database Manager
class DatabaseManager:
    def __init__(self, db_name=DB_FILE):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

#  Setup Tables 
def setup_tables():
    db = DatabaseManager()
    db.connect()

    # Drop old tables
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("DROP TABLE IF EXISTS cyber_incidents")
    db.execute("DROP TABLE IF EXISTS datasets_metadata")
    db.execute("DROP TABLE IF EXISTS it_tickets")

    # Create fresh tables
    db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """)
    db.execute("""
        CREATE TABLE cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT,
            severity TEXT,
            resolution_time INTEGER
        )
    """)
    db.execute("""
        CREATE TABLE datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT,
            size_mb REAL,
            rows_count INTEGER,
            source TEXT
        )
    """)
    db.execute("""
        CREATE TABLE it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_name TEXT,
            status TEXT,
            resolution_time INTEGER
        )
    """)
    db.close()
    print("✅ Tables created successfully")

# Migrate Users 
def migrate_users():
    if not os.path.exists(USERS_FILE):
        print("⚠ No users.txt found. Skipping migration.")
        return

    db = DatabaseManager()
    db.connect()
    with open(USERS_FILE, "r") as f:
        for line in f:
            username, pwd_hash, role = line.strip().split(",")
            db.execute(
                "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, pwd_hash, role)
            )
    db.close()
    print("✅ Users migrated from users.txt to SQLite")

# CRUD Tests 
def crud_cyber():
    db = DatabaseManager()
    db.connect()
    db.execute(
        "INSERT INTO cyber_incidents (incident_type, severity, resolution_time) VALUES (?, ?, ?)",
        ("Phishing", "High", 48)
    )
    print("Cyber Incidents:", db.fetchall("SELECT * FROM cyber_incidents"))
    db.execute("UPDATE cyber_incidents SET resolution_time=? WHERE id=?", (36, 1))
    db.execute("DELETE FROM cyber_incidents WHERE id=?", (1,))
    db.close()

def crud_data():
    db = DatabaseManager()
    db.connect()
    db.execute(
        "INSERT INTO datasets_metadata (dataset_name, size_mb, rows_count, source) VALUES (?, ?, ?, ?)",
        ("SalesData", 120.5, 500000, "Finance")
    )
    print("Datasets:", db.fetchall("SELECT * FROM datasets_metadata"))
    db.execute("UPDATE datasets_metadata SET size_mb=? WHERE id=?", (110.0, 1))
    db.execute("DELETE FROM datasets_metadata WHERE id=?", (1,))
    db.close()

def crud_it():
    db = DatabaseManager()
    db.connect()
    db.execute(
        "INSERT INTO it_tickets (staff_name, status, resolution_time) VALUES (?, ?, ?)",
        ("Ahmed", "Waiting for User", 72)
    )
    print("IT Tickets:", db.fetchall("SELECT * FROM it_tickets"))
    db.execute("UPDATE it_tickets SET status=? WHERE id=?", ("Resolved", 1))
    db.execute("DELETE FROM it_tickets WHERE id=?", (1,))
    db.close()

# Run Setup
if __name__ == "__main__":
    setup_tables()
    migrate_users()

    print("\n--- TESTING CRUD ---")
    crud_cyber()
    crud_data()
    crud_it()
