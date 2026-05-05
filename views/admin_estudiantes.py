import flet as ft
from database.db import get_all_estudiantes, sync_google_forms
from config.theme import INCES_BLUE, INCES_TEAL
import time
import threading

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby7QNF_2g2hgq0yyL-Pwop4z8-BrfxkOqJAbk2rnAtdjQkm4jHmN8togjqbzenDf5kw/exec"
SCRIPT_TOKEN = "inces_admin_2026"

def admin_estudiantes_view(page: ft.Page):
    # Tabla de estudiantes
    estudiantes_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cédula", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Nombres y Apellidos", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Curso / Perfil", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Teléfono", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
        ],
        rows=[],
        border=ft.border.all(1, INCES_TEAL),
        border_radius=10,
        heading_row_color=ft.Colors.with_opacity(0.1, INCES_TEAL),
        expand=True
    )

    # Contenedor para el anillo de carga
    loading_ring = ft.Container(
        content=ft.ProgressRing(color=INCES_TEAL, width=20, height=20),
        visible=False,
        margin=ft.margin.only(right=10)
    )

    # Texto que muestra la última vez que se actualizó
    last_sync_text = ft.Text(
        "Última actualización: Nunca",
        size=12,
        color=ft.Colors.GREY_600,
        italic=True
    )

    def load_table_data():
        """Carga los datos de la base de datos a la tabla visual."""
        estudiantes = get_all_estudiantes()
        estudiantes_table.rows.clear()
        
        if not estudiantes:
            # Fila vacía si no hay estudiantes
            estudiantes_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Sin registros", color=ft.Colors.GREY_600)),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                ])
            )
        else:
            for est in estudiantes:
                # Determinar color según estado
                estado_color = INCES_TEAL if est['estado_inscripcion'] == 'INSCRITO' else ft.Colors.AMBER_700
                if est['estado_inscripcion'] == 'RECHAZADO' or est['estado_inscripcion'] == 'RETIRADO':
                    estado_color = ft.Colors.RED_400
                
                curso_nombre = est['perfil_nombre'] if est['perfil_nombre'] else "Sin asignar"
                
                estudiantes_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(est['cedula'])),
                        ft.DataCell(ft.Text(f"{est['nombres']} {est['apellidos']}")),
                        ft.DataCell(ft.Text(curso_nombre)),
                        ft.DataCell(ft.Text(est['telefono'] or "N/A")),
                        ft.DataCell(ft.Text(est['estado_inscripcion'], color=estado_color, weight=ft.FontWeight.BOLD)),
                    ])
                )
        page.update()

    def handle_sync(e=None):
        """Función que ejecuta la sincronización con Google Forms."""
        loading_ring.visible = True
        page.update()
        
        # Llamada a la API de Google
        success = sync_google_forms(GOOGLE_SCRIPT_URL, SCRIPT_TOKEN)
        
        loading_ring.visible = False
        if success:
            last_sync_text.value = f"Última actualización: {time.strftime('%I:%M %p')}"
            load_table_data()
            
            # Mostrar snackbar solo si fue manual
            if e is not None:
                page.snack_bar = ft.SnackBar(ft.Text("Datos sincronizados correctamente con Google Forms"), bgcolor=ft.Colors.GREEN_700)
                page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al sincronizar. Revisa tu conexión."), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            
        page.update()

    # Botón de refrescar manual
    sync_btn = ft.ElevatedButton(
        "Refrescar Censo",
        icon=ft.Icons.SYNC,
        color=ft.Colors.WHITE,
        bgcolor=INCES_BLUE,
        on_click=handle_sync
    )

    header = ft.Row(
        controls=[
            ft.Text("Estudiantes Censados", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Row([
                last_sync_text,
                loading_ring,
                sync_btn
            ], alignment=ft.MainAxisAlignment.END)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    content = ft.Column(
        controls=[
            header,
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
            # Usar ListView para que la tabla pueda hacer scroll si hay muchos estudiantes
            ft.ListView(
                controls=[
                    ft.Row([estudiantes_table], scroll=ft.ScrollMode.ALWAYS) # Scroll horizontal por si la pantalla es pequeña
                ],
                expand=True,
                spacing=10
            )
        ],
        expand=True,
        spacing=20
    )

    # -----------------------------------------------------
    # ¡LA MAGIA DE LA SINCRONIZACIÓN AUTOMÁTICA!
    # Usamos un Thread para que corra en segundo plano y no bloquee ni cause errores de corrutinas
    # -----------------------------------------------------
    threading.Thread(target=handle_sync, daemon=True).start()

    return content
