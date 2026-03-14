"""
Core Module - Extensiones Base
==============================
Contiene las extensiones fundamentales de Flask.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask

# Instancias globales
db = SQLAlchemy()
login_manager = LoginManager()

# Configuración por defecto
login_manager.login_view = 'auth.login'


def init_extensions(app: Flask):
    """Inicializa las extensiones con la app"""
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configurar sesión
    from config import Config
    app.config['PERMANENT_SESSION_LIFETIME'] = Config.PERMANENT_SESSION_LIFETIME
    app.config['SESSION_COOKIE_SECURE'] = Config.is_production()
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    login_manager.remember_cookie_duration = Config.REMEMBER_COOKIE_DURATION


def init_db(app: Flask):
    """Inicializa la base de datos"""
    with app.app_context():
        db.create_all()
