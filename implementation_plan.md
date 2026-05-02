# Sistema de Censo e Inscripción INCES

Este documento define la arquitectura y los requisitos funcionales del sistema de escritorio para el INCES, basado en la información proporcionada.

## Flujo Principal
1. **Censo:** Los estudiantes escanean un QR y llenan un Google Form. Eligen su curso ("perfil") de una lista desplegable.
2. **Ingreso al Sistema:** Los datos pasan del Google Form a la base de datos del sistema.
3. **Gestión:** Admins y Formadores ingresan a la App Desktop para gestionar la información, enviar comunicados y generar reportes.

## Arquitectura y Base de Datos (Solución al Dilema Desktop)

Dado que es una App Desktop pero necesita ser accedida desde múltiples computadoras por diferentes Formadores, tenemos dos caminos. **Recomendamos la Opción A**:

*   **Opción A (Base de Datos en la Nube - Recomendada):** La app está instalada en cada PC local, pero se conecta a una base de datos gratuita en la nube (como Supabase o Firebase). **Ventaja:** Cualquier formador con internet puede acceder desde cualquier PC. **Desventaja:** Requiere internet activo.
*   **Opción B (Red Local LAN):** Una computadora en el INCES actúa como "Servidor" con la base de datos (PostgreSQL/MySQL). Las demás PC se conectan a ella por el WiFi local. **Ventaja:** No requiere internet. **Desventaja:** Requiere que la PC "Servidor" esté siempre encendida y configurada en la misma red.

## Integración con Google Forms (Recomendación)

**Recomendamos una integración semi-automática o automática.**
1.  **Automática:** Usar la API de Google Sheets para que el sistema lea automáticamente las nuevas respuestas cada vez que un Admin o Formador presione un botón de "Sincronizar".
2.  **Manual (Plan B):** El Admin descarga un archivo Excel/CSV del Google Form y lo carga en la App Desktop mediante un botón de "Importar".

## Roles y Permisos

### 1. Administrador
*   **Gestión de Perfiles (Cursos):** Crear, editar, suspender y reactivar perfiles.
*   **Gestión de Usuarios:** Aprobar/rechazar registros de nuevos Formadores. Asignar Formadores a perfiles específicos.
*   **Visibilidad Global:** Ver todos los estudiantes censados en todos los perfiles.
*   **Reportes y Dashboards:** Ver estadísticas generales (total censados, cursos más populares, etc.) y exportar reportes (PDF/Excel).

### 2. Formador
*   **Visibilidad Limitada:** Solo puede ver a los estudiantes censados en los perfiles que el Admin le haya asignado.
*   **Comunicación:** Módulo de envío de correos masivos o selectivos a sus estudiantes (notificaciones de inicio, horarios, etc.).

## Propuestas Adicionales para Evaluar

*   **Estados del Estudiante:** Un estudiante entra como "Censado". ¿Debería el Formador o Admin cambiar su estado a "Inscrito", "Culminado" o "Retirado"?
*   **Control de Cupos:** ¿Tienen límite de cupos los perfiles? Si el límite es 20, ¿qué pasa con el estudiante número 21?
*   **Asistencia/Calificaciones:** ¿El formador llevará el control de notas o asistencia dentro de este sistema, o solo es para la fase inicial de censo/inscripción?

## Open Questions

> [!IMPORTANT]  
> Por favor, respóndeme estas preguntas para definir la arquitectura final:
> 1. ¿Hay buena conexión a internet en las computadoras del INCES para usar la **Opción A** (Base de datos en la nube)?
> 2. Respecto al Google Form: ¿Prefieres que el sistema se conecte directo a Google Sheets (Automático) o que el Admin suba un archivo Excel (Manual)?
> 3. ¿El sistema debe manejar un límite de cupos por curso?
> 4. Una vez que el estudiante está en el sistema, ¿qué estados puede tener? (Ej: Censado -> Inscrito -> Aprobado/Reprobado).
