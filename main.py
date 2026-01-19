import flet as ft
import sys
from src.ui.sidebar import Sidebar
from src.ui.dashboard import Dashboard
from src.ui.debloater import DebloaterPage
from src.ui.updates import UpdatesPage
from src.ui.installer import InstallerPage
from src.ui.desktop import DesktopPage
from src.ui.system_settings import SystemPage

def main(page: ft.Page):
    page.title = "IT System Repair Tool"
    page.window_width = 1100
    page.window_height = 800
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    
    # Platform Detection
    platform = sys.platform
    user_role = "Admin" # Placeholder
    
    def toggle_theme():
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        page.update()

    # Current Content Container
    content_area = ft.Container(
        expand=True,
        padding=20,
    )
    
    def on_nav_change(index):
        content_area.content = get_page_content(index)
        page.update()

    def get_page_content(index):
        if index == 0:
            return Dashboard()
        elif index == 1:
            return DebloaterPage()
        elif index == 2:
            return UpdatesPage()
        elif index == 3:
            return DesktopPage()
        elif index == 4:
            return SystemPage(on_theme_toggle=toggle_theme)
        elif index == 5:
            return InstallerPage()
        return ft.Text("Not Found")

    # Set initial content
    content_area.content = get_page_content(0)
    
    sidebar = Sidebar(on_nav_change)
    
    layout = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1),
            content_area
        ],
        expand=True,
    )
    
    page.add(layout)

if __name__ == "__main__":
    ft.run(main, assets_dir="src/assets")
