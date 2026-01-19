import flet as ft

fp = ft.FilePicker()
print(f"Has on_result prop: {hasattr(fp, 'on_result')}")
print(f"Dir: {dir(fp)}")
