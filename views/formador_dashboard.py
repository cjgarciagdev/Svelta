import math
import flet as ft
from database.db import get_perfiles_by_formador, get_estudiantes_by_formador, update_estado_inscripcion
from config.theme import INCES_BLUE, INCES_TEAL, SIDEBAR_BG

def formador_dashboard_view(page: ft.Page, user, on_logout):
    """Panel principal del Formador con Dropdown y Paginación."""

    content_area = ft.Container(
        expand=True, padding=20,
        content=ft.Column([], expand=True)
    )

    state = {
        "current_page": 1,
        "items_per_page": 8,
        "selected_perfil": None, # (perfil_id, entidad)
        "estudiantes_filtrados": []
    }

    def back_to_admin():
        from views.admin_dashboard import admin_dashboard_view
        page.clean()
        page.add(admin_dashboard_view(page, user, on_logout=on_logout))
        page.update()

    def load_dashboard():
        content_area.content.controls.clear()
        perfiles = get_perfiles_by_formador(user["id"])
        estudiantes = get_estudiantes_by_formador(user["id"])

        if not perfiles:
            content_area.content.controls.append(
                ft.Container(
                    padding=40,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=50, color=ft.Colors.GREY_400),
                        ft.Text("Aún no tienes perfiles asignados.", size=18, color=ft.Colors.GREY_500),
                        ft.Text("El administrador debe asignarte perfiles para que puedas ver estudiantes.", size=14, color=ft.Colors.GREY_400),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
                )
            )
            page.update()
            return

        # Construir opciones del Dropdown
        dropdown_options = []
        for p in perfiles:
            p_dict = dict(p)
            ent = p_dict.get("entidad", "")
            lbl = f"{p['name']} [{ent if ent else 'CFS'}]"
            # Usamos un string delimitado para el value porque flet Option value debe ser string
            val = f"{p['id']}|{ent}"
            dropdown_options.append(ft.dropdown.Option(val, lbl))

        if state["selected_perfil"] is None:
            state["selected_perfil"] = dropdown_options[0].key

        # Dropdown
        perfil_dropdown = ft.Dropdown(
            label="Selecciona un Perfil",
            options=dropdown_options,
            value=state["selected_perfil"],
            width=350,
            text_size=14,
            on_select=handle_perfil_change
        )

        # Filtrar estudiantes basados en la selección
        sel_parts = state["selected_perfil"].split('|')
        sel_perfil_id = int(sel_parts[0])
        sel_entidad = sel_parts[1] if len(sel_parts) > 1 else ""

        state["estudiantes_filtrados"] = [
            e for e in estudiantes 
            if e["perfil_id"] == sel_perfil_id 
            and dict(e).get("formador_entidad", "") == sel_entidad
        ]

        # Título y Controles superiores
        content_area.content.controls.append(
            ft.Row([
                ft.Column([
                    ft.Text("Mis Estudiantes", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                    ft.Text(f"Total en este perfil: {len(state['estudiantes_filtrados'])}", size=14, color=ft.Colors.GREY_600)
                ]),
                ft.Container(expand=True),
                perfil_dropdown
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        content_area.content.controls.append(ft.Divider(height=20, color=ft.Colors.GREY_300))

        # Configuración de Paginación
        total_items = len(state["estudiantes_filtrados"])
        total_pages = math.ceil(total_items / state["items_per_page"]) if total_items > 0 else 1
        if state["current_page"] > total_pages: state["current_page"] = total_pages
        
        start_idx = (state["current_page"] - 1) * state["items_per_page"]
        end_idx = start_idx + state["items_per_page"]
        page_data = state["estudiantes_filtrados"][start_idx:end_idx]

        # Tabla
        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cédula", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nombres", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Apellidos", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Teléfono", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Acción", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=10,
            expand=True
        )

        if not page_data:
            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("Sin registros", color=ft.Colors.GREY_600)),
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
                estado = est["estado_inscripcion"] or "CENSADO"

                # Colores según estado
                colores_estado = {
                    "CENSADO": (ft.Colors.GREY_700, ft.Colors.GREY_100),
                    "INSCRITO": (ft.Colors.GREEN_700, ft.Colors.GREEN_100),
                    "CULMINADO": (ft.Colors.BLUE_700, ft.Colors.BLUE_100),
                    "RETIRADO": (ft.Colors.RED_700, ft.Colors.RED_100),
                }
                tc, bc = colores_estado.get(estado, (ft.Colors.GREY_700, ft.Colors.GREY_100))

                estado_chip = ft.Container(
                    content=ft.Text(estado, size=11, weight=ft.FontWeight.BOLD, color=tc),
                    bgcolor=bc, padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=12
                )

                # Dropdown para cambiar estado
                dropdown = ft.Dropdown(
                    width=150, height=40, text_size=12,
                    value=estado,
                    options=[
                        ft.dropdown.Option("CENSADO"),
                        ft.dropdown.Option("INSCRITO"),
                        ft.dropdown.Option("CULMINADO"),
                        ft.dropdown.Option("RETIRADO"),
                    ],
                    data=est["id"],
                    on_select=lambda e: handle_estado_change(e.control.data, e.control.value)
                )

                tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(num), weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_600)),
                    ft.DataCell(ft.Text(str(est["cedula"]))),
                    ft.DataCell(ft.Text(est["nombres"])),
                    ft.DataCell(ft.Text(est["apellidos"])),
                    ft.DataCell(ft.Text(str(est["telefono"] or ""))),
                    ft.DataCell(estado_chip),
                    ft.DataCell(dropdown),
                ]))

        # Controles de paginación
        page_info = ft.Text(f"Página {state['current_page']} de {total_pages}", size=14, color=ft.Colors.GREY_700)
        
        def prev_page(e):
            if state["current_page"] > 1:
                state["current_page"] -= 1
                load_dashboard()
                
        def next_page(e):
            if state["current_page"] < total_pages:
                state["current_page"] += 1
                load_dashboard()

        btn_prev = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=INCES_TEAL,
            disabled=(state["current_page"] <= 1),
            on_click=prev_page
        )
        btn_next = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=INCES_TEAL,
            disabled=(state["current_page"] >= total_pages),
            on_click=next_page
        )
        pagination_row = ft.Row([btn_prev, page_info, btn_next], alignment=ft.MainAxisAlignment.CENTER)

        content_area.content.controls.append(ft.Row([tabla], scroll=ft.ScrollMode.AUTO, expand=True, vertical_alignment=ft.CrossAxisAlignment.START))
        content_area.content.controls.append(ft.Container(height=10))
        content_area.content.controls.append(pagination_row)

        page.update()

    def handle_perfil_change(e):
        state["selected_perfil"] = e.control.value
        state["current_page"] = 1
        load_dashboard()

    def handle_estado_change(estudiante_id, nuevo_estado):
        update_estado_inscripcion(estudiante_id, nuevo_estado)
        # Solo recargamos los datos para que se vea reflejado el estado
        load_dashboard()

    load_dashboard()

    # Sidebar del formador
    sidebar = ft.Container(
        width=250, bgcolor=SIDEBAR_BG, padding=20,
        border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_300)),
        content=ft.Column(expand=True, controls=[
            ft.Row([
                ft.Container(
                    content=ft.Image(src="Logo INCES.png", height=40, fit="contain", scale=2.8),
                    height=40,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=30, color=ft.Colors.GREY_300),
            ft.Text("Formador:", size=11, color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
            ft.Text(f"{user['nombres']} {user['apellidos']}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(height=20),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.HOME, color=ft.Colors.BLACK54, size=20), ft.Text("Mis Estudiantes", size=14, weight=ft.FontWeight.W_500)]),
                padding=ft.padding.symmetric(vertical=12, horizontal=15), border_radius=8, ink=True,
                on_click=lambda _: load_dashboard()
            ),
            ft.Container(expand=True),
            
            # BOTÓN PARA VOLVER AL PANEL DE ADMIN (Solo si es ADMIN)
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, color=ft.Colors.BLUE_600, size=20), ft.Text("Volver a Admin", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)]),
                padding=ft.padding.symmetric(vertical=10, horizontal=15), border_radius=8, ink=True,
                on_click=lambda _: back_to_admin()
            ) if user["role"] == "ADMIN" else ft.Container(),

            ft.Divider(height=20, color=ft.Colors.GREY_300),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400, size=20), ft.Text("Cerrar Sesión", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400)]),
                padding=ft.padding.symmetric(vertical=10, horizontal=15), border_radius=8, ink=True,
                on_click=lambda _: on_logout()
            )
        ])
    )

    return ft.Row(expand=True, spacing=0, controls=[sidebar, content_area])
