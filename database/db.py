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
    # Se intenta migrar desde esquema antiguo (full_name) al nuevo (nombres, apellidos, cedula)
    try:
        cursor.execute("SELECT full_name FROM users LIMIT 1")
        cursor.execute("ALTER TABLE users RENAME COLUMN full_name TO nombres")
        cursor.execute("ALTER TABLE users ADD COLUMN apellidos TEXT DEFAULT ''")
        cursor.execute("ALTER TABLE users ADD COLUMN cedula TEXT DEFAULT ''")
        conn.commit()
    except Exception:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            cedula TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL, -- 'ADMIN' o 'FORMADOR'
            status TEXT NOT NULL, -- 'PENDING', 'APPROVED', 'REJECTED'
            was_formador INTEGER DEFAULT 0 -- 1 si fue ascendido de FORMADOR a ADMIN
        )
    """)
    # Migración segura: agregar columna si no existe (para bases de datos antiguas)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN was_formador INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass
    # Corregir registros existentes: todo ADMIN que no sea el principal (id=1) fue formador
    cursor.execute("UPDATE users SET was_formador = 1 WHERE role = 'ADMIN' AND id != 1 AND was_formador = 0")
    conn.commit()

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
            entidad TEXT DEFAULT '',
            FOREIGN KEY(formador_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(perfil_id) REFERENCES perfiles(id) ON DELETE CASCADE,
            PRIMARY KEY (formador_id, perfil_id, entidad)
        )
    """)
    
    # Migración de formador_perfil para añadir entidad a la PK
    try:
        # Check si la columna entidad ya existe
        cursor.execute("SELECT entidad FROM formador_perfil LIMIT 1")
    except Exception:
        try:
            # Recrear tabla para actualizar PRIMARY KEY
            cursor.execute("ALTER TABLE formador_perfil RENAME TO old_formador_perfil")
            cursor.execute("""
                CREATE TABLE formador_perfil (
                    formador_id INTEGER,
                    perfil_id INTEGER,
                    entidad TEXT DEFAULT '',
                    FOREIGN KEY(formador_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY(perfil_id) REFERENCES perfiles(id) ON DELETE CASCADE,
                    PRIMARY KEY (formador_id, perfil_id, entidad)
                )
            """)
            cursor.execute("INSERT INTO formador_perfil (formador_id, perfil_id) SELECT formador_id, perfil_id FROM old_formador_perfil")
            cursor.execute("DROP TABLE old_formador_perfil")
            conn.commit()
        except Exception as e:
            print(f"Error migrando formador_perfil: {e}")

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
            tipo_origen TEXT DEFAULT 'GENERAL', -- 'GENERAL' o 'AMBITO'
            entidad TEXT,
            FOREIGN KEY(perfil_id) REFERENCES perfiles(id) ON DELETE SET NULL,
            UNIQUE (cedula, perfil_id, entidad)
        )
    """)
    
    # Migración de tabla estudiantes para actualizar UNIQUE constraint
    try:
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='estudiantes'")
        sql = cursor.fetchone()[0]
        if "UNIQUE (cedula, perfil_id)" in sql and "entidad" not in sql.split("UNIQUE")[1]:
            cursor.execute("ALTER TABLE estudiantes RENAME TO old_estudiantes")
            cursor.execute("""
                CREATE TABLE estudiantes (
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
                    estado_inscripcion TEXT DEFAULT 'CENSADO',
                    fecha_censo DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tipo_origen TEXT DEFAULT 'GENERAL',
                    entidad TEXT,
                    FOREIGN KEY(perfil_id) REFERENCES perfiles(id) ON DELETE SET NULL,
                    UNIQUE (cedula, perfil_id, entidad)
                )
            """)
            cursor.execute("INSERT INTO estudiantes SELECT id, nombres, apellidos, cedula, genero, edad, nivel_academico, posee_discapacidad, cual_discapacidad, telefono, correo, direccion, perfil_id, estado_inscripcion, fecha_censo, tipo_origen, IFNULL(entidad, '') FROM old_estudiantes")
            cursor.execute("DROP TABLE old_estudiantes")
            conn.commit()
    except Exception as e:
        print(f"Error migrando tabla estudiantes: {e}")
    
    # Migración: agregar tipo_origen y entidad a bases de datos antiguas
    try:
        cursor.execute("ALTER TABLE estudiantes ADD COLUMN tipo_origen TEXT DEFAULT 'GENERAL'")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE estudiantes ADD COLUMN entidad TEXT")
    except Exception:
        pass

    conn.commit()
    conn.close()
    print("[OK] Base de datos verificada/inicializada correctamente.")

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
    cursor.execute("SELECT id, nombres, apellidos, cedula, email, role, status, was_formador FROM users ORDER BY id ASC")
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
    """Actualiza el rol de un usuario. Si sube a ADMIN marca was_formador=1."""
    conn = get_connection()
    cursor = conn.cursor()
    if new_role == "ADMIN":
        # Ascender: marcar que fue formador
        cursor.execute("UPDATE users SET role = ?, was_formador = 1 WHERE id = ?", (new_role, user_id))
    else:
        # Degradar: limpiar la marca
        cursor.execute("UPDATE users SET role = ?, was_formador = 0 WHERE id = ?", (new_role, user_id))
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
                direccion, perfil_id, fecha_censo, tipo_origen, entidad
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(cedula, perfil_id, entidad) DO UPDATE SET
                nombres=excluded.nombres,
                apellidos=excluded.apellidos,
                telefono=excluded.telefono,
                correo=excluded.correo,
                direccion=excluded.direccion,
                tipo_origen=excluded.tipo_origen,
                entidad=COALESCE(NULLIF(excluded.entidad, ''), estudiantes.entidad)
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
            datos.get('fecha_censo', None),
            datos.get('tipo_origen', 'GENERAL'),
            datos.get('entidad', '')
        ))
        conn.commit()
    except Exception as e:
        print(f"Error insertando estudiante: {e}")
    finally:
        conn.close()

def sync_google_forms(url, token, tipo_origen="GENERAL"):
    """Obtiene datos del Google Script y los sincroniza en la BD con su origen."""
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
                        elif "cedula" in k_lower or "cédula" in k_lower or ("identidad" in k_lower and "tipo" not in k_lower): mapped['cedula'] = value
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
                        elif "seleccione el nombre" in k_lower or ("nombre" in k_lower and ("postula" in k_lower or "postulante" in k_lower)): mapped['entidad'] = value
                    
                    if 'cedula' in mapped and mapped['cedula']:
                        mapped['tipo_origen'] = tipo_origen
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
        ORDER BY e.fecha_censo ASC
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

    # Top 5 Cursos con mayor demanda
    cursor.execute("""
        SELECT p.name, COUNT(e.id) as cantidad
        FROM perfiles p
        LEFT JOIN estudiantes e ON p.id = e.perfil_id
        GROUP BY p.id
        ORDER BY cantidad DESC
        LIMIT 5
    """)
    cursos_top = cursor.fetchall()

    # Por Trimestre (calculado en Python para evitar problemas de formato de fecha DD/MM/YYYY)
    cursor.execute("SELECT fecha_censo FROM estudiantes")
    fechas = cursor.fetchall()
    
    trim_counts = {"1er Trimestre": 0, "2do Trimestre": 0, "3er Trimestre": 0, "4to Trimestre": 0}
    for row in fechas:
        fecha_str = str(row['fecha_censo']) if row['fecha_censo'] else ""
        mes = 0
        if '/' in fecha_str:
            try: mes = int(fecha_str.split('/')[1])
            except: pass
        elif '-' in fecha_str:
            try: mes = int(fecha_str.split('-')[1].split(' ')[0])
            except: pass
            
        if 1 <= mes <= 3: trim_counts["1er Trimestre"] += 1
        elif 4 <= mes <= 6: trim_counts["2do Trimestre"] += 1
        elif 7 <= mes <= 9: trim_counts["3er Trimestre"] += 1
        elif 10 <= mes <= 12: trim_counts["4to Trimestre"] += 1

    trimestres = [(k, v) for k, v in trim_counts.items()]

    # Todos los Perfiles con su conteo total de estudiantes
    cursor.execute("""
        SELECT p.name, COUNT(e.id) as cantidad
        FROM perfiles p
        LEFT JOIN estudiantes e ON p.id = e.perfil_id
        GROUP BY p.id
        ORDER BY cantidad DESC
    """)
    perfiles_todos = cursor.fetchall()

    conn.close()
    return {
        "total": total,
        "generos": generos,
        "discapacidades": discapacidades,
        "cursos": cursos_top,
        "trimestres": trimestres,
        "perfiles_todos": perfiles_todos,
    }


    # ==========================================
# FUNCIONES DEL FLUJO DEL FORMADOR
# ==========================================

def get_entidades_disponibles():
    """Devuelve todos los valores únicos de 'entidad' que tienen los estudiantes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT entidad FROM estudiantes
        WHERE entidad IS NOT NULL AND entidad != ''
        ORDER BY entidad ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row["entidad"] for row in rows]

