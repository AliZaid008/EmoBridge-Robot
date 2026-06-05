import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    dominant_emotion TEXT,
    avg_confidence REAL,
    engagement_rate REAL,
    distraction_count INTEGER,

    FOREIGN KEY (child_id) REFERENCES children(child_id)
)
""")

conn.commit()
conn.close()

print("Sessions Table Created Successfully")