import flet as ft
import hashlib
from config.theme import INCES_TEAL, INCES_BLUE, PAGE_BG
from components.header import create_header
from database.db import create_user, count_users


def register_view(page: ft.Page, on_cancel_click):
    """Vista de Registro / Crear Nueva Cuenta."""

    # 1. Creamos las variables para atrapar los datos
    name_field = ft.TextField(label="Nombre Completo", border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    cedula_field = ft.TextField(label="Cédula", border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    email_field = ft.TextField(label="Correo Electrónico", border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)

    # 2. Función que se ejecuta al darle al botón
    def handle_register(e):
        # Validar que no estén vacíos
        if not name_field.value or not email_field.value or not password_field.value or not cedula_field.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor completa todos los campos."), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return

        # Encriptar contraseña
        hashed_pw = hashlib.sha256(password_field.value.encode()).hexdigest()

        # Si es el primer usuario, lo hacemos ADMIN aprobado. Si no, Formador pendiente.
        is_first = (count_users() == 0)
        role = "ADMIN" if is_first else "FORMADOR"
        status = "APPROVED" if is_first else "PENDING"

        # Guardar en base de datos
        success = create_user(name_field.value, email_field.value, hashed_pw, role, status)

        if success:
            msg = "¡Admin creado con éxito!" if is_first else "¡Registro exitoso! Espera la aprobación de un Admin."
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN_700)
            page.snack_bar.open = True
            page.update()
            on_cancel_click()  # Regresar al login
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error: El correo ya está registrado."), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()

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
                                    ft.Text("Crear Nueva Cuenta", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                                    ft.Container(
                                        width=500,
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=12,
                                        padding=35,
                                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)),
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=18,
                                            controls=[
                                                ft.Text("Datos del Usuario", size=22, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87),
                                                
                                                # Pasamos las variables a la vista
                                                name_field,
                                                cedula_field,
                                                email_field,
                                                password_field,
                                                
                                                ft.Container(height=5),
                                                ft.ElevatedButton(
                                                    "Completar Registro",
                                                    bgcolor=INCES_TEAL,
                                                    color=ft.Colors.WHITE,
                                                    width=430,
                                                    height=45,
                                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25), text_style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD)),
                                                    on_click=handle_register, # Llamamos a nuestra nueva función
                                                ),
                                                ft.Container(height=5),
                                                ft.OutlinedButton(
                                                    "Cancelar / Volver",
                                                    width=200,
                                                    height=40,
                                                    style=ft.ButtonStyle(color=ft.Colors.GREY_700, shape=ft.RoundedRectangleBorder(radius=25), side=ft.BorderSide(1, ft.Colors.GREY_300)),
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
