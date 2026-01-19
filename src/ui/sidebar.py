import flet as ft

class Sidebar(ft.Container):
    def __init__(self, nav_callback):
        super().__init__()
        self.nav_callback = nav_callback
        self.padding = 20
        self.width = 200
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.border_radius = ft.border_radius.only(top_right=10, bottom_right=10)
        
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Text("Menu", size=20, weight="bold", color=ft.Colors.ON_SURFACE),
                    padding=ft.padding.only(bottom=20)
                ),
                self.create_menu_item("Dashboard", ft.Icons.DASHBOARD, 0),
                self.create_menu_item("Debloater", ft.Icons.CLEANING_SERVICES, 1),
                self.create_menu_item("Updates", ft.Icons.UPDATE, 2),
                self.create_menu_item("Desktop", ft.Icons.DESKTOP_WINDOWS, 3),
                self.create_menu_item("System", ft.Icons.SETTINGS_SYSTEM_DAYDREAM, 4),
                self.create_menu_item("Installer", ft.Icons.DOWNLOAD, 5),
            ],
            spacing=5,
        )

    def create_menu_item(self, text, icon, index):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text(text, size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ],
                spacing=15,
            ),
            padding=10,
            border_radius=5,
            ink=True,
            on_click=lambda e: self.nav_callback(index),
            data=index
        )
