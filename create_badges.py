import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS badges (
    badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER,
    badge_name TEXT,
    earned_date TEXT,

    FOREIGN KEY (child_id)
    REFERENCES children(child_id)
)
""")

conn.commit()
conn.close()

print("Badges Table Created Successfully")