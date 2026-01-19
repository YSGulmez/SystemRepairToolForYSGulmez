import subprocess
import platform

class UpdateLogic:
    def __init__(self):
        self.os_type = platform.system()

    def run_command(self, command):
        try:
            # shell=True is needed for complex commands but has security risks. 
            # For a local tool, it's acceptable if inputs are controlled.
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return True, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    def check_updates(self):
        if self.os_type == "Windows":
            # USOCLient can trigger the scan.
            # StartScan: Starts the scan
            cmd = "usoclient StartScan"
            success, _ = self.run_command(cmd)
            return success, "Windows Update Scan Triggered. Please check Settings > Windows Update."
        elif self.os_type == "Linux":
            cmd = "echo 'Checking for updates...'; sudo apt update; echo 'Check complete. Press enter to exit.'; read"
            subprocess.run(f"x-terminal-emulator -e \"bash -c '{cmd}'\"", shell=True)
            return True, "Update check started in terminal."
        return False, "Unsupported OS"

    def install_updates(self):
        if self.os_type == "Windows":
            # ResumeUpdate: Resumes update installation
            cmd = "usoclient StartInstall"
            success, _ = self.run_command(cmd)
            return success, "Windows Update Installation Triggered."
        elif self.os_type == "Linux":
            cmd = "echo 'Installing upgrades...'; sudo apt upgrade -y; echo 'Upgrades installed. Press enter to exit.'; read"
            subprocess.run(f"x-terminal-emulator -e \"bash -c '{cmd}'\"", shell=True)
            return True, "Upgrade process started in terminal."
        return False, "Unsupported OS"
