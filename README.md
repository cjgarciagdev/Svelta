# Flask Boilerplate

Plantilla reutilizable para proyectos Flask con autenticación, base de datos y despliegue listo para producción.

---

## Estructura del Proyecto

```
FlaskBoilerplate/
├── app.py                  # Factory de la aplicación (PUNTO DE ENTRADA)
├── config/
│   └── __init__.py         # Configuración global (APP_NAME, DB, etc.)
├── core/
│   └── __init__.py         # Extensiones (SQLAlchemy, LoginManager, etc.)
├── models.py               # Modelos de base de datos
├── routes/
│   ├── __init__.py
│   └── auth_routes.py     # Rutas de autenticación
├── templates/
│   ├── login.html
│   ├── index.html
│   └── dashboard.html
├── requirements.txt       # Dependencias del proyecto
├── Procfile               # Configuración para Render
├── runtime.txt            # Versión de Python
└── .env                   # Variables de entorno (no subir a git)
```

---

## Uso Rápido

### 1. Instalación
```bash
pip install -r requirements.txt
```

### 2. Configurar entorno
```bash
# Edita .env con tus valores
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://usuario:password@host:5432/dbname
```

### 3. Ejecutar en local
```bash
python app.py
```

### 4. Acceder
- Local: http://localhost:5000
- Login: http://localhost:5000/login

---

##  Cómo Crear un Nuevo Proyecto Desde Esta Plantilla

### Paso 1: Copiar la plantilla
```bash
# Copia toda la carpeta FlaskBoilerplate como tu nuevo proyecto
cp -r FlaskBoilerplate MiNuevoProyecto
cd MiNuevoProyecto
```

### Paso 2: Renombrar la aplicación
Edita [`config/__init__.py`](FlaskBoilerplate/config/__init__.py:19):
```python
APP_NAME = "MiNuevoProyecto"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Descripción de tu proyecto"
```

### Paso 3: Limpiar rutas de ejemplo
- Modifica [`routes/auth_routes.py`](FlaskBoilerplate/routes/auth_routes.py) con tus rutas de auth
- Limpia las plantillas en [`templates/`](FlaskBoilerplate/templates/)

### Paso 4: Configurar base de datos
Edita [`config/__init__.py`](FlaskBoilerplate/config/__init__.py:55) - método `get_database_uri()`

---

##  Cómo Agregar Nuevos Módulos/Blueprints

### Estructura recomendada para nuevos módulos

```
routes/
├── __init__.py
├── auth_routes.py        # (existente)
└── tu_modulo_routes.py  # (nuevo)
```

### Paso 1: Crear el archivo de rutas

Crea [`routes/tu_modulo_routes.py`](FlaskBoilerplate/routes/tu_modulo_routes.py):

```python
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from functools import wraps

# Definir Blueprint
tu_modulo_bp = Blueprint('tu_modulo', __name__, url_prefix='/tu-modulo')

# Decorador personalizado ejemplo
def rol_required(rol):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return "No autorizado", 403
            # Agregar verificación de rol si es necesario
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Rutas
@tu_modulo_bp.route('/')
@login_required
def index():
    """Página principal del módulo"""
    return render_template('tu_modulo/index.html')

@tu_modulo_bp.route('/api/datos')
@login_required
def api_datos():
    """API del módulo"""
    return jsonify({'datos': []})

# Agregar más rutas aquí...
```

### Paso 2: Registrar el Blueprint

Edita [`app.py`](FlaskBoilerplate/app.py:81) - función `register_blueprints()`:

```python
def register_blueprints(app):
    """Registra los blueprints"""
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # === AGREGAR NUEVO BLUEPRINT AQUÍ ===
    from routes.tu_modulo_routes import tu_modulo_bp
    app.register_blueprint(tu_modulo_bp)
```

### Paso 3: Crear plantillas (opcional)

Crea [`templates/tu_modulo/index.html`](FlaskBoilerplate/templates/tu_modulo/index.html):

```html
{% extends "base.html" %}

{% block content %}
<h1>Mi Módulo</h1>
<p>Contenido del módulo...</p>
{% endblock %}
```

---

## Cómo Agregar Nuevos Modelos

Edita [`models.py`](FlaskBoilerplate/models.py):

```python
from core import db
from datetime import datetime

class TuModelo(db.Model):
    """Descripción del modelo"""
    __tablename__ = 'tu_tabla'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuario', backref='mis_modelos')
    
    def __repr__(self):
        return f'<TuModelo {self.nombre}>'
    
    # Métodos útiles
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }
```

---

## Configuración de Producción (Render)

### Variables de entorno requeridas

En el dashboard de Render, configura:

| Variable | Valor ejemplo | Descripción |
|----------|---------------|-------------|
| `FLASK_ENV` | `production` | Modo producción |
| `SECRET_KEY` | `genera-una-clave-segura` | Clave para sesiones |
| `DATABASE_URL` | `postgresql://...` | URL de PostgreSQL |
| `PORT` | `5000` | Puerto (auto-configurado) |

### Generar SECRET_KEY segura
```python
import secrets
print(secrets.token_hex(32))
```

### Procfile (ya configurado)
```
web: gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:$PORT app:app --log-file -
```

### Desplegar
1. Sube el código a GitHub
2. Conecta el repositorio en Render
3. Crea un Web Service
4. Configura las variables de entorno
5. Deploy automático

---

## Comandos Útiles

### Desarrollo
```bash
python app.py              # Ejecutar servidor
python app.py --debug      # Modo debug
```

### Base de datos
```bash
# Las tablas se crean automáticamente con init_db()
# Para resetear, elimina instance/*.db
```

### Producción (Gunicorn)
```bash
gunicorn app:app
gunicorn --bind 0.0.0.0:5000 app:app
```

---

## Notas Importantes

1. **No subir .env a Git** - Agrega `.env` a `.gitignore`
2. **Cambiar SECRET_KEY en producción** - Nunca uses la clave por defecto
3. **DATABASE_URL** - Render provee esta variable automáticamente
4. ** Psycopg2** - Required para PostgreSQL, ya incluido en requirements.txt

---

## Estructura Base para Referencia

### app.py - Punto de entrada
- Línea 26: `create_app()` - Factory de la aplicación
- Línea 81: `register_blueprints()` - Registrar nuevos módulos
- Línea 91: `inject_context()` - Variables globales a templates

### config/__init__.py - Configuración
- Línea 19: `APP_NAME` - Nombre de la app
- Línea 22: `APP_VERSION` - Versión
- Línea 55: `get_database_uri()` - URI de base de datos

### core/__init__.py - Extensiones
- db: SQLAlchemy
- login_manager: Flask-Login

### models.py - Modelos
- Usuario: Modelo de usuario (ya incluido)

### routes/ - Rutas
- auth_routes.py: Autenticación (login, logout, registro)
