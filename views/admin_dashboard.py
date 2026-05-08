import flet as ft
from components.sidebar import create_sidebar
from views.admin_users import admin_users_view
from views.admin_cursos import admin_cursos_view
from views.admin_estudiantes import admin_estudiantes_view
from views.admin_home import admin_home_view



def admin_dashboard_view(page: ft.Page, user, on_logout):
    """Panel principal del Administrador (Cascarón)."""
    
    # Este es el contenedor gigante a la derecha donde cambiarán las cosas
    content_area = ft.Container(
        expand=True,
        bgcolor=ft.Colors.GREY_50,
        content=ft.Column([
            admin_home_view(page) # Cargamos el dashboard como primera vista!
        ])
    )

    # Función mágica que se activa cuando haces clic en un botón del Sidebar
    def handle_nav_change(view_name):
        content_area.content.controls.clear()
        
        if view_name == "inicio":
            content_area.content.controls.append(admin_home_view(page))
        elif view_name == "usuarios":
            content_area.content.controls.append(admin_users_view(page, user))
        elif view_name == "cursos":
            content_area.content.controls.append(admin_cursos_view(page))
        elif view_name == "estudiantes":
            content_area.content = admin_estudiantes_view(page)
            
        content_area.update()


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

        
        