import flet as ft
import hashlib
from config.theme import INCES_TEAL, INCES_BLUE, PAGE_BG
from components.header import create_header
from database.db import create_user, count_users


def register_view(page: ft.Page, on_cancel_click):
    """Vista de Registro / Crear Nueva Cuenta."""

    # Campos del formulario
    name_field     = ft.TextField(label="Nombres",            border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    apellido_field = ft.TextField(label="Apellidos",          border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    cedula_field   = ft.TextField(label="Cédula",             border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    email_field    = ft.TextField(label="Correo Electrónico", border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)

    # Textos de error inline — uno por campo
    err_nombres   = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
    err_apellidos = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
    err_cedula    = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
    err_email     = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
    err_password  = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
    err_general   = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)

    def limpiar_errores():
        for err in [err_nombres, err_apellidos, err_cedula, err_email, err_password, err_general]:
            err.visible = False
            err.value = ""

    def mostrar_error(campo_err, msg):
        campo_err.value = f"⚠️ {msg}"
        campo_err.visible = True

    def handle_register(e):
        limpiar_errores()
        hay_error = False

        # 1. Campos vacíos
        if not name_field.value:
            mostrar_error(err_nombres, "Ingresa tus nombres.")
            hay_error = True
        if not apellido_field.value:
            mostrar_error(err_apellidos, "Ingresa tus apellidos.")
            hay_error = True
        if not cedula_field.value:
            mostrar_error(err_cedula, "Ingresa tu cédula.")
            hay_error = True
        if not email_field.value:
            mostrar_error(err_email, "Ingresa tu correo.")
            hay_error = True
        if not password_field.value:
            mostrar_error(err_password, "Ingresa una contraseña.")
            hay_error = True

        if hay_error:
            page.update()
            return

        # 2. Cédula solo números
        if not cedula_field.value.strip().isdigit():
            mostrar_error(err_cedula, "La cédula debe contener solo números.")
            page.update()
            return

        # 3. Formato de correo
        email = email_field.value.strip()
        if "@" not in email or "." not in email.split("@")[-1]:
            mostrar_error(err_email, "Ingresa un correo válido (ej: nombre@correo.com).")
            page.update()
            return

        # 4. Contraseña mínimo 6 caracteres
        if len(password_field.value) < 6:
            mostrar_error(err_password, "La contraseña debe tener al menos 6 caracteres.")
            page.update()
            return

        # Todo OK — crear usuario
        hashed_pw = hashlib.sha256(password_field.value.encode()).hexdigest()
        is_first = (count_users() == 0)
        role   = "ADMIN"    if is_first else "FORMADOR"
        status = "APPROVED" if is_first else "PENDING"

        success = create_user(name_field.value, apellido_field.value, cedula_field.value, email, hashed_pw, role, status)

        if success:
            sb = ft.SnackBar(ft.Text("¡Registro exitoso! Espera la aprobación del Admin." if not is_first else "¡Admin creado!"), bgcolor=ft.Colors.GREEN_700)
            page.overlay.append(sb)
            sb.open = True
            page.update()
            on_cancel_click()
        else:
            mostrar_error(err_email, "Este correo ya está registrado.")
            page.update()

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            create_header(on_login_click=on_cancel_click),
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
                                            spacing=10,
                                            controls=[
                                                ft.Text("Datos del Usuario", size=22, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87),

                                                ft.Row([ft.Container(name_field, expand=1), ft.Container(apellido_field, expand=1)]),
                                                ft.Row([ft.Container(err_nombres, expand=1), ft.Container(err_apellidos, expand=1)]),

                                                cedula_field,
                                                err_cedula,

                                                email_field,
                                                err_email,

                                                password_field,
                                                err_password,

                                                err_general,

                                                ft.Container(height=5),
                                                ft.ElevatedButton(
                                                    "Completar Registro",
                                                    bgcolor=INCES_TEAL,
                                                    color=ft.Colors.WHITE,
                                                    width=430,
                                                    height=45,
                                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25), text_style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD)),
                                                    on_click=handle_register,
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



