import sqlite3

conn = sqlite3.connect("emobridge.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS children (
    child_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    avatar TEXT,
    preferred_theme TEXT
)
""")

conn.commit()

conn.close()

print("Children Table Created Successfully")