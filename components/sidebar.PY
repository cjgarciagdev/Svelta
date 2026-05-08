import flet as ft
from config.theme import INCES_TEAL, INCES_BLUE, SIDEBAR_BG

def create_sidebar(user, on_nav_change, on_logout):
    """Componente de barra lateral reutilizable."""
    
    # Función interna para crear botones de menú bonitos
    def nav_button(icon, text, view_name):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.BLACK54, size=20),
                ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87)
            ]),
            padding=ft.padding.symmetric(vertical=12, horizontal=15),
            border_radius=8,
            ink=True, # Efecto de onda al hacer clic
            on_click=lambda _: on_nav_change(view_name),
            # Hover effect (cambia ligeramente de color al pasar el ratón)
            on_hover=lambda e: setattr(e.control, "bgcolor", ft.Colors.BLACK12 if e.data == "true" else ft.Colors.TRANSPARENT) or e.control.update()
        )

    return ft.Container(
        width=250,
        bgcolor=SIDEBAR_BG,
        padding=20,
        border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_300)),
        content=ft.Column(
            expand=True,
            controls=[
                # HEADER DEL SIDEBAR
                ft.Row([
                    ft.Image(src="Logo INCES.png", height=40, fit="contain"),
                    ft.Text("INCES", size=24, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(height=30, color=ft.Colors.GREY_300),
                
                # DATOS DEL USUARIO
                ft.Text("Administrador:", size=11, color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
                ft.Text(f"{user['nombres']} {user['apellidos']}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                
                ft.Container(height=20),
                
                # BOTONES DE NAVEGACIÓN
                nav_button(ft.Icons.PEOPLE_ALT, "Usuarios", "usuarios"),
                nav_button(ft.Icons.LIBRARY_BOOKS, "Perfiles", "cursos"),
                nav_button(ft.Icons.BADGE, "Estudiantes Censados", "estudiantes"),
                
                # ESPACIO FLEXIBLE PARA EMPUJAR EL BOTÓN DE SALIR ABAJO
                ft.Container(expand=True),
                
                # BOTÓN DE CAMBIAR VISTA (Solo para Admins que también son Formadores)
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SWAP_HORIZ, color=ft.Colors.BLUE_600, size=20),
                        ft.Text("Ver como Formador", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)
                    ]),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    border_radius=8,
                    ink=True,
                    # Usamos open para flet moderno o asignamos directamente
                    on_click=lambda e: (setattr(e.page, "snack_bar", ft.SnackBar(ft.Text("🛠️ La vista de Formador se construirá pronto."))), setattr(e.page.snack_bar, "open", True), e.page.update())
                ) if user["role"] == "ADMIN" and user["id"] != 1 else ft.Container(),
                
                # BOTÓN DE SALIR
                ft.Divider(height=20, color=ft.Colors.GREY_300),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400, size=20),
                        ft.Text("Cerrar Sesión", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400)
                    ]),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    border_radius=8,
                    ink=True,
                    on_click=lambda _: on_logout()
                )
            ]
        )
    )