def assign_perfil_to_formador(formador_id, perfil_id, entidad=""):
    """Asigna un perfil/curso a un formador, opcionalmente filtrado por entidad."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO formador_perfil (formador_id, perfil_id, entidad) VALUES (?, ?, ?)", (formador_id, perfil_id, entidad))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Ya estaba asignado
    finally:
        conn.close()

def remove_perfil_from_formador(formador_id, perfil_id, entidad=""):
    """Quita un perfil/curso de un formador."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM formador_perfil WHERE formador_id = ? AND perfil_id = ? AND entidad = ?", (formador_id, perfil_id, entidad))
    conn.commit()
    conn.close()

def get_perfiles_by_formador(formador_id):
    """Obtiene los perfiles/cursos asignados a un formador."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, fp.entidad FROM perfiles p
        INNER JOIN formador_perfil fp ON p.id = fp.perfil_id
        WHERE fp.formador_id = ?
        ORDER BY p.name
    """, (formador_id,))
    perfiles = cursor.fetchall()
    conn.close()
    return perfiles

def get_estudiantes_by_formador(formador_id):
    """Obtiene los estudiantes de TODOS los cursos asignados al formador."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.*, p.name as perfil_name, fp.entidad as formador_entidad FROM estudiantes e
        INNER JOIN formador_perfil fp ON e.perfil_id = fp.perfil_id
        INNER JOIN perfiles p ON e.perfil_id = p.id
        WHERE fp.formador_id = ? AND IFNULL(e.entidad, '') = IFNULL(fp.entidad, '')
        ORDER BY p.name, e.apellidos
    """, (formador_id,))
    estudiantes = cursor.fetchall()
    conn.close()
    return estudiantes

def update_estado_inscripcion(estudiante_id, nuevo_estado):
    """Actualiza el estado de inscripción de un estudiante."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE estudiantes SET estado_inscripcion = ? WHERE id = ?", (nuevo_estado, estudiante_id))
    conn.commit()
    conn.close()

    
