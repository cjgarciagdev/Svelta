import sqlite3
import os

DB_NAME = "inces.sqlite"

def get_connection():
    """Obtiene la conexión a la base de datos SQLite."""
    # Habilitar claves foráneas en SQLite
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = 1")
    conn.row_factory = sqlite3.Row # Para poder acceder a las columnas por nombre
    return conn

def init_db():
    """Crea las tablas de la base de datos si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabla de Usuarios (Admins y Formadores)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL, -- 'ADMIN' o 'FORMADOR'
            status TEXT NOT NULL -- 'PENDING', 'APPROVED', 'REJECTED'
        )
    """)

    # 2. Tabla de Perfiles (Cursos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1
        )
    """)

    # 3. Tabla Relacional (Formador -> Perfil)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS formador_perfil (
            formador_id INTEGER,
            perfil_id INTEGER,
            FOREIGN KEY(formador_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(perfil_id) REFERENCES perfiles(id) ON DELETE CASCADE,
            PRIMARY KEY (formador_id, perfil_id)
        )
    """)

    # 4. Tabla de Estudiantes (Datos exactos del Google Form)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            cedula TEXT NOT NULL,
            genero TEXT,
            edad INTEGER,
            nivel_academico TEXT,
            posee_discapacidad BOOLEAN,
            cual_discapacidad TEXT,
            telefono TEXT,
            correo TEXT,
            direccion TEXT,
            perfil_id INTEGER,
            estado_inscripcion TEXT DEFAULT 'CENSADO', -- 'CENSADO', 'INSCRITO', 'CULMINADO', 'RETIRADO'
            fecha_censo DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(perfil_id) REFERENCES perfiles(id) ON DELETE SET NULL,
            UNIQUE (cedula, perfil_id)
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Base de datos verificada/inicializada correctamente.")

def count_users():
    """Cuenta cuántos usuarios hay en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM users")
    result = cursor.fetchone()
    conn.close()
    return result["total"]

def create_user(full_name, email, password_hash, role, status):
    """Crea un nuevo usuario en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash, role, status) VALUES (?, ?, ?, ?, ?)",
            (full_name, email, password_hash, role, status)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Esto ocurre si el correo ya existe
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    """Busca un usuario por su correo."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    """Obtiene todos los usuarios de la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_status(user_id, new_status):
    """Actualiza el estado de un usuario (PENDING, APPROVED, REJECTED)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = ? WHERE id = ?", (new_status, user_id))
    conn.commit()
    conn.close()

def update_user_role(user_id, new_role):
    """Actualiza el rol de un usuario (ADMIN, FORMADOR)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()
