import flet as ft
from config.theme import INCES_BLUE


# ─── Tooltip de información ⓘ (activación por clic) ──────────────────────────
def info_tooltip(mensaje: str, titulo: str = "Detalles de la Cifra") -> ft.Control:
    """Ícono ⓘ azul que abre un diálogo de información sobre todo el sistema."""
    
    def close_dlg(e):
        dialog.open = False
        if dialog.page:
            dialog.page.update()

    dialog = ft.AlertDialog(
        title=ft.Text(titulo, weight=ft.FontWeight.BOLD, color="#2A579A", size=16),
        content=ft.Container(
            content=ft.Text(mensaje, size=13, color=ft.Colors.BLACK87),
            width=350,
            padding=10
        ),
        actions=[
            ft.TextButton("Entendido", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=8),
    )

    def on_click(e):
        page = e.control.page
        if dialog not in page.overlay:
            page.overlay.append(dialog)
        dialog.open = True
        page.update()

    icon_container = ft.Container(
        content=ft.Icon(
            ft.Icons.INFO_OUTLINE,
            size=16,
            color=ft.Colors.BLUE_400,
        ),
        padding=6,
        border_radius=14,
        on_click=on_click,
        tooltip="Haz clic para ver más detalles",
    )

    return icon_container


# ─── Panel flotante "User Help & Resources" ─────────────────────────────────
def help_menu(page: ft.Page) -> ft.Control:
    """
    Botón ❓ con panel desplegable de ayuda que flota sobre el contenido.
    Compatible con Flet 0.85.x — usa page.overlay para que el panel no sea
    recortado por ningún contenedor padre.
    """

    # ── Opciones del menú ────────────────────────────────────────────────────
    opciones = [
        (ft.Icons.TOUR_OUTLINED,       "Tour de Bienvenida (Iniciar)"),
        (ft.Icons.MENU_BOOK_OUTLINED,  "Guías y Documentación"),
        (ft.Icons.HELP_OUTLINE,        "Preguntas Frecuentes"),
        (ft.Icons.CHAT_OUTLINED,       "Contactar Soporte (Ticket/Chat)"),
        (ft.Icons.BUG_REPORT_OUTLINED, "Reportar un Error"),
    ]

    # ── Estado ───────────────────────────────────────────────────────────────
    panel_open = [False]

    # ── Ítems del panel ──────────────────────────────────────────────────────
    def _make_item(icono, label):
        item = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icono, size=16, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=13, color=ft.Colors.BLACK87),
                ],
                spacing=10,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=6,
            bgcolor=ft.Colors.WHITE,
            ink=True,
            on_click=lambda e: close_panel(),
        )

        def _on_hover(e):
            item.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE
            item.update()

        item.on_hover = _on_hover
        return item

    items = [_make_item(icono, label) for icono, label in opciones]

    # ── Panel flotante (se mete en page.overlay) ─────────────────────────────
    panel = ft.Container(
        visible=False,
        bgcolor=ft.Colors.WHITE,
        border_radius=8,
        border=ft.border.Border.all(1, ft.Colors.BLACK12),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color="#1F000000",
            offset=ft.Offset(0, 4),
        ),
        padding=ft.Padding.symmetric(vertical=6),
        width=280,
        right=10,
        top=54,   # debajo de la AppBar (48 px) + margen
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "User Help & Resources",
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.BLACK54,
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                ),
                ft.Divider(height=1, color=ft.Colors.BLACK12),
                *items,
            ],
            spacing=0,
            tight=True,
        ),
    )

    # ── Funciones de apertura/cierre ─────────────────────────────────────────
    def open_panel():
        if panel not in page.overlay:
            page.overlay.append(panel)
        panel.visible = True
        panel_open[0] = True
        page.update()

    def close_panel():
        panel.visible = False
        panel_open[0] = False
        page.update()

    def toggle_panel(e):
        if panel_open[0]:
            close_panel()
        else:
            open_panel()

    # ── Botón de ayuda ───────────────────────────────────────────────────────
    btn_ayuda = ft.IconButton(
        icon=ft.Icons.HELP_OUTLINE,
        icon_color=ft.Colors.WHITE,
        icon_size=20,
        tooltip="Ayuda",
        on_click=toggle_panel,
    )

    return btn_ayuda
