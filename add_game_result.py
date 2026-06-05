import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

game_results = [
    (1, 85, 'Medium', 10, 80.0, 2.4),
    (2, 92, 'Hard', 12, 91.0, 1.8),
    (3, 78, 'Easy', 8, 75.0, 2.9),
    (4, 95, 'Hard', 15, 96.0, 1.5),
    (5, 88, 'Medium', 11, 84.0, 2.1),
    (6, 72, 'Easy', 7, 70.0, 3.2),
    (7, 90, 'Hard', 13, 89.0, 1.9),
    (8, 83, 'Medium', 9, 82.0, 2.5),
    (9, 97, 'Hard', 16, 98.0, 1.3),
    (10, 86, 'Medium', 10, 85.0, 2.2)
]

cursor.executemany("""
INSERT INTO game_results
(
    session_id,
    score,
    difficulty_level,
    total_attempts,
    success_rate,
    reaction_time
)
VALUES (?, ?, ?, ?, ?, ?)
""", game_results)

conn.commit()
conn.close()

print("Game Results Added Successfully")