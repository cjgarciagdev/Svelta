import flet as ft
from config.theme import INCES_TEAL
import threading


def create_help_button(page: ft.Page, title: str, help_text: str):
    """Botón circular '!' que abre un diálogo de ayuda sobre todo el sistema."""
    
    def close_dlg(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text(title, weight=ft.FontWeight.BOLD, color=INCES_TEAL, size=16),
        content=ft.Container(
            content=ft.Text(help_text, size=13, color=ft.Colors.BLACK87),
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
        if dialog not in page.overlay:
            page.overlay.append(dialog)
        dialog.open = True
        page.update()

    icon_container = ft.Container(
        content=ft.Text("!", size=16, weight=ft.FontWeight.BOLD, color=INCES_TEAL, text_align=ft.TextAlign.CENTER),
        width=32,
        height=32,
        border=ft.border.Border.all(1.5, INCES_TEAL),
        border_radius=16,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=on_click,
        tooltip="Haz clic para ver ayuda",
    )

    return icon_container
