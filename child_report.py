import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    c.name,
    c.age,
    s.dominant_emotion,
    g.score,
    g.success_rate,
    g.reaction_time,
    b.badge_name           
            

FROM children c

JOIN sessions s
ON c.child_id = s.child_id

JOIN game_results g
ON s.session_id = g.session_id
               
LEFT JOIN badges b
ON c.child_id = b.child_id                              
""")

rows = cursor.fetchall()

for row in rows:
    print("Name:", row[0])
    print("Age:", row[1])
    print("Emotion:", row[2])
    print("Score:", row[3])
    print("Success Rate:", row[4])
    print("Reaction Time:", row[5])
    print("Badge:", row[6])
    print("-------------------")

conn.close()