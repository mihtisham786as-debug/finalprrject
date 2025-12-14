import sqlite3
import pandas as pd
import os



class DatabaseManager:
    def __init__(self, db_name='platform.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.load_csv_data()

    def load_csv_data(self):
        # Cyber incidents
        df = pd.read_csv("data/cyber_insidents.csv")
        df = df[["category","severity","status","resolution_time_hours","reported_date"]]
        df.rename(columns={"resolution_time_hours":"resolution_time"}, inplace=True)
        df.to_sql("cyber_incidents", self.conn, if_exists="append", index=False)


        # Datasets
        df = pd.read_csv("data/datasets.csv")
        df = df[["name","size_mb","rows","source","created_date"]]
        df.to_sql("datasets", self.conn, if_exists="append", index=False)


        # IT tickets
        df = pd.read_csv("data/it_tickets.csv")
        df = df[["staff","status","resolution_time_hours","created_date"]]
        df.rename(columns={"resolution_time_hours":"resolution_time"}, inplace=True)
        df.to_sql("it_tickets", self.conn, if_exists="append", index=False)


        self.conn.commit()

    

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
        )''')


        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        severity TEXT,
        status TEXT,
        resolution_time INTEGER,
        reported_date TEXT
    )
""")



        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    size_mb INTEGER,
    rows INTEGER,
    source TEXT,
    created_date TEXT
)
""")



        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS it_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff TEXT,
    status TEXT,
    resolution_time INTEGER,
    created_date TEXT
)
""")

        self.conn.commit()


    def fetch_all(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()