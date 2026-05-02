import flet as ft
from config.theme import BLUE_PRIMARY
from components.header import create_header


def register_view(page: ft.Page, on_cancel_click):
    """Vista de Registro / Crear Nueva Cuenta."""
    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            create_header(),
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.ListView(
                    expand=True,
                    padding=ft.padding.symmetric(vertical=20, horizontal=20),
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                                controls=[
                                    ft.Text(
                                        "Crear Nueva Cuenta",
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK87,
                                    ),
                                    # Tarjeta de Registro
                                    ft.Container(
                                        width=500,
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=12,
                                        padding=35,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=15,
                                            color=ft.Colors.BLACK12,
                                            offset=ft.Offset(0, 4),
                                        ),
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=18,
                                            controls=[
                                                ft.Text(
                                                    "Datos del Usuario",
                                                    size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=ft.Colors.BLACK87,
                                                ),
                                                ft.TextField(
                                                    label="Nombre Completo",
                                                    border_color=ft.Colors.GREY_300,
                                                    border_radius=8,
                                                    focused_border_color=BLUE_PRIMARY,
                                                    text_size=14,
                                                ),
                                                ft.TextField(
                                                    label="Cédula",
                                                    border_color=ft.Colors.GREY_300,
                                                    border_radius=8,
                                                    focused_border_color=BLUE_PRIMARY,
                                                    text_size=14,
                                                ),
                                                ft.TextField(
                                                    label="Correo Electrónico",
                                                    border_color=ft.Colors.GREY_300,
                                                    border_radius=8,
                                                    focused_border_color=BLUE_PRIMARY,
                                                    text_size=14,
                                                ),
                                                ft.TextField(
                                                    label="Contraseña",
                                                    password=True,
                                                    can_reveal_password=True,
                                                    border_color=ft.Colors.GREY_300,
                                                    border_radius=8,
                                                    focused_border_color=BLUE_PRIMARY,
                                                    text_size=14,
                                                ),
                                                ft.Container(height=5),
                                                # Botón Completar Registro
                                                ft.ElevatedButton(
                                                    "Completar Registro",
                                                    bgcolor=BLUE_PRIMARY,
                                                    color=ft.Colors.WHITE,
                                                    width=430,
                                                    height=45,
                                                    style=ft.ButtonStyle(
                                                        shape=ft.RoundedRectangleBorder(radius=25),
                                                        text_style=ft.TextStyle(
                                                            size=15, weight=ft.FontWeight.BOLD
                                                        ),
                                                    ),
                                                    on_click=lambda _: on_cancel_click(),
                                                ),
                                                ft.Container(height=5),
                                                # Botón Cancelar / Volver
                                                ft.OutlinedButton(
                                                    "Cancelar / Volver",
                                                    width=200,
                                                    height=40,
                                                    style=ft.ButtonStyle(
                                                        color=ft.Colors.GREY_700,
                                                        shape=ft.RoundedRectangleBorder(radius=25),
                                                        side=ft.BorderSide(1, ft.Colors.GREY_300),
                                                    ),
                                                    on_click=lambda _: on_cancel_click(),
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
