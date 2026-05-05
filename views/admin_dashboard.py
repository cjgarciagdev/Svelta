import flet as ft
from components.sidebar import create_sidebar
from views.admin_users import admin_users_view

def admin_dashboard_view(page: ft.Page, user, on_logout):
    """Panel principal del Administrador (Cascarón)."""
    
    # Este es el contenedor gigante a la derecha donde cambiarán las cosas
    content_area = ft.Container(
        expand=True,
        padding=30,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column([
            ft.Text("Bienvenido al Panel de Control", size=24, weight=ft.FontWeight.BOLD),
        ])
    )

    # Función mágica que se activa cuando haces clic en un botón del Sidebar
    def handle_nav_change(view_name):
        content_area.content.controls.clear()
        
        if view_name == "usuarios":
            content_area.content.controls.append(admin_users_view(page, user))
        elif view_name == "cursos":
            content_area.content.controls.append(ft.Container())
        elif view_name == "estudiantes":
            content_area.content.controls.append(ft.Container())
            
        page.update()

    # Retornamos una Fila: A la izquierda el Sidebar, a la derecha el Área de Contenido
    return ft.Row(
        expand=True,
        spacing=0,
        controls=[
            # 1. Nuestro nuevo menú lateral
            create_sidebar(user=user, on_nav_change=handle_nav_change, on_logout=on_logout),
            
            # 2. El área dinámica
            content_area
        ]
    )
