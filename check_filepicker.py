import flet as ft
import inspect

print("Checking FilePicker signature:")
try:
    sig = inspect.signature(ft.FilePicker)
    print(sig)
except Exception as e:
    print(e)

print(f"Has on_result: {'on_result' in inspect.signature(ft.FilePicker).parameters}")
