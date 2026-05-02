import flet as ft
import hashlib
from config.theme import INCES_TEAL, INCES_BLUE, LIGHT_BLUE_BG, LIGHT_BLUE_BORDER, TEXT_BLUE
from components.header import create_header
from database.db import get_user_by_email
import time

def login_view(page: ft.Page, on_register_click, on_login_success):
    """Vista principal de Login para Admins y Formadores."""

    email_field = ft.TextField(label="Correo Electrónico", border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_color=ft.Colors.GREY_300, border_radius=8, focused_border_color=INCES_TEAL, text_size=14)
    error_text = ft.Text("", color=ft.Colors.RED_700, size=13, visible=False)

    def handle_login(e):
        error_text.visible = False
        
        if not email_field.value or not password_field.value:
            error_text.value = "Ingresa tu correo y contraseña."
            error_text.visible = True
            page.update()
            return
            
        user = get_user_by_email(email_field.value)
        
        if not user:
            error_text.value = "Usuario no encontrado."
            error_text.visible = True
            page.update()
            return
            
        hashed_pw = hashlib.sha256(password_field.value.encode()).hexdigest()
        
        if user["password_hash"] != hashed_pw:
            error_text.value = "Contraseña incorrecta."
            error_text.visible = True
            page.update()
            return
            
        if user["status"] == "PENDING":
            error_text.value = "Tu cuenta está en espera de aprobación."
            error_text.color = ft.Colors.ORANGE_700
            error_text.visible = True
            page.update()
            return
            
        if user["status"] == "REJECTED":
            error_text.value = "Tu solicitud de cuenta fue rechazada."
            error_text.visible = True
            page.update()
            return
            
        # ¡Login Exitoso!
        error_text.value = f"¡Bienvenido {user['full_name']}! Entrando..."
        error_text.color = ft.Colors.GREEN_700
        error_text.visible = True
        page.update()
        
        # Pausa pequeñita para que se vea el mensaje y hacemos el cambio de pantalla
        time.sleep(1)
        on_login_success(user)

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
                                    ft.Text("Portal de Censo e Inscripción", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                                    ft.Container(
                                        width=500,
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=12,
                                        padding=35,
                                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)),
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                ft.Text("Acceso al Sistema", size=22, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87),
                                                email_field,
                                                password_field,
                                                error_text,
                                                ft.ElevatedButton(
                                                    "Ingresar",
                                                    bgcolor=INCES_TEAL,
                                                    color=ft.Colors.WHITE,
                                                    width=430,
                                                    height=45,
                                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25), text_style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD)),
                                                    on_click=handle_login
                                                ),
                                                ft.Text("¿Aún no eres formador?", color=ft.Colors.GREY_600, size=14),
                                                ft.OutlinedButton(
                                                    "Solicitar Acceso",
                                                    width=200,
                                                    height=40,
                                                    style=ft.ButtonStyle(color=ft.Colors.GREY_700, shape=ft.RoundedRectangleBorder(radius=25), side=ft.BorderSide(1, ft.Colors.GREY_300)),
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
