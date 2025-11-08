# #Handles database setup, connection, insertion, and fetching.
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

def connect_db(create_db_if_missing = False):
    if create_db_if_missing:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
    else:
        conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def ensure_database():
    conn = connect_db(create_db_if_missing=True)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    conn.commit()
    cur.close()
    conn.close()

def create_table():
    ensure_database()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(225),
            content LONGTEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Database and table ready.")

def insert_document(title,content):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO documents (title, content) VALUES (%s, %s)",(title, content))
    conn.commit()
    conn.close()

def fetch_all_texts():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM documents")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
