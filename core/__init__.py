"""
Core Module - Extensiones Base
==============================
Contiene las extensiones fundamentales de Flask.

Para agregar más extensiones:
1. Importa la extensión aquí
2. Inicialízala en init_extensions()
"""

from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager  # [LOGIN] Descomenta para activar login
from flask import Flask

# =====================================================
# [ZONA 1] INSTANCIAS DE EXTENSIONES
# Agrega nuevas extensiones aquí
# Ejemplo: from flask_mail import Mail
#          mail = Mail()
# =====================================================

# Instancias globales - NO EDITAR
db = SQLAlchemy()
# login_manager = LoginManager()  # [LOGIN] Descomenta para activar login

# Configuración por defecto
# login_manager.login_view = 'auth.login'  # [LOGIN] Descomenta para activar login


def init_extensions(app: Flask):
    """Inicializa las extensiones con la app"""
    # =====================================================
    # [ZONA 2] INICIALIZAR EXTENSIONES
    # Agrega más extensiones aquí:
    # mail.init_app(app)
    # bcrypt.init_app(app)
    # =====================================================
    
    db.init_app(app)
    # login_manager.init_app(app)  # [LOGIN] Descomenta para activar login
    
    # [LOGIN] Configurar sesión (Descomenta para activar login):
    # from config import Config
    # app.config['PERMANENT_SESSION_LIFETIME'] = Config.PERMANENT_SESSION_LIFETIME
    # app.config['SESSION_COOKIE_SECURE'] = Config.is_production()
    # app.config['SESSION_COOKIE_HTTPONLY'] = True
    # app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    # login_manager.remember_cookie_duration = Config.REMEMBER_COOKIE_DURATION


def init_db(app: Flask):
    """Inicializa la base de datos"""
    with app.app_context():
        db.create_all()
        # =====================================================
        # [ZONA 3] CREAR TABLAS ADICIONALES
        # Si necesitas crear tablas específicas:
        # from models import TuModelo
        # db.create_all()
        # =====================================================
