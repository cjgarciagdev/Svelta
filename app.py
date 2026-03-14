"""
App Factory - Plantilla Reutilizable
===================================
Copia este archivo como base para tu proyecto.

Para usar:
1. Copia como app.py de tu proyecto
2. Edita los nombres de Blueprint
3. Agrega tus propias rutas
"""

import os
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_login import current_user, login_required

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Importar configuración
from config import get_config, Config
from core import db, login_manager, init_extensions, init_db
from models import Usuario


def create_app():
    """Factory de la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    config = get_config()
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config.get_engine_options()
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Configurar user loader
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    # =====================================================
    # [ZONA 1] AGREGAR BLUEPRINTS AQUÍ
    # Importa y registra tus nuevos blueprints en register_blueprints()
    # =====================================================
    register_blueprints(app)
    
    # Inyectar contexto global
    # =====================================================
    # [ZONA 2] AGREGAR VARIABLES GLOBALES A TEMPLATES AQUÍ
    # Edita inject_context() para agregar más variables globales
    # =====================================================
    inject_context(app)

    # ==================== RUTAS PRINCIPALES ====================
    # =====================================================
    # [ZONA 3] AGREGAR RUTAS PRINCIPALES AQUÍ
    # Agrega tus @app.route() debajo de esta línea
    # Ejemplo:
    # @app.route('/mi-ruta')
    # def mi_ruta():
    #     return render_template('mi_template.html')
    # =====================================================
    
    @app.route('/')
    def index():
        """Página principal - redirige según autenticación"""
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return render_template('index.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Panel principal después del login"""
        return render_template('dashboard.html')
    
    @app.route('/api/saludo')
    def api_saludo():
        """Ejemplo de API"""
        return jsonify({
            'mensaje': 'Hola desde la API',
            'app': Config.APP_NAME,
            'version': Config.APP_VERSION
        })
    
    return app


def register_blueprints(app):
    """Registra los blueprints - Agrega los tuyos aquí"""
    # =====================================================
    # [ZONA A] IMPORTAR BLUEPRINTS
    # Agrega tus importaciones aquí:
    # from routes.tu_modulo_routes import tu_modulo_bp
    # =====================================================
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # =====================================================
    # [ZONA B] REGISTRAR BLUEPRINTS
    # Ejemplo para agregar nuevo blueprint:
    # from routes.paciente_routes import paciente_bp
    # app.register_blueprint(paciente_bp)
    # =====================================================
    
    # --- AGREGAR NUEVOS BLUEPRINTS ABAJO DE ESTA LÍNEA ---
    # (Ejemplo commented como guía)
    # from routes.producto_routes import producto_bp
    # app.register_blueprint(producto_bp)
    # from routes.reporte_routes import reporte_bp
    # app.register_blueprint(reporte_bp)


def inject_context(app):
    """Inyecta variables globales a los templates"""
    # =====================================================
    # [ZONA C] AGREGAR VARIABLES GLOBALES A TEMPLATES
    # Agrega más valores al diccionario retornado:
    # return dict(
    #     current_user=current_user,
    #     app_name=Config.APP_NAME,
    #     nueva_variable="valor"
    # )
    # =====================================================
    @app.context_processor
    def inject_user():
        from models import Configuracion
        return dict(
            current_user=current_user,
            app_name=Config.APP_NAME,
            app_version=Config.APP_VERSION
        )


# Variable para socketio (si la necesitas)
socketio = None


# ==================== PUNTO DE ENTRADA ====================

# Crear instancia de la aplicación para Gunicorn
app = create_app()

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '1') in ['1', 'true']
    app.run(host='0.0.0.0', port=port, debug=debug)
