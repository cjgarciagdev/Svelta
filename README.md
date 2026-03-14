
## Leyes del Desarrollador (Protocolo Obligatorio)

Para mantener la integridad y estabilidad, todo colaborador debe seguir estas normas:

### 1. Propiedad y Edición de Módulos
* **Privacidad de Módulos:** No está permitido editar módulos o archivos desarrollados por otro programador sin su autorización expresa.
* **Consenso de Mejoras:** Se permiten mejoras de rendimiento o refactorización siempre que el resto del grupo esté de acuerdo y no se altere la funcionalidad general del sistema.

### 2. Documentación y Trazabilidad
* **Registro de Cambios:** Todo nuevo desarrollo debe comentarse directamente en el código o registrarse en un archivo de descripción.
* **Detalle Obligatorio:** Se debe especificar **QUÉ** se hizo y **DÓNDE** (archivos y funciones afectados) para facilitar la auditoría.

### 3. Estabilidad y "Zero Errors"
* **Estado de Entrega:** Está estrictamente prohibido dejar el sistema con errores. 
* **Verificación de Host:** Tras cualquier cambio, es obligatorio verificar que el host (Render/Local) cargue correctamente.
* **Responsabilidad de Reparación:** Si un cambio causa que el sistema no cargue, el desarrollador responsable debe reparar el error de inmediato o revertir sus cambios.

### 4. Control de Stack Tecnológico
* **Nuevos Lenguajes:** No se permite añadir nuevos lenguajes de programación o frameworks sin la aceptación unánime de todo el grupo de desarrollo.
* **Limpieza:** No dejar código muerto, comentarios "por si acaso" o impresiones de depuración (`print`) en producción. Se permite en **CASOS EXCEPCIONALES**, siempre que sea para un avance posterior y no afecte la integridad del resto del sistema.
### Estructura Actual
* **FlaskBoilerplate/**

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
