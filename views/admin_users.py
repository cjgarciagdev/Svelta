import flet as ft
from database.db import get_all_users, update_user_status, update_user_role
from config.theme import INCES_TEAL, INCES_BLUE

def admin_users_view(page: ft.Page, current_user):
    """Vista de Gestión de Usuarios (Aprobación de Formadores)."""
    
    # Esta es la tabla que mostrará los datos
    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Correo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Rol", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def load_users():
        """Obtiene los usuarios de la BD y llena la tabla."""
        users_table.rows.clear()
        users = get_all_users()
        
        for user in users:
            # Creamos el diseño del estado (Chip)
            if user["status"] == "PENDING":
                text_color = ft.Colors.ORANGE_700
                bg_color = ft.Colors.ORANGE_100
                status_text = "PENDIENTE"
            elif user["status"] == "APPROVED":
                text_color = ft.Colors.GREEN_700
                bg_color = ft.Colors.GREEN_100
                status_text = "APROBADO"
            else:
                text_color = ft.Colors.RED_700
                bg_color = ft.Colors.RED_100
                status_text = "RECHAZADO"
            
            estado_chip = ft.Container(
                content=ft.Text(status_text, size=12, weight=ft.FontWeight.BOLD, color=text_color),
                bgcolor=bg_color,
                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                border_radius=15
            )

            # Botones de acción (Por defecto mostramos Aprobar/Rechazar y Hacer Admin)
            acciones_lista = []
            
            if user["role"] == "FORMADOR":
                acciones_lista.extend([
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE, 
                        icon_color=ft.Colors.GREEN_500, 
                        tooltip="Aprobar",
                        data={"id": user["id"], "status": "APPROVED"},
                        on_click=handle_status_change
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CANCEL, 
                        icon_color=ft.Colors.RED_500, 
                        tooltip="Rechazar",
                        data={"id": user["id"], "status": "REJECTED"},
                        on_click=handle_status_change
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ADMIN_PANEL_SETTINGS, 
                        icon_color=INCES_TEAL, 
                        tooltip="Hacer Administrador",
                        data={"id": user["id"], "role": "ADMIN"},
                        on_click=handle_role_change
                    )
                ])
            elif user["role"] == "ADMIN":
                acciones_lista.append(
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_MODERATOR, 
                        icon_color=ft.Colors.RED_400, 
                        tooltip="Quitar permisos de Admin",
                        data={"id": user["id"], "role": "FORMADOR"},
                        on_click=handle_role_change
                    )
                )

            acciones = ft.Row(acciones_lista)

            # Evitar que el usuario actual se modifique a sí mismo
            if user["id"] == current_user["id"]:
                acciones = ft.Text("") # Texto vacío visible en lugar de botones

            users_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(user["id"]))),
                        ft.DataCell(ft.Text(user["full_name"])),
                        ft.DataCell(ft.Text(user["email"])),
                        ft.DataCell(ft.Text(user["role"])),
                        ft.DataCell(estado_chip),
                        ft.DataCell(acciones),
                    ]
                )
            )
        
        page.update()

    def handle_status_change(e):
        """Maneja el clic en los botones de Aprobar/Rechazar."""
        user_id = e.control.data["id"]
        new_status = e.control.data["status"]
        
        # Actualizamos en BD
        update_user_status(user_id, new_status)
        
        # Recargamos la tabla
        load_users()
        
    def handle_role_change(e):
        """Maneja el clic en el botón de Hacer Administrador."""
        user_id = e.control.data["id"]
        new_role = e.control.data["role"]
        
        # Actualizamos en BD (Opcionalmente podríamos cambiar el status a APPROVED también)
        update_user_role(user_id, new_role)
        update_user_status(user_id, "APPROVED") # Un admin siempre debe estar aprobado
        
        # Recargamos la tabla
        load_users()

    # Cargar los datos la primera vez
    load_users()

    # Retornamos el contenedor con la vista armada
    return ft.Container(
        expand=True,
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PEOPLE_ALT, color=INCES_TEAL, size=30),
                ft.Text("Gestión de Formadores", size=24, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
            ]),
            ft.Text("Aprueba o rechaza a los formadores que se han registrado en el sistema.", color=ft.Colors.GREY_600),
            ft.Divider(height=30, color=ft.Colors.GREY_300),
            
            # Usamos Row con scroll=auto por si la tabla es muy ancha
            ft.Row([users_table], scroll=ft.ScrollMode.AUTO)
        ])
    )
