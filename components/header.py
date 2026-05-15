import flet as ft
from config.theme import BLUE_PRIMARY


def create_header(on_login_click=None, on_register_click=None):
    """Barra superior azul con logo y menú del INCES."""
    return ft.Container(
        bgcolor=BLUE_PRIMARY,
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Logo
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Container(
                            content=ft.Image(src="Logo INCES.png", height=45, fit="contain", scale=2.8),
                            margin=ft.margin.only(left=30)
                        ),
                    ],
                ),
                # Menú derecho (solo Crear cuenta e Iniciar Sesión)
                ft.Row(
                    spacing=15,
                    controls=[
                        ft.Container(
                            content=ft.Text("Crear cuenta", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                            ink=True,
                            on_click=lambda _: on_register_click() if on_register_click else None,
                            on_hover=lambda e: setattr(e.control.content, "color", ft.Colors.WHITE70 if e.data == "true" else ft.Colors.WHITE) or e.control.update()
                        ),
                        ft.Text("|", color=ft.Colors.WHITE, size=13),
                        ft.Container(
                            content=ft.Text("Iniciar Sesión", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                            ink=True,
                            on_click=lambda _: on_login_click() if on_login_click else None,
                            on_hover=lambda e: setattr(e.control.content, "color", ft.Colors.WHITE70 if e.data == "true" else ft.Colors.WHITE) or e.control.update()
                        ),
                    ],
                ),
            ],
        ),
    )
