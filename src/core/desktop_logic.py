import subprocess
import platform
import ctypes
import os
import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DesktopLogic:
    def __init__(self):
        self.os_type = platform.system()

    def set_wallpaper(self, image_path):
        if not os.path.exists(image_path):
            return False, "Image file not found."

        try:
            if self.os_type == "Windows":
                # SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
                return True, "Wallpaper changed successfully."
            elif self.os_type == "Linux":
                # Try to detect desktop environment
                de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
                
                if "gnome" in de or "ubuntu" in de:
                    cmd = f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}"
                    subprocess.run(cmd, shell=True)
                    return True, "Wallpaper changed (GNOME)."
                elif "kde" in de or "plasma" in de:
                    script = f"""
                    var allDesktops = desktops();
                    for (i=0;i<allDesktops.length;i++) {{
                        d = allDesktops[i];
                        d.wallpaperPlugin = "org.kde.image";
                        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                        d.writeConfig("Image", "file://{image_path}");
                    }}
                    """
                    cmd = f"dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:{script}'"
                    subprocess.run(cmd, shell=True)
                    return True, "Wallpaper changed (KDE)."
                elif "xfce" in de:
                    # XFCE usually has multiple monitors/workspaces, trying to set for all
                    cmd = f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s {image_path}"
                    subprocess.run(cmd, shell=True)
                    return True, "Wallpaper changed (XFCE)."
                
                return False, f"Wallpaper change failed (Unsupported DE: {de})."
            return False, "Unsupported OS"
        except Exception as e:
            return False, str(e)

    def set_default_wallpaper(self):
        """Sets the wolf wallpaper as default."""
        try:
            # We want the wolf wallpaper to be the default
            # The path is relative to the project root in dev, or bundled in EXE
            wolf_path = get_resource_path(os.path.join("src", "assets", "wallpapers", "wolf_wallpaper.jpg"))
            
            if os.path.exists(wolf_path):
                return self.set_wallpaper(wolf_path)
            else:
                # Fallback to Windows default if wolf is missing
                default_path = r"C:\Windows\Web\Wallpaper\Windows\img0.jpg"
                if os.path.exists(default_path):
                    return self.set_wallpaper(default_path)
                return False, f"Wallpaper not found at {wolf_path}"
        except Exception as e:
            return False, f"Failed to set default: {str(e)}"

    def restart_explorer(self):
        if self.os_type == "Windows":
            cmd = "taskkill /f /im explorer.exe & start explorer.exe"
            subprocess.run(cmd, shell=True)
            return True, "Explorer restarted."
        elif self.os_type == "Linux":
            de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
            if "gnome" in de:
                # GNOME Shell restart (only works on X11)
                subprocess.run("gnome-shell --replace &", shell=True)
                return True, "GNOME Shell restart initiated."
            elif "kde" in de or "plasma" in de:
                subprocess.run("kquitapp5 plasmashell && kstart5 plasmashell &", shell=True)
                return True, "KDE Plasma Shell restarted."
            elif "xfce" in de:
                subprocess.run("xfce4-panel -r &", shell=True)
                return True, "XFCE Panel restarted."
            
            return False, f"Restart not implemented for {de}."
        return False, "Unsupported OS"
