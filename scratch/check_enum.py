import flet as ft
for attr in dir(ft.ClipBehavior):
    if not attr.startswith("_"):
        print(attr, "=", getattr(ft.ClipBehavior, attr))
