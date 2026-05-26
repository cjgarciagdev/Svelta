import flet as ft
from database.db import get_all_estudiantes, sync_google_forms
from config.theme import INCES_BLUE, INCES_TEAL
from utils.report_generator import generate_estudiantes_report, generate_estudiantes_xlsx_report
import time
import threading
import os

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwux_BKbkRt41oIiMOZaP_XpWf-VaFhbBIrTW-cQfzItisPH_Bs9PSYUuy1A_L5gnP1Tw/exec"
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
        margin=ft.Margin.only(right=10)
    )

    # Texto que muestra la última vez que se actualizó
    last_sync_text = ft.Text(
        "Última actualización: Nunca",
        size=12,
        color=ft.Colors.GREY_600,
        italic=True
    )

    def handle_generate_xlsx_report(e):
        """Genera el reporte Excel con los datos actuales de la tabla."""
        loading_ring.visible = True
        page.update()

        def _run():
            try:
                data = get_all_estudiantes()
                path = generate_estudiantes_xlsx_report(list(data))
                loading_ring.visible = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                        ft.Text(f"Reporte Excel generado: {os.path.basename(path)}", color=ft.Colors.WHITE),
                    ]),
                    bgcolor=ft.Colors.GREEN_700,
                    duration=5000,
                )
                page.snack_bar.open = True
                # Abrir la carpeta donde se guardó el Excel
                os.startfile(os.path.dirname(path))
            except Exception as ex:
                loading_ring.visible = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al generar reporte Excel: {ex}", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                )
                page.snack_bar.open = True
            page.update()

        threading.Thread(target=_run, daemon=True).start()

    def handle_generate_report(e):
        """Genera el reporte PDF con los datos actuales de la tabla."""
        loading_ring.visible = True
        page.update()

        def _run():
            try:
                data = get_all_estudiantes()
                path = generate_estudiantes_report(list(data))
                loading_ring.visible = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                        ft.Text(f"Reporte generado: {os.path.basename(path)}", color=ft.Colors.WHITE),
                    ]),
                    bgcolor=ft.Colors.GREEN_700,
                    duration=5000,
                )
                page.snack_bar.open = True
                # Abrir la carpeta donde se guardó el PDF
                os.startfile(os.path.dirname(path))
            except Exception as ex:
                loading_ring.visible = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al generar reporte: {ex}", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                )
                page.snack_bar.open = True
            page.update()

        threading.Thread(target=_run, daemon=True).start()


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

    # Botón de reporte PDF
    report_btn = ft.ElevatedButton(
        "Descargar Reporte PDF",
        icon=ft.Icons.PICTURE_AS_PDF,
        color=ft.Colors.WHITE,
        bgcolor=INCES_TEAL,
        on_click=handle_generate_report,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    # Botón de reporte Excel
    report_xlsx_btn = ft.ElevatedButton(
        "Descargar Reporte Excel",
        icon=ft.Icons.GRID_ON,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_700,
        on_click=handle_generate_xlsx_report,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    header = ft.Row(
        controls=[
            ft.Text("Estudiantes Censados", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Row([
                last_sync_text,
                loading_ring,
                sync_btn,
                report_btn,
                report_xlsx_btn,
            ], alignment=ft.MainAxisAlignment.END, spacing=8)
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
