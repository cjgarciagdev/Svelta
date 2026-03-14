# Flask Boilerplate

Plantilla reutilizable para proyectos Flask con autenticación (opcional), base de datos y despliegue listo para producción.

> **Estado actual: SIN AUTH** - El sistema de login está comentado. Descomenta las secciones `[LOGIN]` para activarlo.

---

##  Estructura del Proyecto

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
│   └── auth_routes.py     # Rutas de autenticación (comentadas)
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

##  Uso Rápido

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

---

## Activar Sistema de Login

El sistema de autenticación está **comentado** para mantener la app pública. Para activarlo:

### 1. Descomenta en `app.py`:
- Importar `current_user, login_required` de flask_login
- Configurar `login_manager.user_loader`
- Registrar `auth_bp` en `register_blueprints()`
- Agregar `current_user` al context processor

### 2. Descomenta en `core/__init__.py`:
- Importar `LoginManager`
- Crear instancia `login_manager`
- Inicializar en `init_extensions()`

### 3. Rutas de auth ya existen en:
- `routes/auth_routes.py` (ya están creadas, solo necesitas registrarlas)

### 4. Acceso:
- Login: http://localhost:5000/auth/login
- Registro: http://localhost:5000/auth/registro
- Logout: http://localhost:5000/auth/logout

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
- Modifica [`routes/`](FlaskBoilerplate/routes/) con tus rutas
- Limpia las plantillas en [`templates/`](FlaskBoilerplate/templates/)

### Paso 4: Configurar base de datos
Edita [`config/__init__.py`](FlaskBoilerplate/config/__init__.py:55) - método `get_database_uri()`

---

##  Cómo Agregar Nuevos Módulos/Blueprints

### Estructura recomendada para nuevos módulos

```
routes/
├── __init__.py
└── tu_modulo_routes.py  # (nuevo)
```

### Paso 1: Crear el archivo de rutas

Crea [`routes/tu_modulo_routes.py`](FlaskBoilerplate/routes/tu_modulo_routes.py):

```python
from flask import Blueprint, render_template, jsonify

tu_modulo_bp = Blueprint('tu_modulo', __name__, url_prefix='/tu-modulo')

@tu_modulo_bp.route('/')
def index():
    return render_template('tu_modulo/index.html')

@tu_modulo_bp.route('/api/datos')
def api_datos():
    return jsonify({'datos': []})
```

### Paso 2: Registrar el Blueprint

Edita [`app.py`](FlaskBoilerplate/app.py:81) - función `register_blueprints()`:

```python
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
{% endblock %}
```

---

##  Cómo Agregar Nuevos Modelos

Edita [`models.py`](FlaskBoilerplate/models.py):

```python
class TuModelo(db.Model):
    """Descripción del modelo"""
    __tablename__ = 'tu_tabla'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TuModelo {self.nombre}>'
```

---

##  Configuración de Producción (Render)

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

##  Notas Importantes

1. **No subir .env a Git** - Agrega `.env` a `.gitignore`
2. **Cambiar SECRET_KEY en producción** - Nunca uses la clave por defecto
3. **DATABASE_URL** - Render provee esta variable automáticamente
4. ** Psycopg2** - Requiere psycopg2-binary para PostgreSQL
5. **Login** - El sistema de auth está comentado por defecto
