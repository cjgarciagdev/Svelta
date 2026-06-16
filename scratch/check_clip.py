import flet as ft
import inspect

for cls in [ft.Container, ft.Row, ft.Column]:
    print(cls.__name__)
    sig = inspect.signature(cls.__init__)
    if "clip_behavior" in sig.parameters:
        print("  clip_behavior parameter exists")
    else:
        print("  clip_behavior parameter does not exist")
    # check default in _prop_defaults or similar if possible
    c = cls()
    print("  default clip_behavior:", getattr(c, "clip_behavior", None))
