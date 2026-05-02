import flet as ft
from config.theme import BLUE_PRIMARY, LIGHT_BLUE_BG, LIGHT_BLUE_BORDER, TEXT_BLUE
from components.header import create_header


def login_view(page: ft.Page, on_register_click):
    """Vista principal de Login / Validación."""
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
                    padding=ft.padding.symmetric(vertical=30, horizontal=20),
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                controls=[
                                    ft.Text(
                                        "Portal de Censo e Inscripción",
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK87,
                                    ),
                                    # Tarjeta de Login
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
                                            spacing=20,
                                            controls=[
                                                ft.Text(
                                                    "Login / Validación",
                                                    size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=ft.Colors.BLACK87,
                                                ),
                                                # Caja informativa azul claro
                                                ft.Container(
                                                    bgcolor=LIGHT_BLUE_BG,
                                                    border=ft.border.all(1, LIGHT_BLUE_BORDER),
                                                    border_radius=8,
                                                    padding=12,
                                                    content=ft.Text(
                                                        "Ingrese su Cédula o ID para verificar su estado en el sistema.",
                                                        color=TEXT_BLUE,
                                                        size=13,
                                                    ),
                                                ),
                                                # Campo Cédula
                                                ft.TextField(
                                                    label="Cédula",
                                                    border_color=ft.Colors.GREY_300,
                                                    border_radius=8,
                                                    focused_border_color=BLUE_PRIMARY,
                                                    text_size=14,
                                                ),
                                                # Botón Ingresar
                                                ft.ElevatedButton(
                                                    "Ingresar",
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
                                                ),
                                                ft.Text(
                                                    "¿Aún no tienes cuenta?",
                                                    color=ft.Colors.GREY_600,
                                                    size=14,
                                                ),
                                                # Botón Regístrate
                                                ft.OutlinedButton(
                                                    "Regístrate",
                                                    width=200,
                                                    height=40,
                                                    style=ft.ButtonStyle(
                                                        color=ft.Colors.GREY_700,
                                                        shape=ft.RoundedRectangleBorder(radius=25),
                                                        side=ft.BorderSide(1, ft.Colors.GREY_300),
                                                    ),
                                                    on_click=lambda _: on_register_click(),
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
