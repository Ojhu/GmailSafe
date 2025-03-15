import sqlite3
import os

WEB_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(WEB_ROOT, 'details.db')

def create_table():
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                password TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        ''')
    conn.close()

def insert_user(user_details):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute('''
            INSERT INTO users (full_name, username, email, phone_number, password, gender)
            VALUES (:Full_Name, :Username, :Email, :Phone_Number, :Password, :Gender)
        ''', user_details)
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def check_password(stored_password, provided_password):
    """Check if the provided password matches the stored password."""
    return stored_password == provided_password
