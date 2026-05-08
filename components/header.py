import flet as ft
from config.theme import BLUE_PRIMARY


def create_header():
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
                # Menú derecho
                ft.Row(
                    spacing=15,
                    controls=[
                        ft.Text("Inicio", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                        ft.Text("|", color=ft.Colors.WHITE, size=13),
                        ft.Text("Formaciones", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=20,
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            content=ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Text("¿Qué te gustaría estudiar?", color=ft.Colors.GREY_500, size=12),
                                    ft.Icon(ft.Icons.SEARCH, color=BLUE_PRIMARY, size=16),
                                ],
                            ),
                        ),
                        ft.Text("Crear cuenta", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                        ft.Text("|", color=ft.Colors.WHITE, size=13),
                        ft.Text("Iniciar Sesión", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                    ],
                ),
            ],
        ),
    )
