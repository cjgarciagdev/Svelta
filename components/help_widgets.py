import flet as ft
from config.theme import INCES_BLUE


# ─── Tooltip de información ⓘ (activación por clic) ──────────────────────────
def info_tooltip(mensaje: str, titulo: str = "Detalles de la Cifra") -> ft.Control:
    """
    Ícono ⓘ azul con tooltip customizado activado por clic.
    - Clic en el ícono → muestra/oculta el panel
    - Clic dentro del panel → lo cierra
    - Fade-in de 150ms al abrir
    """
    tooltip_box = ft.Container(
        content=ft.Column(
            [
                ft.Text(titulo, weight=ft.FontWeight.BOLD, color="#2A579A", size=13),
                ft.Text(mensaje, color="#333333", size=12),
            ],
            spacing=4,
            height=200,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.Border.all(1, "#E0E0E0"),
        border_radius=6,
        padding=12,
        width=280,
        shadow=ft.BoxShadow(
            blur_radius=12,
            color="#26000000",
            offset=ft.Offset(0, 4),
        ),
        visible=False,
        opacity=0,
        animate_opacity=150,
        bottom=30,
        left=-132,
    )

    is_open = [False]

    def _set_opacity(value):
        try:
            tooltip_box.opacity = value
            if tooltip_box.page:
                tooltip_box.update()
        except Exception:
            pass

    def _show():
        try:
            is_open[0] = True
            tooltip_box.visible = True
            if tooltip_box.page:
                tooltip_box.update()
            import threading
            threading.Timer(0.05, lambda: _set_opacity(1)).start()
        except Exception:
            pass

    def _hide():
        try:
            is_open[0] = False
            _set_opacity(0)
            import threading
            threading.Timer(0.15, lambda: _finish_hide()).start()
        except Exception:
            pass

    def _finish_hide():
        try:
            if not is_open[0]:
                tooltip_box.visible = False
                if tooltip_box.page:
                    tooltip_box.update()
        except Exception:
            pass

    def on_click(e):
        """Alterna el tooltip al hacer clic en el ícono."""
        if is_open[0]:
            _hide()
        else:
            _show()

    def on_tooltip_click(e):
        """Clic dentro del panel lo cierra."""
        _hide()

    tooltip_box.on_click = on_tooltip_click

    icon_container = ft.Container(
        content=ft.Icon(
            ft.Icons.INFO_OUTLINE,
            size=16,
            color=ft.Colors.BLUE_400,
        ),
        padding=6,
        border_radius=14,
        on_click=on_click,
        tooltip="Más información",
    )

    return ft.Stack(
        controls=[icon_container, tooltip_box],
        clip_behavior=ft.ClipBehavior.NONE,
        width=28,
        height=28,
    )


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
