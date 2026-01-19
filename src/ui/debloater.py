import flet as ft
from src.core.debloater_logic import DebloaterLogic

class DebloaterPage(ft.Container):
    def __init__(self):
        super().__init__()
        self.logic = DebloaterLogic()
        self.padding = 20
        self.expand = True

        self.log_view = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=150)
        self.apps_list_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.checkboxes = []
        self.current_app_type = "Appx" # "Appx" or "ThirdParty"

        is_win = self.logic.os_type == "Windows"
        self.tabs = ft.Tabs(
            length=2 if is_win else 1,
            selected_index=0,
            on_change=self.on_tab_change,
            tabs=[
                ft.Tab(label="Windows Apps (Appx)" if is_win else "Linux Packages (Apt/Snap/Flatpak)", icon=ft.Icons.WINDOW if is_win else ft.Icons.TERMINAL),
                ft.Tab(label="3rd Party Apps", icon=ft.Icons.APPS) if is_win else ft.Tab(visible=False),
            ],
        )

        self.content = ft.Column(
            [
                ft.Text("Debloater Utility", size=24, weight="bold"),
                ft.Text(f"Detected OS: {self.logic.os_type}", italic=True),
                self.tabs,
                ft.Row(
                    [
                        ft.ElevatedButton("Scan Apps", icon=ft.Icons.SEARCH, on_click=self.on_scan_click),
                        ft.ElevatedButton("Remove Selected", on_click=self.on_remove_click, color=ft.Colors.RED_200, icon=ft.Icons.DELETE),
                    ]
                ),
                ft.Container(
                    content=self.apps_list_view,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                ft.Text("Execution Log:", size=16),
                ft.Container(
                    content=self.log_view,
                    bgcolor=ft.Colors.BLACK54,
                    padding=10,
                    border_radius=5
                )
            ],
            expand=True
        )

    def on_tab_change(self, e):
        self.current_app_type = "Appx" if self.tabs.selected_index == 0 else "ThirdParty"
        self.apps_list_view.controls.clear()
        self.checkboxes = []
        self.update()

    def on_scan_click(self, e):
        self.log(f"Scanning for {self.current_app_type}...")
        self.apps_list_view.controls.clear()
        self.apps_list_view.controls.append(ft.ProgressRing())
        self.update()
        
        if self.current_app_type == "Appx":
            apps = self.logic.get_windows_apps()
        else:
            apps = self.logic.get_third_party_apps()
            
        self.apps_list_view.controls.clear()
        self.checkboxes = []
        
        if not apps:
             self.log("No apps found.")
             self.apps_list_view.controls.append(ft.Text("No apps found."))
        else:
            self.log(f"Found {len(apps)} apps.")
            for name, data in apps.items():
                cb = ft.Checkbox(label=name, value=False, data=data)
                self.checkboxes.append(cb)
                self.apps_list_view.controls.append(cb)
        
        self.update()

    def log(self, message):
        self.log_view.controls.append(ft.Text(f"> {message}", font_family="Consolas", size=12))
        self.update()

    def on_remove_click(self, e):
        to_remove = [cb for cb in self.checkboxes if cb.value]
        if not to_remove:
            self.log("No apps selected.")
            return

        self.log(f"Starting removal of {len(to_remove)} apps...")
        for cb in to_remove:
            self.log(f"Removing {cb.label}...")
            if self.current_app_type == "Appx":
                success, output = self.logic.remove_windows_app(cb.data)
            else:
                success, output = self.logic.remove_third_party_app(cb.data)
                
            if success:
                self.log(f"Success: {cb.label}")
            else:
                self.log(f"Failed: {output}")
        self.log("Process complete.")
