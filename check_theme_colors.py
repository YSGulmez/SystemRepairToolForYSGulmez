import flet as ft

def check_colors():
    c = ft.Colors
    print(f"ON_SURFACE: {hasattr(c, 'ON_SURFACE')}")
    print(f"SURFACE_CONTAINER: {hasattr(c, 'SURFACE_CONTAINER')}")
    print(f"ON_SURFACE_VARIANT: {hasattr(c, 'ON_SURFACE_VARIANT')}")

check_colors()
