import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

sessions = [
    (1, '2026-06-01 10:00', '2026-06-01 10:15', 'Happy', 0.89, 0.92, 1),
    (1, '2026-06-02 11:00', '2026-06-02 11:20', 'Surprised', 0.85, 0.88, 2),
    (2, '2026-06-03 09:30', '2026-06-03 09:45', 'Sad', 0.75, 0.80, 3),
    (2, '2026-06-04 10:00', '2026-06-04 10:18', 'Happy', 0.90, 0.95, 1),
    (3, '2026-06-05 12:00', '2026-06-05 12:20', 'Neutral', 0.82, 0.84, 2),
    (3, '2026-06-06 01:00', '2026-06-06 01:15', 'Happy', 0.93, 0.96, 0),
    (4, '2026-06-07 02:00', '2026-06-07 02:25', 'Angry', 0.70, 0.75, 4),
    (4, '2026-06-08 03:00', '2026-06-08 03:20', 'Happy', 0.88, 0.91, 1),
    (5, '2026-06-09 04:00', '2026-06-09 04:15', 'Surprised', 0.92, 0.94, 0),
    (5, '2026-06-10 05:00', '2026-06-10 05:18', 'Happy', 0.95, 0.97, 0)
]

cursor.executemany("""
INSERT INTO sessions
(
    child_id,
    start_time,
    end_time,
    dominant_emotion,
    avg_confidence,
    engagement_rate,
    distraction_count
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", sessions)

conn.commit()
conn.close()

print("Sessions Added Successfully")