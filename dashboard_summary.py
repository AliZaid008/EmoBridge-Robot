import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM children")
children_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM sessions")
sessions_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM game_results")
results_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM badges")
badges_count = cursor.fetchone()[0]

cursor.execute("""
SELECT dominant_emotion
FROM sessions
GROUP BY dominant_emotion
ORDER BY COUNT(*) DESC
LIMIT 1
""")

emotion = cursor.fetchone()[0]

print("===== EmoBridge Dashboard =====")
print(f"Total Children: {children_count}")
print(f"Total Sessions: {sessions_count}")
print(f"Total Game Results: {results_count}")
print(f"Total Badges: {badges_count}")
print(f"Most Common Emotion: {emotion}")
print("System Status: Active ✅")

conn.close()