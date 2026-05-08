import sqlite3
import os
import json
import urllib.request
from urllib.error import URLError

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

def create_user(nombres, apellidos, cedula, email, password_hash, role, status):
    """Crea un nuevo usuario en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (nombres, apellidos, cedula, email, password_hash, role, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nombres, apellidos, cedula, email, password_hash, role, status)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # El correo o cédula ya existe
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
    cursor.execute("SELECT id, nombres, apellidos, cedula, email, role, status FROM users ORDER BY id ASC")
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

def delete_user(user_id):
    """Elimina permanentemente un usuario de la base de datos."""
    # Proteger al admin principal
    if user_id == 1:
        return False
        
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        conn.close()

def create_perfil(name):
    """Crea un nuevo perfil (curso) en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO perfiles (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_perfiles():
    """Obtiene todos los perfiles registrados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perfiles ORDER BY id DESC")
    perfiles = cursor.fetchall()
    conn.close()
    return perfiles

def toggle_perfil_status(perfil_id, is_active):
    """Activa o desactiva un perfil."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE perfiles SET is_active = ? WHERE id = ?", (is_active, perfil_id))
    conn.commit()
    conn.close()

def get_perfil_id_by_name(name):
    """Busca el ID de un perfil por su nombre."""
    if not name: return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM perfiles WHERE name LIKE ?", (f"%{name}%",))
    row = cursor.fetchone()
    conn.close()
    return row['id'] if row else None

def insert_or_update_estudiante(datos):
    """Inserta o actualiza un estudiante validando por cédula y perfil_id."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Obtener perfil_id basado en el nombre del curso
    perfil_nombre = datos.get('perfil_nombre', '')
    perfil_id = get_perfil_id_by_name(perfil_nombre)
    
    if not perfil_id and perfil_nombre:
        # Si no existe el perfil pero nos llegó un nombre válido, lo creamos
        try:
            cursor.execute("INSERT INTO perfiles (name) VALUES (?)", (perfil_nombre,))
            perfil_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            perfil_id = get_perfil_id_by_name(perfil_nombre)
        
    try:
        # Intentamos insertar. Si hay conflicto de cédula y perfil_id, se actualizan los datos
        cursor.execute("""
            INSERT INTO estudiantes (
                nombres, apellidos, cedula, genero, edad, nivel_academico,
                posee_discapacidad, cual_discapacidad, telefono, correo, 
                direccion, perfil_id, fecha_censo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(cedula, perfil_id) DO UPDATE SET
                nombres=excluded.nombres,
                apellidos=excluded.apellidos,
                telefono=excluded.telefono,
                correo=excluded.correo,
                direccion=excluded.direccion
        """, (
            datos.get('nombres', ''),
            datos.get('apellidos', ''),
            str(datos.get('cedula', '')).strip(),
            datos.get('genero', ''),
            datos.get('edad', None),
            datos.get('nivel_academico', ''),
            1 if str(datos.get('posee_discapacidad', '')).lower() in ['sí', 'si', 'yes', 'true'] else 0,
            datos.get('cual_discapacidad', ''),
            str(datos.get('telefono', '')),
            datos.get('correo', ''),
            datos.get('direccion', ''),
            perfil_id,
            datos.get('fecha_censo', None)
        ))
        conn.commit()
    except Exception as e:
        print(f"Error insertando estudiante: {e}")
    finally:
        conn.close()

def sync_google_forms(url, token):
    """Obtiene datos del Google Script y los sincroniza en la BD."""
    full_url = f"{url}?token={token}"
    try:
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                if type(data) is dict and "error" in data:
                    print(f"Error de API: {data['error']}")
                    return False
                
                # Procesar cada fila
                for row in data:
                    mapped = {}
                    for key, value in row.items():
                        # Si la celda está vacía en Google Sheets, la ignoramos para que no sobreescriba una válida
                        if str(value).strip() == "":
                            continue
                            
                        k_lower = str(key).lower()
                        if "nombres" in k_lower: mapped['nombres'] = value
                        elif "apellidos" in k_lower: mapped['apellidos'] = value
                        elif "cedula" in k_lower or "cédula" in k_lower or "identidad" in k_lower: mapped['cedula'] = value
                        elif "genero" in k_lower or "género" in k_lower: mapped['genero'] = value
                        elif "edad" in k_lower: 
                            try: mapped['edad'] = int(value)
                            except: mapped['edad'] = 0
                        elif "nivel acad" in k_lower: mapped['nivel_academico'] = value
                        elif "posee alguna discap" in k_lower: mapped['posee_discapacidad'] = value
                        elif "indique cu" in k_lower: mapped['cual_discapacidad'] = value
                        elif "teléfono" in k_lower or "telefono" in k_lower: mapped['telefono'] = value
                        elif "correo" in k_lower: mapped['correo'] = value
                        elif "dirección" in k_lower or "direccion" in k_lower: mapped['direccion'] = value
                        elif "p.p.l" in k_lower or "perfil" in k_lower or "opcion de" in k_lower: mapped['perfil_nombre'] = value
                        elif "marca temporal" in k_lower: mapped['fecha_censo'] = value
                    
                    if 'cedula' in mapped and mapped['cedula']:
                        insert_or_update_estudiante(mapped)
                return True
            return False
    except URLError as e:
        print(f"Error de red al sincronizar: {e}")
        return False
    except Exception as e:
        print(f"Error general en sincronización: {e}")
        return False

def get_all_estudiantes():
    """Obtiene todos los estudiantes con sus respectivos perfiles."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.*, p.name as perfil_nombre 
        FROM estudiantes e
        LEFT JOIN perfiles p ON e.perfil_id = p.id
        ORDER BY e.fecha_censo DESC
    """)
    estudiantes = cursor.fetchall()
    conn.close()
    return estudiantes

def get_stats():
    """Obtiene estadísticas básicas para el dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total estudiantes
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    total = cursor.fetchone()[0]
    
    # Por Género
    cursor.execute("SELECT genero, COUNT(*) FROM estudiantes GROUP BY genero")
    generos = cursor.fetchall()
    
    # Por Discapacidad
    cursor.execute("SELECT posee_discapacidad, COUNT(*) FROM estudiantes GROUP BY posee_discapacidad")
    discapacidades = cursor.fetchall()

     # NUEVO: Top 5 Cursos con mayor demanda
    cursor.execute("""
        SELECT p.name, COUNT(e.id) as cantidad
        FROM perfiles p
        LEFT JOIN estudiantes e ON p.id = e.perfil_id
        GROUP BY p.id
        ORDER BY cantidad DESC
        LIMIT 5
    """)
    cursos_top = cursor.fetchall()
    
    conn.close()
    # Actualiza el return para incluir "cursos"
    return {"total": total, "generos": generos, "discapacidades": discapacidades, "cursos": cursos_top}
    
