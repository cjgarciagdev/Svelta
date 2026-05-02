import flet as ft
from config.theme import PAGE_BG
from views.login_view import login_view
from views.register_view import register_view


def main(page: ft.Page):
    page.title = "Inces - Portal de Censo e Inscripción"
    page.window.width = 1000
    page.window.height = 700
    page.window.min_width = 800
    page.window.min_height = 550
    page.window.center()
    page.bgcolor = PAGE_BG
    page.padding = 0
    page.spacing = 0

    def show_login():
        """Muestra la vista de login."""
        page.clean()
        page.add(login_view(page, on_register_click=show_register))

    def show_register():
        """Muestra la vista de registro."""
        page.clean()
        page.add(register_view(page, on_cancel_click=show_login))

    # Mostrar login al iniciar
    show_login()


ft.run(main)
