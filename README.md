# Flask Boilerplate

Plantilla reutilizable para proyectos Flask.

## Estructura

```
mi-proyecto/
├── app.py              # Factory de la aplicación
├── config/
│   └── __init__.py    # Configuración
├── core/
│   └── __init__.py    # Extensiones
├── models.py           # Modelos de DB
├── routes/
│   ├── __init__.py
│   └── auth_routes.py  # Rutas de auth
├── templates/
│   ├── login.html
│   └── index.html
└── requirements.txt
```

## Uso

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno (opcional):**
   ```bash
   # .env
   FLASK_ENV=development
   SECRET_KEY=tu-clave-secreta
   DATABASE_URL=postgresql://...
   ```

3. **Ejecutar:**
   ```bash
   python app.py
   ```

4. **Acceder:** http://localhost:5000

## Personalización

### 1. Cambiar nombre de app
Edita `config/__init__.py`:
```python
APP_NAME = "MiNuevaApp"
```

### 2. Agregar modelos
Edita `models.py` y agrega tus clases.

### 3. Agregar rutas
Crea nuevos archivos en `routes/` y regístralos en `app.py`.

### 4. Desplegar en Render
Agrega en Render:
- `DATABASE_URL`: Tu URL de PostgreSQL
- `SECRET_KEY`: Genera una clave segura
