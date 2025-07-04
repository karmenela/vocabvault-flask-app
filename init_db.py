import sqlite3

conn = sqlite3.connect("vocabvault.db")
db = conn.cursor()

db.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Database and users table created successfully.")
