# Manual Técnico — Portal de Censo e Inscripción INCES

---

## 1. Introducción

El **Portal de Censo e Inscripción** es una aplicación de escritorio desarrollada para el **Instituto Nacional de Capacitación y Educación Socialista (INCES)**. Su propósito es centralizar y gestionar todo el flujo de registro de participantes en los cursos de formación, desde el censo inicial hasta la culminación o retiro del estudiante.

**Beneficios principales:**

- **Automatización:** Los datos se sincronizan automáticamente desde los formularios de Google Forms, eliminando la carga manual.
- **Trazabilidad:** Cada participante pasa por estados claros (Censado → Inscrito → Culminado / Retirado), permitiendo un seguimiento preciso.
- **Reportes al instante:** Genere listados en PDF y Excel con estadísticas agrupadas por trimestre o por curso.
- **Roles definidos:** Administradores y formadores tienen vistas y permisos adaptados a sus tareas.

---

## 2. Requisitos del Sistema

| Requisito | Detalle |
|---|---|
| **Sistema operativo** | Windows 10 o superior |
| **Software necesario** | Python 3.10+ y las dependencias listadas en `requirements.txt` |
| **Ejecución** | Abra una terminal en la carpeta del proyecto y ejecute: `python main.py` |
| **Conexión a Internet** | Necesaria solo para sincronizar datos desde Google Forms |
| **Credenciales** | Correo electrónico y contraseña proporcionados por el administrador del sistema |

---

## 3. Arquitectura de la Aplicación

La aplicación está construida con **Flet (0.85+)**, un framework que permite crear interfaces de escritorio con Python utilizando controles de Flutter. La base de datos es **SQLite** (`inces.sqlite`).

**Estructura del proyecto:**

| Directorio/Archivo | Descripción |
|---|---|
| `main.py` | Punto de entrada de la aplicación |
| `config/theme.py` | Constantes de colores y estilos |
| `database/db.py` | Inicialización y consultas de la base de datos |
| `components/` | Componentes reutilizables (header, sidebar, help widgets) |
| `views/` | Vistas de cada sección del panel administrativo y de formadores |
| `utils/report_generator.py` | Generación de reportes PDF y Excel |
| `docs/` | Documentación técnica y manuales |
| `assets/` | Recursos estáticos (imágenes, íconos) |

**Flujo de navegación:**

1. `main.py` muestra un splash screen con el logo del INCES.
2. Transición automática a la pantalla de **login**.
3. Según el rol del usuario, se redirige al panel de **Administrador** o **Formador**.
4. Cada panel contiene un **sidebar** lateral para navegar entre las distintas secciones.

---

## 4. Base de Datos

**Archivo:** `inces.sqlite` (se crea automáticamente al ejecutar `main.py`)

**Tablas principales:**

| Tabla | Propósito |
|---|---|
| `usuarios` | Almacena credenciales, roles y estados de los usuarios |
| `perfiles` | Catálogo de cursos de formación |
| `formador_perfiles` | Relación muchos a muchos entre formadores y perfiles (con entidad) |
| `estudiantes` | Datos de los participantes censados (desde Google Forms) |
| `estudiantes_ambito` | Datos del censo de otros ámbitos |

**Estados de un estudiante:** CENSADO → INSCRITO → CULMINADO / RETIRADO

**Estados de un usuario:** PENDING → APPROVED / REJECTED

---

## 5. Guía de Instalación y Ejecución

1. Clone o descargue el repositorio del proyecto.
2. Asegúrese de tener **Python 3.10 o superior** instalado.
3. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Ejecute la aplicación:
   ```
   python main.py
   ```
5. La base de datos se crea automáticamente en la primera ejecución.
6. Inicie sesión con las credenciales proporcionadas por el administrador del sistema.

---

## 6. Funcionalidades por Rol

### 6.1 Administrador

| Sección | Descripción |
|---|---|
| **Inicio** | Dashboard con estadísticas generales (total de censados, gráficos por género, discapacidad, cursos más demandados) |
| **Usuarios** | Gestión de formadores: aprobar, rechazar, asignar cursos y cambiar roles |
| **Perfiles** | Alta, baja y modificación de cursos de formación |
| **Censo CFS** | Listado de participantes del censo principal, con filtros y exportación |
| **Censo de Otros Ámbitos** | Segundo censo (formulario alternativo) con las mismas funcionalidades |

### 6.2 Formador

| Sección | Descripción |
|---|---|
| **Mis Estudiantes** | Tabla de estudiantes filtrada por curso asignado, con opción de cambiar estado de inscripción |

---

## 7. Sincronización con Google Forms

La aplicación consume datos desde **Google Apps Script** mediante peticiones HTTP GET.

**Endpoints configurados:**

- **Censo CFS:** `GOOGLE_SCRIPT_URL` en `admin_estudiantes.py`
- **Censo Otros Ámbitos:** `GOOGLE_SCRIPT_URL_AMBITO` en `admin_estudiantes_ambito.py`

Cada endpoint debe devolver un JSON con la estructura esperada por la base de datos. La sincronización se invoca manualmente desde los botones **"Refrescar Censo"** y **"Refrescar Ámbito"** respectivamente.

---

## 8. Reportes

Los reportes se generan en los formatos **PDF** y **Excel** y se guardan en la carpeta `reports/`.

**Tipos de reporte:**

- **General:** Todos los participantes filtrados en la vista actual.
- **Trimestral:** Agrupados por trimestre de inscripción.

**Tecnología:** La generación de PDF utiliza la biblioteca **FPDF**. Los archivos Excel se generan con **openpyxl**.

---

## 9. Mantenimiento y Troubleshooting

**Problema:** La aplicación no inicia.
- Verifique que Python 3.10+ esté instalado: `python --version`
- Instale las dependencias: `pip install -r requirements.txt`

**Problema:** Los datos no se sincronizan.
- Verifique su conexión a Internet.
- Confirme que el script de Google Apps Script está desplegado y accesible.
- Revise la consola en busca de errores HTTP.

**Problema:** Error al generar reportes.
- Asegúrese de que la carpeta `reports/` exista y tenga permisos de escritura.
- Verifique que haya datos filtrados en la vista actual.

**Problema:** El formador no puede iniciar sesión.
- Confirme que su cuenta ha sido aprobada por un administrador.
- Verifique que el curso esté asignado correctamente.

---

## 10. Personalización

**Colores:** Las constantes de color se definen en `config/theme.py`. Modifique los valores HEX para cambiar la paleta de la aplicación.

**Rutas de assets:** Las imágenes y recursos estáticos se almacenan en `assets/`. El logo principal es `Logo INCES.png` en la raíz del proyecto.

---

*Documento Técnico generado para el Instituto Nacional de Capacitación y Educación Socialista (INCES). Versión 2.0 — Junio 2026.*
