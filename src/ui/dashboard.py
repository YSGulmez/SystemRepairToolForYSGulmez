import flet as ft
import psutil

class Dashboard(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 20
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        
        self.content = ft.Column(
            [
                ft.Text("System Overview", size=24, weight="bold"),
                ft.Divider(),
                ft.Row(
                    [
                        self.create_stat_card("CPU Usage", f"{cpu_usage}%", ft.Icons.COMPUTER, ft.Colors.BLUE),
                        self.create_stat_card("RAM Usage", f"{ram_usage}%", ft.Icons.MEMORY, ft.Colors.ORANGE),
                        self.create_stat_card("Disk Status", "Healthy", ft.Icons.STORAGE, ft.Colors.GREEN),
                    ],
                    spacing=20
                ),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.Text("Quick Actions", size=20, weight="bold"),
                ft.Row(
                    [
                        ft.ElevatedButton("Scan System", icon=ft.Icons.SEARCH),
                        ft.ElevatedButton("Clear Temp", icon=ft.Icons.DELETE_OUTLINE),
                        ft.ElevatedButton("Check Updates", icon=ft.Icons.UPDATE),
                    ]
                )
            ]
        )

    def create_stat_card(self, title, value, icon, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=color),
                    ft.Text(value, size=20, weight="bold"),
                    ft.Text(title, size=12, color=ft.Colors.GREY_400),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=150,
            height=120,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
            padding=20,
            alignment=ft.alignment.Alignment(0, 0),
        )
