import flet as ft
print(f"Flet version: {getattr(ft, '__version__', 'unknown')}")
print("Attributes in ft starting with 'padding' or 'Padding':")
print([a for a in dir(ft) if a.lower().startswith('padding')])
print("Attributes in ft starting with 'margin' or 'Margin':")
print([a for a in dir(ft) if a.lower().startswith('margin')])

if hasattr(ft, 'Padding'):
    print(f"Dir ft.Padding: {dir(ft.Padding)}")
