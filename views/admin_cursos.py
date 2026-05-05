import flet as ft
from database.db import get_all_perfiles, create_perfil, toggle_perfil_status
from config.theme import INCES_TEAL, INCES_BLUE

def admin_cursos_view(page: ft.Page):
    """Vista de Gestión de Perfiles (Cursos)."""

    cursos_grid = ft.Row(wrap=True, spacing=15, run_spacing=15)

    nombre_field = ft.TextField(
        label="Nombre del nuevo perfil",
        border_color=ft.Colors.GREY_300,
        border_radius=8,
        focused_border_color=INCES_TEAL,
        text_size=14,
        expand=True
    )

    def load_perfiles():
        cursos_grid.controls.clear()
        perfiles = get_all_perfiles()

        for perfil in perfiles:
            is_active = perfil["is_active"]

            if is_active:
                status_text = "Activo"
                status_color = ft.Colors.GREEN_700
                status_bg = ft.Colors.GREEN_100
                btn_icon = ft.Icons.PAUSE_CIRCLE
                btn_tooltip = "Desactivar"
            else:
                status_text = "Inactivo"
                status_color = ft.Colors.RED_700
                status_bg = ft.Colors.RED_100
                btn_icon = ft.Icons.PLAY_CIRCLE
                btn_tooltip = "Reactivar"

            card = ft.Container(
                width=220,
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=20,
                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL, color=INCES_TEAL, size=35),
                        ft.Text(perfil["name"], size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Container(
                            content=ft.Text(status_text, size=12, weight=ft.FontWeight.BOLD, color=status_color),
                            bgcolor=status_bg,
                            padding=ft.padding.symmetric(horizontal=10, vertical=5),
                            border_radius=15
                        ),
                        ft.IconButton(
                            icon=btn_icon,
                            icon_color=status_color,
                            tooltip=btn_tooltip,
                            data={"id": perfil["id"], "new_status": 0 if is_active else 1},
                            on_click=handle_toggle
                        )
                    ]
                )
            )
            cursos_grid.controls.append(card)

        page.update()

    def handle_create(e):
        if not nombre_field.value:
            return
        create_perfil(nombre_field.value.strip())
        nombre_field.value = ""
        load_perfiles()

    def handle_toggle(e):
        perfil_id = e.control.data["id"]
        new_status = e.control.data["new_status"]
        toggle_perfil_status(perfil_id, new_status)
        load_perfiles()

    load_perfiles()

    return ft.Container(
        expand=True,
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIBRARY_BOOKS, color=INCES_TEAL, size=30),
                ft.Text("Gestión de Perfiles", size=24, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
            ]),
            ft.Text("Crea y administra los perfiles (cursos) que ofrece el INCES.", color=ft.Colors.GREY_600),
            ft.Divider(height=20, color=ft.Colors.GREY_300),
            ft.Row([
                nombre_field,
                ft.ElevatedButton(
                    "Crear Perfil",
                    bgcolor=INCES_TEAL,
                    color=ft.Colors.WHITE,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=handle_create
                )
            ]),
            ft.Container(height=10),
            cursos_grid
        ])
    )
