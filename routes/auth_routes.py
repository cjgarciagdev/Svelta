"""
Auth Routes - Plantilla de Autenticación
=======================================
Copia este archivo y personalízalo.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
from models import db, Usuario
from config import Config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página y proceso de login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        try:
            usuario = Usuario.query.filter_by(username=username).first()
            
            if not usuario:
                error = 'Usuario no encontrado'
            elif not usuario.activo:
                error = 'Usuario inactivo'
            elif not usuario.check_password(password):
                error = 'Contraseña incorrecta'
            elif usuario.rol not in Config.ALLOWED_ROLES:
                error = f'Rol no autorizado. Roles permitidos: {", ".join(Config.ALLOWED_ROLES)}'
            else:
                session.permanent = True
                login_user(usuario, remember=True, duration=timedelta(days=30))
                return redirect(url_for('dashboard'))
                
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render_template('login.html', error=error)


@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra sesión"""
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevos usuarios - Opcional"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        nombre = request.form.get('nombre', '').strip()
        
        # Verificar si existe
        if Usuario.query.filter_by(username=username).first():
            return render_template('registro.html', error='Usuario ya existe')
        
        # Crear usuario
        usuario = Usuario(
            username=username,
            email=email,
            nombre_completo=nombre,
            rol=Config.DEFAULT_ROLE
        )
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('registro.html')
