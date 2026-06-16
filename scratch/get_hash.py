import sqlite3
conn = sqlite3.connect("inces.sqlite")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT password_hash FROM users WHERE email='gabo@gmail.com'")
print(cursor.fetchone()[0])
conn.close()
