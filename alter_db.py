import sqlite3
import sys

try:
    conn = sqlite3.connect('inces.sqlite')
    cursor = conn.cursor()

    # Rename full_name to nombres
    cursor.execute('ALTER TABLE users RENAME COLUMN full_name TO nombres')
    
    # Add apellidos
    cursor.execute('ALTER TABLE users ADD COLUMN apellidos TEXT DEFAULT ""')
    
    # Add cedula
    cursor.execute('ALTER TABLE users ADD COLUMN cedula TEXT DEFAULT ""')
    
    # Update existing cedulas to random numbers so UNIQUE constraint won't fail if there are multiple users
    cursor.execute("UPDATE users SET cedula = id || '0000'")

    # Now create unique index on cedula
    cursor.execute('CREATE UNIQUE INDEX idx_users_cedula ON users(cedula)')
    
    conn.commit()
    print("Database updated successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
