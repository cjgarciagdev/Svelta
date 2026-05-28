import flet as ft

def main(page: ft.Page):
    try:
        p = ft.Padding.symmetric(horizontal=20, vertical=12)
        print("ft.Padding.symmetric works")
    except Exception as e:
        print(f"ft.Padding.symmetric failed: {e}")

    try:
        p = ft.padding.symmetric(horizontal=20, vertical=12)
        print("ft.padding.symmetric works")
    except Exception as e:
        print(f"ft.padding.symmetric failed: {e}")

if __name__ == "__main__":
    # We don't need a full app to test the attribute
    try:
        import flet.padding as padding
        print("flet.padding module exists")
        print(f"Dir padding: {dir(padding)}")
    except Exception as e:
        print(f"flet.padding module failed: {e}")
