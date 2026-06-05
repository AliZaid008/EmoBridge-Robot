import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

children = [
    ('Ahmed', 8, 'Robot Friend', 'Blue'),
    ('Ali', 7, 'Space Hero', 'Green'),
    ('Maryam', 9, 'Princess', 'Pink'),
    ('Hassan', 6, 'Robot Friend', 'Blue'),
    ('Zainab', 8, 'Animal World', 'Yellow')
]

cursor.executemany("""
INSERT INTO children
(name, age, avatar, preferred_theme)
VALUES (?, ?, ?, ?)
""", children)

conn.commit()
conn.close()

print("Children Added Successfully")