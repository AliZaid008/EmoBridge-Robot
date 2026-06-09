import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

# Average Score
cursor.execute("""
SELECT AVG(score)
FROM game_results
""")

avg_score = cursor.fetchone()[0]

# Average Reaction Time
cursor.execute("""
SELECT AVG(reaction_time)
FROM game_results
""")

avg_reaction = cursor.fetchone()[0]

# Most Common Emotion
cursor.execute("""
SELECT dominant_emotion,
COUNT(*)

FROM sessions

GROUP BY dominant_emotion

ORDER BY COUNT(*) DESC

LIMIT 1
""")

emotion = cursor.fetchone()[0]

print("===== Smart Child Report =====")
print(f"Average Score: {avg_score:.2f}")
print(f"Average Reaction Time: {avg_reaction:.2f} sec")
print(f"Most Common Emotion: {emotion}")

if avg_score >= 80:
    print("Progress Level: Excellent ⭐")
elif avg_score >= 60:
    print("Progress Level: Good 👍")
else:
    print("Progress Level: Needs Support 🌱")

conn.close()