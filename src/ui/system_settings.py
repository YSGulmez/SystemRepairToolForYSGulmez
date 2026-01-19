import flet as ft
from src.core.system_logic import SystemLogic

class SystemPage(ft.Container):
    def __init__(self, on_theme_toggle=None):
        super().__init__()
        self.logic = SystemLogic()
        self.on_theme_toggle = on_theme_toggle
        self.padding = 20

        self.status = ft.Text()
        
        self.content = ft.Column(
            [
                ft.Text("System Settings", size=24, weight="bold"),
                ft.Divider(),
                ft.Text("Appearance", size=18, weight="bold"),
                ft.Row(
                    [
                        ft.ElevatedButton("Toggle Light/Dark Mode", icon=ft.Icons.BRIGHTNESS_4, on_click=lambda _: self.on_theme_toggle() if self.on_theme_toggle else None),
                    ]
                ),
                ft.Divider(),
                ft.Text("System Maintenance", size=18, weight="bold"),
                ft.Row(
                    [
                        ft.ElevatedButton("Deep Cleanup", icon=ft.Icons.CLEANING_SERVICES, on_click=self.on_cleanup_click, color=ft.Colors.GREEN_400),
                        ft.ElevatedButton("Repair System Files", icon=ft.Icons.BUILD, on_click=self.on_repair_click, color=ft.Colors.BLUE_400),
                    ]
                ),
                ft.Divider(),
                ft.Text("Danger Zone", size=18, weight="bold", color=ft.Colors.RED_400),
                ft.Row(
                    [
                        ft.ElevatedButton("Factory Reset Device", icon=ft.Icons.FORMAT_COLOR_FILL_OUTLINED, on_click=self.on_format_click, color=ft.Colors.RED_700),
                    ]
                ),
                ft.Divider(),
                self.status
            ]
        )

    def on_sound_click(self, e):
        success, msg = self.logic.open_sound_settings()
        self.status.value = msg
        self.update()

    def on_cleanup_click(self, e):
        self.status.value = "Cleaning up..."
        self.update()
        success, msg = self.logic.cleanup_system()
        self.status.value = msg
        self.update()

    def on_repair_click(self, e):
        success, msg = self.logic.repair_system()
        self.status.value = msg
        self.update()

    def on_format_click(self, e):
        def close_dlg(e):
            confirm_dlg.open = False
            self.update()

        def confirm_reset(e):
            confirm_dlg.open = False
            success, msg = self.logic.format_device()
            self.status.value = msg
            self.update()

        confirm_dlg = ft.AlertDialog(
            title=ft.Text("Factory Reset"),
            content=ft.Text(f"Are you sure you want to reset this device? This action will open the { 'Windows Reset UI' if self.logic.os_type == 'Windows' else 'System Settings' }."),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.TextButton("Proceed", on_click=confirm_reset, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(confirm_dlg)
        confirm_dlg.open = True
        self.update()
