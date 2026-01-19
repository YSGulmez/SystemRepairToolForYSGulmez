import subprocess
import platform

class SystemLogic:
    def __init__(self):
        self.os_type = platform.system()

    def open_sound_settings(self):
        try:
            if self.os_type == "Windows":
                subprocess.run("start ms-settings:sound", shell=True)
                return True, "Opened Sound Settings."
            elif self.os_type == "Linux":
                subprocess.run("pavucontrol", shell=True)
                return True, "Opened PulseAudio Control."
        except Exception as e:
            return False, str(e)
        return False, "Unsupported OS"

    def cleanup_system(self):
        """Removes temporary files and system cache with elevation."""
        if self.os_type == "Windows":
            try:
                cleanup_cmd = (
                    "Write-Host 'Starting System Cleanup...' -ForegroundColor Cyan; "
                    "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue; "
                    "Remove-Item -Path C:\\Windows\\Temp\\* -Recurse -Force -ErrorAction SilentlyContinue; "
                    "Remove-Item -Path C:\\Windows\\Prefetch\\* -Recurse -Force -ErrorAction SilentlyContinue; "
                    "Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue; "
                    "Write-Host 'Cleanup completed!' -ForegroundColor Green; Start-Sleep -Seconds 2"
                )
                ps_elevate = f"Start-Process powershell -Verb RunAs -ArgumentList '-Command', \\\"{cleanup_cmd}\\\""
                subprocess.run(["powershell", "-Command", ps_elevate], shell=True)
                return True, "Cleanup started in an elevated window. Please approve the UAC prompt."
            except Exception as e:
                return False, f"Cleanup failed to start: {str(e)}"
        elif self.os_type == "Linux":
            try:
                # Use x-terminal-emulator to run cleanup with sudo
                cleanup_cmd = "echo 'Starting System Cleanup...'; sudo apt-get autoremove -y && sudo apt-get clean; rm -rf ~/.cache/*; echo 'Cleanup completed! Press enter to exit.'; read"
                result = subprocess.run(f"x-terminal-emulator -e \"bash -c '{cleanup_cmd}'\"", shell=True)
                return True, "Cleanup started in a terminal. Please enter your password if prompted."
            except Exception as e:
                return False, f"Cleanup failed: {str(e)}"
        
        return False, "Unsupported OS"

    def repair_system(self):
        """Runs repair commands with elevation."""
        if self.os_type == "Windows":
            try:
                inner_cmd = "Write-Host 'Starting System Repair (SFC & DISM)...' -ForegroundColor Cyan; sfc /scannow; DISM /Online /Cleanup-Image /RestoreHealth; Write-Host 'Repair finished. Press any key to exit.' -ForegroundColor Green; Read-Host"
                ps_elevate = f"Start-Process powershell -Verb RunAs -ArgumentList '-Command', \\\"{inner_cmd}\\\""
                subprocess.run(["powershell", "-Command", ps_elevate], shell=True)
                return True, "System repair requested elevation. Please check the UAC prompt."
            except Exception as e:
                return False, f"Repair failed to start: {str(e)}"
        elif self.os_type == "Linux":
            try:
                repair_cmd = "echo 'Starting System Repair...'; sudo dpkg --configure -a && sudo apt-get install -f; echo 'Repair completed! Press enter to exit.'; read"
                subprocess.run(f"x-terminal-emulator -e \"bash -c '{repair_cmd}'\"", shell=True)
                return True, "Repair started in a terminal. Please enter your password if prompted."
            except Exception as e:
                return False, f"Repair failed: {str(e)}"

        return False, "Unsupported OS"

    def format_device(self):
        """Triggers system reset UI."""
        if self.os_type == "Windows":
            try:
                subprocess.run("systemreset --factoryreset", shell=True)
                return True, "Windows Reset UI launched."
            except Exception as e:
                return False, f"Failed to launch Reset UI: {str(e)}"
        elif self.os_type == "Linux":
            # There's no universal "factory reset" for Linux, but we can point to gnome-control-center if available
            try:
                subprocess.run("gnome-control-center system", shell=True) # For newer GNOME, it's under system
                return True, "Opened System Settings. Look for Reset options if available on your distro."
            except:
                return False, "No universal reset UI found for this Linux distribution."

        return False, "Unsupported OS"
