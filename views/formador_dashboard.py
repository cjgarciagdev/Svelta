import flet as ft
from database.db import get_perfiles_by_formador, get_estudiantes_by_formador, update_estado_inscripcion
from config.theme import INCES_BLUE, INCES_TEAL, SIDEBAR_BG

def formador_dashboard_view(page: ft.Page, user, on_logout):
    """Panel principal del Formador."""

    content_area = ft.Container(
        expand=True, padding=20,
        content=ft.Column([], scroll=ft.ScrollMode.AUTO)
    )

    def back_to_admin():
        from views.admin_dashboard import admin_dashboard_view
        page.clean()
        page.add(admin_dashboard_view(page, user, on_logout=on_logout))
        page.update()

    def load_dashboard():
        content_area.content.controls.clear()
        perfiles = get_perfiles_by_formador(user["id"])
        estudiantes = get_estudiantes_by_formador(user["id"])

        # Título
        content_area.content.controls.append(
            ft.Text("Mis Cursos Asignados", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE)
        )

        if not perfiles:
            content_area.content.controls.append(
                ft.Container(
                    padding=40,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=50, color=ft.Colors.GREY_400),
                        ft.Text("Aún no tienes perfiles asignados.", size=18, color=ft.Colors.GREY_500),
                        ft.Text("El administrador debe asignarte cursos para que puedas ver estudiantes.", size=14, color=ft.Colors.GREY_400),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
                )
            )
            page.update()
            return

        # Por cada perfil, mostrar sus estudiantes
        for perfil in perfiles:
            estudiantes_perfil = [e for e in estudiantes if e["perfil_name"] == perfil["name"]]

            # Tabla de estudiantes de este perfil
            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Cédula", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Nombres", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Apellidos", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Teléfono", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Acción", weight=ft.FontWeight.BOLD)),
                ],
                rows=[]
            )

            for est in estudiantes_perfil:
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
                    ft.DataCell(ft.Text(str(est["cedula"]))),
                    ft.DataCell(ft.Text(est["nombres"])),
                    ft.DataCell(ft.Text(est["apellidos"])),
                    ft.DataCell(ft.Text(str(est["telefono"] or ""))),
                    ft.DataCell(estado_chip),
                    ft.DataCell(dropdown),
                ]))

            # Tarjeta del perfil
            card = ft.Container(
                bgcolor=ft.Colors.WHITE, padding=20, border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SCHOOL, color=INCES_TEAL, size=25),
                        ft.Text(perfil["name"], size=20, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                        ft.Container(
                            content=ft.Text(f"{len(estudiantes_perfil)} estudiantes", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=INCES_TEAL, padding=ft.padding.symmetric(horizontal=10, vertical=5), border_radius=12
                        )
                    ]),
                    ft.Divider(height=10, color=ft.Colors.GREY_300),
                    ft.Row([tabla], scroll=ft.ScrollMode.AUTO) if estudiantes_perfil else ft.Text("No hay estudiantes censados en este perfil.", color=ft.Colors.GREY_500)
                ])
            )
            content_area.content.controls.append(ft.Container(height=15))
            content_area.content.controls.append(card)

        page.update()

    def handle_estado_change(estudiante_id, nuevo_estado):
        update_estado_inscripcion(estudiante_id, nuevo_estado)
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
                content=ft.Row([ft.Icon(ft.Icons.HOME, color=ft.Colors.BLACK54, size=20), ft.Text("Mis Cursos", size=14, weight=ft.FontWeight.W_500)]),
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
