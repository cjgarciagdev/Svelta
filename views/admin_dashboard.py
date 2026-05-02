import flet as ft
from config.theme import BLUE_PRIMARY

def admin_dashboard_view(page: ft.Page, user, on_logout):
    """Panel principal del Administrador."""
    
    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                padding=20,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"Panel de Administrador - Hola, {user['full_name']}", size=20, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Cerrar Sesión", on_click=lambda _: on_logout(), bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE)
                    ]
                )
            ),
            ft.Container(
                padding=20,
                content=ft.Text("Aquí construiremos las tablas de usuarios y estudiantes.", size=16)
            )
        ]
    )
