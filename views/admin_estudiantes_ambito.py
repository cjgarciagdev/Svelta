import flet as ft
from database.db import get_all_estudiantes, sync_google_forms, get_all_perfiles
from config.theme import INCES_BLUE, INCES_TEAL
from utils.report_generator import generate_estudiantes_report, generate_estudiantes_xlsx_report
import time
import threading
import os
import math

GOOGLE_SCRIPT_URL_AMBITO = "https://script.google.com/macros/s/AKfycbweM1zIrHOPvhSFNggExghoUHzRo9cUfkBr5CBO4cwl0i4PKWu6pxIwXABOnovEda4_/exec"
SCRIPT_TOKEN_AMBITO = "inces_admin_2026"

def admin_estudiantes_ambito_view(page: ft.Page):
    state = {
        "current_page": 1,
        "items_per_page": 8,
        "all_data": [],
        "filtered_data": []
    }

    # Controles de filtro
    search_field = ft.TextField(
        hint_text="Buscar cédula, nombre o apellido...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.PURPLE_600,
        height=40,
        text_size=13,
        expand=True,
        on_change=lambda e: handle_filter_change()
    )

    estado_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("TODOS"),
            ft.dropdown.Option("CENSADO"),
            ft.dropdown.Option("INSCRITO"),
            ft.dropdown.Option("CULMINADO"),
            ft.dropdown.Option("RETIRADO"),
            ft.dropdown.Option("RECHAZADO"),
        ],
        value="TODOS",
        width=150,
        height=40,
        text_size=13,
        border_radius=8,
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.PURPLE_600,
        on_select=lambda e: handle_filter_change()
    )

    curso_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("TODOS")],
        value="TODOS",
        width=180,
        height=40,
        text_size=13,
        border_radius=8,
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.PURPLE_600,
        on_select=lambda e: handle_filter_change()
    )

    # Cargar cursos en el dropdown
    perfiles = get_all_perfiles()
    for p in perfiles:
        curso_dropdown.options.append(ft.dropdown.Option(p["name"]))

    # Tabla
    estudiantes_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Cédula", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Nombres y Apellidos", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Género", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Correo", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Curso / Perfil", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Teléfono", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.PURPLE_200),
        border_radius=10,
        heading_row_color=ft.Colors.PURPLE_50,
        expand=True
    )

    # Paginación
    page_text = ft.Text("Página 1 de 1", size=13, weight=ft.FontWeight.BOLD)
    prev_btn = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        tooltip="Página anterior",
        icon_color=ft.Colors.PURPLE_600,
        on_click=lambda e: change_page(-1)
    )
    next_btn = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        tooltip="Página siguiente",
        icon_color=ft.Colors.PURPLE_600,
        on_click=lambda e: change_page(1)
    )

    loading_ring = ft.Container(
        content=ft.ProgressRing(color=ft.Colors.PURPLE_600, width=20, height=20),
        visible=False,
        margin=ft.Margin.only(right=10)
    )

    last_sync_text = ft.Text(
        "Última actualización: Nunca",
        size=12,
        color=ft.Colors.GREY_600,
        italic=True
    )

    def change_page(delta):
        state["current_page"] += delta
        render_table()

    def handle_filter_change():
        state["current_page"] = 1
        
        query = (search_field.value or "").lower().strip()
        f_estado = estado_dropdown.value
        f_curso = curso_dropdown.value

        filtered = []
        for est in state["all_data"]:
            estado = est["estado_inscripcion"] or "CENSADO"
            curso = est["perfil_nombre"] or "Sin asignar"
            
            # Filtro Estado
            if f_estado != "TODOS" and estado != f_estado:
                continue
            
            # Filtro Curso
            if f_curso != "TODOS" and curso != f_curso:
                continue
            
            # Filtro Búsqueda
            if query:
                cedula = str(est.get("cedula", "")).lower()
                nombres = str(est.get("nombres", "")).lower()
                apellidos = str(est.get("apellidos", "")).lower()
                if query not in cedula and query not in nombres and query not in apellidos:
                    continue
            
            filtered.append(est)
        
        state["filtered_data"] = filtered
        render_table()

    def render_table():
        total_items = len(state["filtered_data"])
        total_pages = math.ceil(total_items / state["items_per_page"]) if total_items > 0 else 1
        
        # Limitar la página actual a los rangos válidos
        if state["current_page"] > total_pages:
            state["current_page"] = total_pages
        if state["current_page"] < 1:
            state["current_page"] = 1

        start_idx = (state["current_page"] - 1) * state["items_per_page"]
        end_idx = start_idx + state["items_per_page"]
        page_data = state["filtered_data"][start_idx:end_idx]

        estudiantes_table.rows.clear()

        if not page_data:
            estudiantes_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("Sin registros", color=ft.Colors.GREY_600)),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("-")),
                ])
            )
        else:
            for idx, est in enumerate(page_data):
                num = (state["current_page"] - 1) * state["items_per_page"] + idx + 1
                estado_val = est["estado_inscripcion"] or "CENSADO"
                estado_color = INCES_TEAL if estado_val == 'INSCRITO' else ft.Colors.AMBER_700
                if estado_val in ['RECHAZADO', 'RETIRADO']:
                    estado_color = ft.Colors.RED_400
                elif estado_val == 'CULMINADO':
                    estado_color = ft.Colors.BLUE_700
                
                curso_nombre = est['perfil_nombre'] if est['perfil_nombre'] else "Sin asignar"
                
                estudiantes_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(num), weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_600)),
                        ft.DataCell(ft.Text(str(est.get('cedula', '')))),
                        ft.DataCell(ft.Text(f"{est.get('nombres', '')} {est.get('apellidos', '')}")),
                        ft.DataCell(ft.Text(est.get('genero', '') or "N/A")),
                        ft.DataCell(ft.Text(est.get('correo', '') or "N/A")),
                        ft.DataCell(ft.Text(curso_nombre)),
                        ft.DataCell(ft.Text(est.get('telefono', '') or "N/A")),
                        ft.DataCell(ft.Text(estado_val, color=estado_color, weight=ft.FontWeight.BOLD)),
                    ])
                )
        
        # Actualizar controles de paginación
        page_text.value = f"Página {state['current_page']} de {total_pages}"
        prev_btn.disabled = state["current_page"] <= 1
        next_btn.disabled = state["current_page"] >= total_pages
        
        page.update()

    def fetch_data():
        """Carga los datos de la base de datos a la tabla visual."""
        raw_data = get_all_estudiantes()
        # Solo cargar los que son de AMBITO
        state["all_data"] = [dict(r) for r in raw_data if dict(r).get('tipo_origen', 'GENERAL') == 'AMBITO']
        handle_filter_change()

    def handle_generate_xlsx_report(e):
        loading_ring.visible = True
        page.update()
        def _run():
            try:
                path = generate_estudiantes_xlsx_report(state["filtered_data"])
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
        loading_ring.visible = True
        page.update()
        def _run():
            try:
                path = generate_estudiantes_report(state["filtered_data"])
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

    def handle_sync(e=None):
        def _do_sync():
            loading_ring.visible = True
            page.update()

            success = sync_google_forms(GOOGLE_SCRIPT_URL_AMBITO, SCRIPT_TOKEN_AMBITO, tipo_origen="AMBITO")

            loading_ring.visible = False
            if success:
                last_sync_text.value = f"Última actualización: {time.strftime('%I:%M %p')}"
                fetch_data()
                if e is not None:
                    page.snack_bar = ft.SnackBar(ft.Text("Datos de Ámbito sincronizados"), bgcolor=ft.Colors.GREEN_700)
                    page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al sincronizar. Revisa tu conexión."), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True

            page.update()

        threading.Thread(target=_do_sync, daemon=True).start()

    # Botones principales
    sync_btn = ft.ElevatedButton("Refrescar Ámbito", icon=ft.Icons.SYNC, color=ft.Colors.WHITE, bgcolor=ft.Colors.PURPLE_600, on_click=handle_sync)
    report_btn = ft.ElevatedButton("PDF", icon=ft.Icons.PICTURE_AS_PDF, color=ft.Colors.WHITE, bgcolor=INCES_TEAL, on_click=handle_generate_report, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
    report_xlsx_btn = ft.ElevatedButton("Excel", icon=ft.Icons.GRID_ON, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700, on_click=handle_generate_xlsx_report, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

    header = ft.Row(
        controls=[
            ft.Text("Censo de Otros Ámbitos", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Row([
                last_sync_text, loading_ring, sync_btn, report_btn, report_xlsx_btn
            ], alignment=ft.MainAxisAlignment.END, spacing=8)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    filters_row = ft.Row(
        controls=[
            search_field,
            ft.Text("Estado:", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
            estado_dropdown,
            ft.Text("Curso:", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
            curso_dropdown
        ],
        spacing=15,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    pagination_row = ft.Row(
        controls=[
            prev_btn,
            page_text,
            next_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    content = ft.Column(
        controls=[
            header,
            filters_row,
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
            ft.ListView(
                controls=[
                    ft.Row([estudiantes_table], scroll=ft.ScrollMode.ALWAYS)
                ],
                expand=True,
                spacing=10
            ),
            pagination_row
        ],
        expand=True,
        spacing=20
    )

    # Iniciar la sincronización automática
    threading.Thread(target=handle_sync, daemon=True).start()

    return content
