import flet as ft
from config.theme import INCES_BLUE

def manual_view(page: ft.Page):
    try:
        with open("docs/MANUAL_DE_USUARIO.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Manual no disponible\n\nEl archivo `docs/MANUAL_DE_USUARIO.md` no fue encontrado."

    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=30, vertical=20),
                content=ft.Column([
                    ft.Text("Manual Técnico", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                    ft.Divider(height=10, color=ft.Colors.GREY_300),
                ])
            ),
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=30, vertical=10),
                content=ft.Column([
                    ft.Markdown(
                        value=content,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
                        on_tap_link=lambda e: page.launch_url(e.data),
                    )
                ], scroll=ft.ScrollMode.AUTO, expand=True)
            )
        ]
    )
