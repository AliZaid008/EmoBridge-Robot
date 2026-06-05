import sqlite3

conn = sqlite3.connect("emobridge.db")
cursor = conn.cursor()

name = input("Enter Child Name: ")

cursor.execute("""
SELECT *
FROM children
WHERE name = ?
""", (name,))

rows = cursor.fetchall()

for row in rows:
    print("===== Child Profile =====")
    print("ID:", row[0])
    print("Name:", row[1])
    print("Age:", row[2])
    print("Avatar:", row[3])
    print("Theme:", row[4])

conn.close()