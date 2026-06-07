import flet as ft
from database.db import get_all_users, update_user_status, update_user_role, delete_user, get_all_perfiles, assign_perfil_to_formador, remove_perfil_from_formador, get_perfiles_by_formador, get_entidades_disponibles
from config.theme import INCES_TEAL, INCES_BLUE

def admin_users_view(page: ft.Page, current_user):
    """Vista de Gestión de Usuarios (Aprobación de Formadores)."""
    
    # Esta es la tabla que mostrará los datos
    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cédula", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombres", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Apellidos", weight=ft.FontWeight.BOLD)),
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
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                border_radius=15
            )

            # Botones de acción (Por defecto mostramos Aprobar/Rechazar y Hacer Admin)
            acciones_lista = []
            
            if user["role"] == "FORMADOR":
                if dict(current_user).get("was_formador", 0) == 0:
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
                        ),
                        ft.IconButton(
                            icon=ft.Icons.MENU_BOOK,
                            icon_color=ft.Colors.BLUE_400,
                            tooltip="Asignar Perfiles",
                            data={"id": user["id"]},
                            on_click=lambda e: open_assign_dialog(e.control.data["id"])
                        ),
                    ])
            elif user["role"] == "ADMIN":
                # Solo el admin principal puede degradar (y no puede degradarse a sí mismo)
                if user["id"] != 1 and dict(current_user).get("was_formador", 0) == 0:
                    acciones_lista.append(
                        ft.IconButton(
                            icon=ft.Icons.REMOVE_MODERATOR, 
                            icon_color=ft.Colors.RED_400, 
                            tooltip="Quitar permisos de Admin",
                            data={"id": user["id"], "role": "FORMADOR"},
                            on_click=handle_role_change
                        )
                    )
            
            # Botón de eliminar (disponible para todos menos el admin principal)
            if user["id"] != 1 and dict(current_user).get("was_formador", 0) == 0:
                acciones_lista.append(
                    ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_OUTLINED, 
                        icon_color=ft.Colors.RED_400,
                        tooltip="Eliminar Usuario",
                        data={"id": user["id"]},
                        on_click=lambda e: open_delete_dialog(e.control.data["id"])
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
                        ft.DataCell(ft.Text(user["cedula"])),
                        ft.DataCell(ft.Text(user["nombres"])),
                        ft.DataCell(ft.Text(user["apellidos"])),
                        ft.DataCell(ft.Text(dict(user).get("correo") or dict(user).get("email", ""))),
                        ft.DataCell(ft.Container(
                            content=ft.Text(
                                "FORMADOR/ADMIN" if (user["role"] == "ADMIN" and dict(user).get("was_formador", 0) == 1) else user["role"],
                                size=12, weight=ft.FontWeight.BOLD,
                                color=INCES_TEAL if user["role"] == "ADMIN" else ft.Colors.BLACK87
                            ),
                            bgcolor=ft.Colors.TEAL_50 if user["role"] == "ADMIN" else ft.Colors.TRANSPARENT,
                            padding=ft.padding.Padding(left=8, top=4, right=8, bottom=4),
                            border_radius=10
                        )),
                        ft.DataCell(estado_chip),
                        ft.DataCell(acciones),
                    ]
                )
            )
        
        page.update()

    def open_delete_dialog(user_id):
        """Muestra un diálogo de confirmación antes de eliminar."""
        def confirm_delete(e):
            delete_user(user_id)
            dlg.open = False
            page.update()
            load_users()

        def close_dlg(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar permanentemente a este usuario? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.ElevatedButton("Eliminar", bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=confirm_delete),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def open_assign_dialog(user_id):
        """Muestra un diálogo para asignar/quitar perfiles a un formador con Entidad opcional."""
        
        perfiles_dropdown = ft.Dropdown(
            label="Perfil",
            options=[ft.dropdown.Option(str(p["id"]), p["name"]) for p in get_all_perfiles() if p["is_active"]],
            width=250,
            text_size=13
        )

        # Cargar entidades únicas desde la BD
        entidades_disponibles = get_entidades_disponibles()
        entidad_options = [ft.dropdown.Option("", "CFS")] + [
            ft.dropdown.Option(e, e) for e in entidades_disponibles
        ]
        entidad_dropdown = ft.Dropdown(
            label="Ámbito",
            hint_text="CFS",
            options=entidad_options,
            value="",
            width=220,
            text_size=13
        )
        
        lista_asignados = ft.Column(scroll=ft.ScrollMode.AUTO, height=200)

        def render_asignados():
            lista_asignados.controls.clear()
            asignados = get_perfiles_by_formador(user_id)
            if not asignados:
                lista_asignados.controls.append(ft.Text("No tiene perfiles asignados.", color=ft.Colors.GREY_500))
            else:
                for p in asignados:
                    p_dict = dict(p)
                    ent_val = p_dict.get("entidad", "")
                    entidad_str = f" [{ent_val}]" if ent_val else " [CFS]"
                    lista_asignados.controls.append(
                        ft.Row([
                            ft.Icon(ft.Icons.SCHOOL, size=16, color=INCES_TEAL),
                            ft.Text(f"{p['name']}{entidad_str}", size=13, weight=ft.FontWeight.W_500, expand=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Quitar",
                                data={"perfil_id": p["id"], "entidad": ent_val},
                                on_click=lambda e: remove_and_refresh(e.control.data)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
            # No llamamos a page.update() aquí, lo dejamos a las funciones que llaman a render_asignados()

        def remove_and_refresh(data):
            remove_perfil_from_formador(user_id, data["perfil_id"], data["entidad"])
            render_asignados()
            page.update()

        def add_assignment(e):
            if not perfiles_dropdown.value:
                return
            perfil_id = int(perfiles_dropdown.value)
            entidad = (entidad_dropdown.value or "").strip()
            
            success = assign_perfil_to_formador(user_id, perfil_id, entidad)
            if success:
                entidad_dropdown.value = ""
                render_asignados()
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Esa combinación ya está asignada"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()

        def close_dlg(e):
            dlg.open = False
            page.update()
        
        add_btn = ft.ElevatedButton("Agregar", icon=ft.Icons.ADD, bgcolor=INCES_TEAL, color=ft.Colors.WHITE, on_click=add_assignment)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Asignar Permisos al Formador"),
            content=ft.Container(
                width=600,
                content=ft.Column([
                    ft.Text("Agrega un perfil y opcionalmente especifica una entidad para limitar su acceso.", size=12, color=ft.Colors.GREY_600),
                    ft.Row([perfiles_dropdown, entidad_dropdown, add_btn], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(height=20, color=ft.Colors.GREY_300),
                    ft.Text("Permisos Actuales:", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=lista_asignados,
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        border_radius=8,
                        padding=10
                    )
                ], tight=True)
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dlg),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        render_asignados()
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
