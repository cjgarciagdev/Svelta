"""
Configuración Base - Plantilla Reutilizable
===========================================
Cambia los valores según tu proyecto.

Para usar esta plantilla:
1. Copia esta carpeta como tu nuevo proyecto
2. Edita los valores de configuración abajo
3. Ejecuta python app.py
"""

import os
from datetime import timedelta


# ==================== CONFIGURACIÓN DEL PROYECTO ====================
# =====================================================
# [ZONA 1] EDITAR NOMBRE Y DATOS BÁSICOS
# Cambia los valores de tu aplicación aquí
# =====================================================

# Nombre de tu aplicación
APP_NAME = "MiAppSalud"

# Versión
APP_VERSION = "1.0.0"

# Descripción
APP_DESCRIPTION = "Sistema de gestión de salud"

# URL de producción
PRODUCTION_URL = "https://miapp.ejemplo.com"


class Config:
    """Configuración base de la aplicación"""
    
    # =====================================================
    # [ZONA 2] CLAVES Y CONFIGURACIÓN GENERAL
    # Edita SECRET_KEY para producción
    # =====================================================
    
    # --- CLAVES SECRETAS ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'cambia-esta-clave-secreta-2024')
    
    # --- BASE DE DATOS ---
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- SESIÓN ---
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # --- LOGIN ---
    LOGIN_VIEW = 'auth.login'
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    
    # --- ROLES PERMITIDOS ---
    # =====================================================
    # [ZONA 3] EDITAR ROLES DE USUARIO
    # Define los roles de tu aplicación aquí
    # =====================================================
    # Edita según los roles de tu aplicación
    ALLOWED_ROLES = ['admin', 'especialista', 'usuario']
    DEFAULT_ROLE = 'usuario'
    
    @staticmethod
    def get_database_uri():
        """Obtiene la URI de la base de datos"""
        # =====================================================
        # [ZONA 4] CONFIGURACIÓN DE BASE DE DATOS
        # PostgreSQL: DATABASE_URL se configura en variables de entorno
        # SQLite: Se usa automáticamente si no hay DATABASE_URL
        # =====================================================
        db_uri = os.getenv('DATABASE_URL')
        
        if db_uri:
            db_uri = db_uri.strip().replace(' ', '')
            while '@@' in db_uri:
                db_uri = db_uri.replace('@@', '@')
            if db_uri.startswith('postgres://'):
                db_uri = db_uri.replace('postgres://', 'postgresql://', 1)
            return db_uri
        else:
            # Desarrollo local con SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            parent_dir = os.path.abspath(os.path.join(basedir, '..'))
            os.makedirs(os.path.join(parent_dir, 'instance'), exist_ok=True)
            return f"sqlite:///{os.path.join(parent_dir, 'instance', 'miapp.db')}"
    
    @staticmethod
    def get_engine_options():
        """Opciones del motor de base de datos"""
        # =====================================================
        # [ZONA 5] CONFIGURACIÓN AVANZADA DE DB
        # Pool settings, SSL, etc. para PostgreSQL
        # =====================================================
        db_uri = Config.get_database_uri()
        
        if not db_uri.startswith('postgresql'):
            return {}
        
        is_pooler = ':6543/' in db_uri
        
        engine_options = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {
                'connect_timeout': 10,
                'sslmode': 'require'
            },
        }
        
        if is_pooler:
            engine_options['query_cache_size'] = 0
        
        return engine_options
    
    @staticmethod
    def is_production():
        """Verifica si está en producción"""
        return os.getenv('FLASK_ENV') == 'production' or os.getenv('RENDER') == 'true'


class DevelopmentConfig(Config):
    """Desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Producción"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Mapeo de configuraciones
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtiene la configuración según el entorno"""
    # =====================================================
    # [ZONA 6] SELECCIÓN DE ENTORNO
    # Cambia FLASK_ENV a 'production' para desplegar
    # =====================================================
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
