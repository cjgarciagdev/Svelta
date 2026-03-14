"""
Modelos de Base de Datos - Plantilla
====================================
Copia este archivo y edita los modelos según tu proyecto.

Para usar:
1. Copia models.py como tu modelo base
2. Edita las clases abajo
3. Agrega tus propios modelos
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ==================== USUARIO (Sistema de Auth) ====================
# =====================================================
# [ZONA 1] MODELO DE USUARIO - EDITAR AQUÍ
# Este modelo es requerido para Flask-Login
# =====================================================

class Usuario(UserMixin, db.Model):
    """Modelo de Usuario base - Edita según necesidad"""
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='usuario')
    nombre_completo = db.Column(db.String(120))
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime)
    cambio_password_requerido = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        try:
            if check_password_hash(self.password_hash, password):
                return True
        except:
            pass
        return self.password_hash == password
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'rol': self.rol,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'activo': self.activo
        }


# ==================== MODELOS PERSONALIZADOS ====================
# =====================================================
# [ZONA 2] AGREGAR NUEVOS MODELOS AQUÍ
# Copia el siguiente template para nuevos modelos:
#
# class TuNuevoModelo(db.Model):
#     """Descripción del modelo"""
#     __tablename__ = 'tu_tabla'
#     
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(100), nullable=False)
#     descripcion = db.Column(db.Text)
#     fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
#     activo = db.Column(db.Boolean, default=True)
#     
#     # Relaciones
#     usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
#     usuario = db.relationship('Usuario', backref='mis_registros')
#     
#     def __repr__(self):
#         return f'<TuNuevoModelo {self.nombre}>'
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'nombre': self.nombre
#         }
# =====================================================

class Registro(db.Model):
    """Ejemplo: Modelo base para registros"""
    __tablename__ = 'registro'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    datos = db.Column(db.Text)  # JSON string
    notas = db.Column(db.Text)
    
    usuario = db.relationship('Usuario', backref='registros')


class Configuracion(db.Model):
    """Configuración global del sistema"""
    __tablename__ = 'configuracion'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.Text)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def obtener(clave, valor_default=None):
        config = Configuracion.query.filter_by(clave=clave).first()
        return config.valor if config else valor_default
    
    @staticmethod
    def establecer(clave, valor):
        config = Configuracion.query.filter_by(clave=clave).first()
        if config:
            config.valor = valor
        else:
            config = Configuracion(clave=clave, valor=valor)
            db.session.add(config)
        db.session.commit()


# ==================== AGREGAR MODELOS ADICIONALES ABAJO ====================
# --- Modelos de ejemplo commentados como guía ---
# 
# class Producto(db.Model):
#     """Modelo de productos"""
#     __tablename__ = 'producto'
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(100), nullable=False)
#     precio = db.Column(db.Float)
#     stock = db.Column(db.Integer, default=0)
#     categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
#     categoria = db.relationship('Categoria', backref='productos')
# 
# class Categoria(db.Model):
#     """Modelo de categorías"""
#     __tablename__ = 'categoria'
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(50), nullable=False)


# ==================== FUNCIÓN DE INICIALIZACIÓN ====================
# =====================================================
# [ZONA 3] INICIALIZACIÓN DE BASE DE DATOS
# db.create_all() crea las tablas automáticamente
# =====================================================

def init_db(app):
    """Inicializa la base de datos"""
    with app.app_context():
        db.create_all()
        print("[OK] Base de datos creada")


def seed_default_data(app):
    """Agrega datos por defecto - Sobrescribe en tu proyecto"""
    # =====================================================
    # [ZONA 4] DATOS POR DEFECTO
    # Agrega datos iniciales aquí si es necesario
    # =====================================================
    with app.app_context():
        # Crear usuario admin si no existe
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                rol='admin',
                nombre_completo='Administrador',
                email='admin@ejemplo.com'
            )
            admin.set_password('Admin123@')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Usuario admin creado")
        
        # Agregar más datos por defecto aquí...
        # ejemplo: crear categorías iniciales
        # if not Categoria.query.first():
        #     cat = Categoria(nombre='General')
        #     db.session.add(cat)
        #     db.session.commit()
