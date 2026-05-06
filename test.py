import sqlite3
import json

conn = sqlite3.connect('inces.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT id, cedula, perfil_id, nombres, apellidos FROM estudiantes")
estudiantes = [dict(row) for row in cursor.fetchall()]

cursor.execute("SELECT * FROM perfiles")
perfiles = [dict(row) for row in cursor.fetchall()]

print("--- Estudiantes ---")
print(json.dumps(estudiantes, indent=2))
print("--- Perfiles ---")
print(json.dumps(perfiles, indent=2))

conn.close()
