import flet as ft
import hashlib
import bcrypt
import secrets
from config.theme import INCES_TEAL, INCES_BLUE, LIGHT_BLUE_BG, LIGHT_BLUE_BORDER, TEXT_BLUE
from components.header import create_header
from database.db import get_user_by_email, update_user_password
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
            
        hashed_pw_attempt = password_field.value.encode()
        stored_hash = user["password_hash"]
        
        is_valid = False
        if stored_hash.startswith("$2b$"):
            is_valid = bcrypt.checkpw(hashed_pw_attempt, stored_hash.encode())
        else:
            is_valid = (stored_hash == hashlib.sha256(hashed_pw_attempt).hexdigest())
            if is_valid:
                # Migración silenciosa
                new_bcrypt_hash = bcrypt.hashpw(hashed_pw_attempt, bcrypt.gensalt()).decode()
                update_user_password(user["id"], new_bcrypt_hash)
        
        if not is_valid:
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
        error_text.value = f"¡Bienvenido {user['nombres']}! Entrando..."
        error_text.color = ft.Colors.GREEN_700
        error_text.visible = True
        page.update()
        
        # Pausa pequeñita para que se vea el mensaje y hacemos el cambio de pantalla
        time.sleep(1)
        on_login_success(user)

    def open_recovery_dialog(e):
        state = {"email": "", "code": "", "step": 1}
        
        email_rec_field = ft.TextField(label="Correo Electrónico", text_size=13, width=300)
        code_rec_field = ft.TextField(label="Código de 6 dígitos", text_size=13, width=300, visible=False)
        new_pw_rec_field = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, text_size=13, width=300, visible=False)
        err_rec = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
        instrucciones_text = ft.Text("Ingresa tu correo registrado para enviarte un código.", size=13)
        
        btn_action = ft.ElevatedButton("Enviar Código", bgcolor=INCES_TEAL, color=ft.Colors.WHITE)

        def close_dlg(e):
            dialog.open = False
            page.update()

        def handle_action(e):
            err_rec.visible = False
            page.update()
            
            if state["step"] == 1:
                if not email_rec_field.value:
                    err_rec.value = "Ingresa tu correo."
                    err_rec.visible = True
                    page.update()
                    return
                user = get_user_by_email(email_rec_field.value)
                if not user:
                    err_rec.value = "No hay ningún usuario con ese correo."
                    err_rec.visible = True
                    page.update()
                    return
                
                state["email"] = email_rec_field.value
                state["code"] = "".join(str(secrets.choice(range(10))) for _ in range(6))
                
                btn_action.disabled = True
                btn_action.text = "Enviando..."
                page.update()
                
                from utils.email_sender import send_recovery_code
                enviado = send_recovery_code(state["email"], state["code"])
                
                btn_action.disabled = False
                if enviado:
                    state["step"] = 2
                    instrucciones_text.value = f"Hemos enviado un código a {state['email']}."
                    email_rec_field.visible = False
                    code_rec_field.visible = True
                    btn_action.text = "Verificar Código"
                else:
                    btn_action.text = "Enviar Código"
                    err_rec.value = "Error al enviar correo. Verifica la configuración."
                    err_rec.visible = True
                page.update()
                
            elif state["step"] == 2:
                if code_rec_field.value.strip() != state["code"]:
                    err_rec.value = "Código incorrecto."
                    err_rec.visible = True
                    page.update()
                    return
                
                state["step"] = 3
                instrucciones_text.value = "Código verificado. Ingresa tu nueva contraseña."
                code_rec_field.visible = False
                new_pw_rec_field.visible = True
                btn_action.text = "Guardar Contraseña"
                page.update()
                
            elif state["step"] == 3:
                if len(new_pw_rec_field.value) < 6:
                    err_rec.value = "La contraseña debe tener al menos 6 caracteres."
                    err_rec.visible = True
                    page.update()
                    return
                    
                user = get_user_by_email(state["email"])
                hashed_pw = bcrypt.hashpw(new_pw_rec_field.value.encode(), bcrypt.gensalt()).decode()
                update_user_password(user["id"], hashed_pw)
                
                dialog.open = False
                page.snack_bar = ft.SnackBar(ft.Text("¡Contraseña actualizada con éxito!"), bgcolor=ft.Colors.GREEN_700)
                page.snack_bar.open = True
                page.update()

        btn_action.on_click = handle_action

        dialog = ft.AlertDialog(
            title=ft.Text("Recuperar Contraseña", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                instrucciones_text,
                email_rec_field,
                code_rec_field,
                new_pw_rec_field,
                err_rec
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                btn_action
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            create_header(on_register_click=on_register_click),
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.ListView(
                    expand=True,
                    padding=ft.Padding.symmetric(vertical=30, horizontal=20),
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                controls=[
                                    ft.Text("Censo Inces", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
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
                                                ft.TextButton(
                                                    "¿Olvidaste tu contraseña?", 
                                                    style=ft.ButtonStyle(color=ft.Colors.BLUE_600),
                                                    on_click=open_recovery_dialog
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
