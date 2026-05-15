import flet as ft
from config.theme import PAGE_BG
from views.login_view import login_view
from views.register_view import register_view
from database.db import init_db
from views.formador_dashboard import formador_dashboard_view
from views.admin_dashboard import admin_dashboard_view

def main(page: ft.Page):
    # Inicializar base de datos
    init_db()

    page.title = "Inces - Portal de Censo e Inscripción"
    page.window.width = 1000
    page.window.height = 700
    page.window.min_width = 800
    page.window.min_height = 550
    
    # Configurar ventana para el splash screen
    page.window.frameless = True
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.spacing = 0

    def on_login_success(user):
        """Se ejecuta cuando el login es correcto."""
        page.clean()
        if user["role"] == "ADMIN":
            page.add(admin_dashboard_view(page, user, on_logout=show_login))
        else:
            page.add(formador_dashboard_view(page, user, on_logout=show_login))

    def show_login():
        """Muestra la vista de login."""
        page.clean()
        page.add(login_view(page, on_register_click=show_register, on_login_success=on_login_success))

    def show_register():
        """Muestra la vista de registro."""
        page.clean()
        page.add(register_view(page, on_cancel_click=show_login))

    def show_splash():
        """Muestra una pantalla de carga (Splash Screen) con el logo."""
        page.clean()
        logo = ft.Image(src="Logo INCES.png", height=150, fit="contain", opacity=0, animate_opacity=1000)
        page.add(
            ft.Container(
                content=logo,
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        )
        
        def animate():
            import time
            # Animación de parpadeo (fade in / fade out)
            time.sleep(0.2)
            logo.opacity = 1
            page.update()
            time.sleep(1.5)
            logo.opacity = 0
            page.update()
            time.sleep(1.0)
            
            # Restaurar ventana para la app
            page.window.frameless = False
            page.window.bgcolor = ft.Colors.WHITE
            page.bgcolor = PAGE_BG
            page.update()
            
            # Terminar splash y mostrar login
            show_login()

        import threading
        threading.Thread(target=animate, daemon=True).start()

    # Mostrar splash al iniciar
    show_splash()

ft.app(target=main, assets_dir=".")
