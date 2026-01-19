import flet as ft
from src.core.update_logic import UpdateLogic

class UpdatesPage(ft.Container):
    def __init__(self):
        super().__init__()
        self.logic = UpdateLogic()
        self.padding = 20
        self.output_text = ft.Text(value="", font_family="Consolas")
        
        self.content = ft.Column(
            [
                ft.Text("System Update Manager", size=24, weight="bold"),
                ft.Text("Manage Windows/Linux updates from here.", italic=True),
                ft.Divider(),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Check for Updates", 
                            icon=ft.Icons.SEARCH, 
                            on_click=self.on_check_click
                        ),
                        ft.ElevatedButton(
                            "Install Updates", 
                            icon=ft.Icons.DOWNLOAD, 
                            on_click=self.on_install_click,
                            color=ft.Colors.GREEN_200
                        ),
                    ],
                    spacing=20
                ),
                ft.Divider(),
                ft.Text("Output:", weight="bold"),
                ft.Container(
                    content=ft.Column([self.output_text], scroll=ft.ScrollMode.ALWAYS),
                    bgcolor=ft.Colors.BLACK54,
                    padding=15,
                    border_radius=5,
                    height=300,
                    width=float("inf")
                )
            ]
        )

    def on_check_click(self, e):
        self.output_text.value = "Checking for updates..."
        self.update()
        success, msg = self.logic.check_updates()
        self.output_text.value += f"\n\n{msg}"
        self.update()

    def on_install_click(self, e):
        self.output_text.value = "Starting installation..."
        self.update()
        success, msg = self.logic.install_updates()
        self.output_text.value += f"\n\n{msg}"
        self.update()
