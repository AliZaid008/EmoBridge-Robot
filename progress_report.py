import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    c.name,
    s.dominant_emotion,
    g.score

FROM children c

JOIN sessions s
ON c.child_id = s.child_id

JOIN game_results g
ON s.session_id = g.session_id

WHERE c.child_id = 1
""")

rows = cursor.fetchall()

print("===== Progress Report =====")

for row in rows:
    print(
        "Name:", row[0],
        "| Emotion:", row[1],
        "| Score:", row[2]
    )

conn.close()