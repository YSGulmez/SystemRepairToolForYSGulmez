import subprocess
import platform
import shutil

class InstallerLogic:
    def __init__(self):
        self.os_type = platform.system()
        self.winget_avail = self.detect_winget() if self.os_type == "Windows" else False

    def detect_winget(self):
        try:
            subprocess.run(["winget", "--version"], capture_output=True, check=True, shell=True)
            return True
        except:
            return False

    def get_apps_list(self):
        # A list of common IT tools
        return [
            {"name": "Google Chrome", "win_id": "Google.Chrome", "lin_pkg": "google-chrome-stable"},
            {"name": "Mozilla Firefox", "win_id": "Mozilla.Firefox", "lin_pkg": "firefox"},
            {"name": "7-Zip", "win_id": "7zip.7zip", "lin_pkg": "p7zip-full"},
            {"name": "AnyDesk", "win_id": "AnyDeskSoftwareGmbH.AnyDesk", "lin_pkg": "anydesk"},
            {"name": "VLC Media Player", "win_id": "VideoLAN.VLC", "lin_pkg": "vlc"},
            {"name": "Notepad++", "win_id": "Notepad++.Notepad++", "lin_pkg": "notepad-plus-plus"},
            {"name": "Visual Studio Code", "win_id": "Microsoft.VisualStudioCode", "lin_pkg": "code"},
        ]

    def install_app(self, app_data):
        if self.os_type == "Windows":
            if not self.winget_avail:
                return False, "Winget not found. Please install App Installer from MS Store."
            
            cmd = f"winget install -e --id {app_data['win_id']} --accept-package-agreements --accept-source-agreements"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout
            
        elif self.os_type == "Linux":
            pkg = app_data.get('lin_pkg')
            if not pkg:
                return False, "No Linux package defined for this app."
            
            # Run in terminal to handle sudo password
            cmd = f"echo 'Installing {pkg}...'; sudo apt install -y {pkg}; echo 'Installation complete. Press enter to exit.'; read"
            subprocess.run(f"x-terminal-emulator -e \"bash -c '{cmd}'\"", shell=True)
            return True, "Installation started in terminal. Please check the terminal window."
            
        return False, "Unsupported OS"
