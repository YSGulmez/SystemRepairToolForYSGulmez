import flet as ft

print("Checking flet attributes:")
try:
    print(f"ft.Colors exists: {hasattr(ft, 'Colors')}")
    print(f"ft.colors exists: {hasattr(ft, 'colors')}")
except Exception as e:
    print(e)

try:
    print(f"ft.Icons exists: {hasattr(ft, 'Icons')}")
    print(f"ft.icons exists: {hasattr(ft, 'icons')}")
except Exception as e:
    print(e)

if hasattr(ft, 'Colors'):
    print(f"Blue in ft.Colors: {hasattr(ft.Colors, 'BLUE')}")
