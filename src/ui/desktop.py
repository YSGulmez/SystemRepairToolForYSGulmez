import flet as ft
import os
from src.core.desktop_logic import DesktopLogic, get_resource_path

class DesktopPage(ft.Container):
    def __init__(self):
        super().__init__()
        self.logic = DesktopLogic()
        self.padding = 20
        self.expand = True

        self.status_text = ft.Text("")
        self.file_picker = ft.FilePicker()
        self.file_picker.on_result = self.on_file_picked
        
        # Gallery container
        self.gallery = ft.Row(wrap=True, spacing=10, scroll=ft.ScrollMode.AUTO)
        
        self.content = ft.Column(
            [
                self.file_picker,
                ft.Text("Desktop Management", size=24, weight="bold"),
                ft.Divider(),
                ft.Text("Wallpaper Gallery", size=18, weight="bold"),
                ft.Text("Add your images to src/assets/wallpapers/ to see them here.", size=12, color=ft.Colors.GREY_400),
                ft.Container(
                    content=self.gallery,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=10,
                    height=300,
                    expand=False
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Browse Other Image", icon=ft.Icons.IMAGE, on_click=self.on_browse_click),
                        ft.ElevatedButton("Apply Default Windows Wallpaper", icon=ft.Icons.RESTORE, on_click=self.on_apply_default, color=ft.Colors.BLUE_GREY_300),
                        self.status_text
                    ]
                ),
                ft.Divider(),
                ft.Text("Quick Fixes", size=18, weight="bold"),
                ft.ElevatedButton("Restart Explorer / Finder", icon=ft.Icons.REFRESH, on_click=self.on_restart_explorer, color=ft.Colors.ORANGE_300)
            ],
            expand=True
        )
        # Wallpapers will be loaded in did_mount

    def did_mount(self):
        self.load_wallpapers()

    def load_wallpapers(self):
        """Scans assets/wallpapers and populates the gallery."""
        # Use get_resource_path to find assets folder
        gallery_path = get_resource_path(os.path.join("src", "assets", "wallpapers"))
        self.gallery.controls.clear()
        
        if not os.path.exists(gallery_path):
            # Fallback if get_resource_path didn't find it (e.g. dev mode check)
            gallery_path = os.path.join(os.getcwd(), "src", "assets", "wallpapers")
            if not os.path.exists(gallery_path):
                os.makedirs(gallery_path, exist_ok=True)
                self.gallery.controls.append(ft.Text("No built-in wallpapers found."))
                return

        supported_exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        files = [f for f in os.listdir(gallery_path) if f.lower().endswith(supported_exts)]
        
        if not files:
            self.gallery.controls.append(ft.Text("Gallery is empty."))
        else:
            for file_name in files:
                full_path = os.path.join(gallery_path, file_name)
                self.gallery.controls.append(self.create_wallpaper_card(file_name, full_path))
        
        self.update()

    def create_wallpaper_card(self, name, path):
        return ft.GestureDetector(
            on_tap=lambda _: self.set_wallpaper_from_gallery(path),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=path,
                            width=150,
                            height=85,
                            fit=ft.BoxFit.COVER,
                            border_radius=5,
                        ),
                        ft.Text(name[:15] + "..." if len(name) > 15 else name, size=10, text_align=ft.TextAlign.CENTER, width=150),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                padding=5,
                border_radius=8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                ink=True,
            )
        )

    def set_wallpaper_from_gallery(self, path):
        self.status_text.value = "Applying wallpaper..."
        self.update()
        success, msg = self.logic.set_wallpaper(path)
        self.status_text.value = msg
        self.update()

    def on_browse_click(self, e):
        self.page.run_task(self.file_picker.pick_files)

    def on_file_picked(self, e):
        if e.files:
            file_path = e.files[0].path
            self.status_text.value = f"Setting wallpaper: {e.files[0].name}..."
            self.update()
            
            success, msg = self.logic.set_wallpaper(file_path)
            self.status_text.value = msg
            self.update()

    def on_apply_default(self, e):
        self.status_text.value = "Applying default wallpaper..."
        self.update()
        success, msg = self.logic.set_default_wallpaper()
        self.status_text.value = msg
        self.update()

    def on_restart_explorer(self, e):
        success, msg = self.logic.restart_explorer()
        self.status_text.value = msg
        self.update()
