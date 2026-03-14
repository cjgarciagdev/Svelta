-- =============================================
-- BASE DE DATOS SUPABASE - PLANTILLA FLASK
-- =============================================
-- Ejecuta este script en el SQL Editor de Supabase

-- 1. TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    rol VARCHAR(20) DEFAULT 'usuario',
    nombre_completo VARCHAR(120),
    email VARCHAR(120),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT NOW(),
    ultimo_acceso TIMESTAMP,
    cambio_password_requerido BOOLEAN DEFAULT FALSE
);

-- 2. TABLA DE CONFIGURACIÓN
CREATE TABLE IF NOT EXISTS configuracion (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(50) UNIQUE NOT NULL,
    valor TEXT,
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- 3. TABLA DE REGISTROS (ejemplo genérico)
CREATE TABLE IF NOT EXISTS registro (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuario(id),
    fecha TIMESTAMP DEFAULT NOW(),
    datos TEXT,
    notas TEXT
);

-- =============================================
-- DATOS INICIALES
-- =============================================

-- Insertar usuario admin por defecto
INSERT INTO usuario (username, password_hash, rol, nombre_completo, email)
VALUES (
    'admin',
    'scrypt:32768:8:1$MzZ5ZnN0YWNr$ ejemplo_hash_aqui',  -- Cambia esta contraseña
    'admin',
    'Administrador',
    'admin@ejemplo.com'
)
ON CONFLICT (username) DO NOTHING;

-- Insertar configuración por defecto
INSERT INTO configuracion (clave, valor) VALUES
    ('app_nombre', 'MiApp'),
    ('app_version', '1.0.0'),
    ('app_url', 'https://miapp.ejemplo.com')
ON CONFLICT (clave) DO NOTHING;

-- =============================================
-- NOTA IMPORTANTE
-- =============================================
-- Para usar con Flask, usa la Connection Pooler URL:
-- postgresql://postgres:[TU_PASSWORD]@aws-0-xxx.pooler.supabase.com:6543/postgres
--
-- NO uses la URL directa del puerto 5432
-- =============================================
