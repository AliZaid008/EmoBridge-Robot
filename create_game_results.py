import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS game_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    score INTEGER,
    difficulty_level TEXT,
    total_attempts INTEGER,
    success_rate REAL,
    reaction_time REAL,

    FOREIGN KEY (session_id)
    REFERENCES sessions(session_id)
)
""")

conn.commit()
conn.close()

print("Game Results Table Created Successfully")