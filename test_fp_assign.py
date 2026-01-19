import flet as ft

def on_result(e):
    print("Result")

try:
    fp = ft.FilePicker()
    fp.on_result = on_result
    print("Assignment successful")
except Exception as e:
    print(f"Assignment failed: {e}")

print(f"On result in dict: {'on_result' in fp.__dict__}")
