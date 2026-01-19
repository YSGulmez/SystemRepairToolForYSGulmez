import flet as ft
from src.core.installer_logic import InstallerLogic

class InstallerPage(ft.Container):
    def __init__(self):
        super().__init__()
        self.logic = InstallerLogic()
        self.apps = self.logic.get_apps_list()
        self.padding = 20

        self.status_text = ft.Text(value="Select apps to install.")
        
        self.content = ft.Column(
            [
                ft.Text("App Installer", size=24, weight="bold"),
                ft.Text(f"Method: {'Winget' if self.logic.winget_avail else 'Manual'} (Windows) / Apt (Linux)", italic=True),
                ft.Divider(),
                self.build_app_list(),
                ft.Divider(),
                ft.Row(
                    [
                        ft.ElevatedButton("Install Selected", on_click=self.on_install_click, icon=ft.Icons.DOWNLOAD_FOR_OFFLINE),
                        self.status_text
                    ]
                )
            ]
        )

    def build_app_list(self):
        self.checkboxes = []
        rows = []
        for app in self.apps:
            cb = ft.Checkbox(label=app["name"], data=app)
            self.checkboxes.append(cb)
            rows.append(cb)
        
        return ft.ListView(controls=rows, height=400)

    def on_install_click(self, e):
        to_install = [cb for cb in self.checkboxes if cb.value]
        if not to_install:
            self.status_text.value = "No apps selected."
            self.update()
            return

        self.status_text.value = f"Installing {len(to_install)} apps..."
        self.update()

        for cb in to_install:
            app_name = cb.data["name"]
            self.status_text.value = f"Installing {app_name}..."
            self.update()
            
            success, msg = self.logic.install_app(cb.data)
            status = "Done" if success else "Failed"
            cb.label = f"{app_name} - {status}"
            cb.value = False
            self.update()
        
        self.status_text.value = "Installation process finished."
        self.update()
