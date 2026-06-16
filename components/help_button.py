import flet as ft
from config.theme import INCES_TEAL
import threading


def create_help_button(page: ft.Page, title: str, help_text: str):
    """Botón circular '!' con popup flotante activado por clic."""
    popup = ft.Container(
        content=ft.Column(
            [
                ft.Text(title, weight=ft.FontWeight.BOLD, color=INCES_TEAL, size=13),
                ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                ft.Text(help_text, size=12, color="#333333"),
            ],
            spacing=4,
            height=200,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.Border.all(1, "#E0E0E0"),
        border_radius=8,
        padding=14,
        width=280,
        shadow=ft.BoxShadow(
            blur_radius=12,
            color="#26000000",
            offset=ft.Offset(0, 4),
        ),
        visible=False,
        opacity=0,
        animate_opacity=150,
        top=36,
        left=0,
    )

    is_open = [False]

    def _set_opacity(value):
        try:
            popup.opacity = value
            if popup.page:
                popup.update()
        except Exception:
            pass

    def _show():
        try:
            is_open[0] = True
            popup.visible = True
            if popup.page:
                popup.update()
            threading.Timer(0.05, lambda: _set_opacity(1)).start()
        except Exception:
            pass

    def _hide():
        try:
            is_open[0] = False
            _set_opacity(0)
            threading.Timer(0.15, _finish_hide).start()
        except Exception:
            pass

    def _finish_hide():
        try:
            if not is_open[0]:
                popup.visible = False
                if popup.page:
                    popup.update()
        except Exception:
            pass

    def on_click(e):
        if is_open[0]:
            _hide()
        else:
            _show()

    def on_popup_click(e):
        _hide()

    popup.on_click = on_popup_click

    icon_container = ft.Container(
        content=ft.Text("!", size=16, weight=ft.FontWeight.BOLD, color=INCES_TEAL, text_align=ft.TextAlign.CENTER),
        width=32,
        height=32,
        border=ft.border.Border.all(1.5, INCES_TEAL),
        border_radius=16,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=on_click,
    )

    return ft.Stack(
        controls=[icon_container, popup],
        clip_behavior=ft.ClipBehavior.NONE,
        width=32,
        height=32,
    )
