from fastapi import FastAPI
import sqlite3

app = FastAPI()


@app.on_event("startup")
def setup_database():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
            INSERT INTO users (name, role)
            VALUES (?, ?)
        """, [
            ("Shweta", "Flutter Developer"),
            ("Rahul", "Backend Developer"),
            ("Aman", "AI Engineer"),
            ("Priya", "UI UX Designer")
        ])

    conn.commit()
    conn.close()


@app.get("/")
def home():
    return {"message": "Database API Running"}


@app.get("/users")
def get_users():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "role": row[2]
        })

    conn.close()

    return users