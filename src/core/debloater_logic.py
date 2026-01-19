import subprocess
import sys
import platform
import shutil

class DebloaterLogic:
    def __init__(self):
        self.os_type = platform.system()

    def run_command(self, command):
        try:
            if self.os_type == "Windows":
                # Ensure UTF-8 output from PowerShell
                ps_cmd = f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {command}"
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                    capture_output=True,
                    shell=False
                )
                output = result.stdout.decode('utf-8', errors='replace').strip()
                error = result.stderr.decode('utf-8', errors='replace').strip()
                
                if result.returncode != 0:
                    return False, error or output
                return True, output
            elif self.os_type == "Linux":
                # Check for apt (most common in current implementation)
                if "apt" in command and shutil.which("apt") is None:
                    return False, "Package manager 'apt' not found. This tool currently targets Debian/Ubuntu-based systems."
                
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
            else:
                return False, "Unsupported OS"
        except Exception as e:
            return False, str(e)

    def get_windows_apps(self):
        if self.os_type == "Linux":
            return self.get_linux_apps()
            
        try:
            cmd = "Get-AppxPackage | Select-Object Name, PackageFullName | ConvertTo-Json"
            success, output = self.run_command(cmd)
            if not success:
                return {}
            
            import json
            apps_list = json.loads(output)
            
            # PowerShell ConvertTo-Json can return a dict if single item, or list if multiple.
            if isinstance(apps_list, dict):
                apps_list = [apps_list]
                
            result = {}
            for app in apps_list:
                name = app.get('Name')
                package = app.get('PackageFullName')
                if name and package:
                    result[name] = package
            return result
        except Exception as e:
            print(f"Error fetching apps: {e}")
            return {}

    def remove_windows_app(self, package_name):
        if self.os_type == "Linux":
            return self.remove_linux_app(package_name)
        cmd = f"Get-AppxPackage *{package_name}* | Remove-AppxPackage"
        return self.run_command(cmd)

    def get_linux_apps(self):
        """Returns a combined list of Apt, Snap, and Flatpak apps."""
        apps = {}
        
        # 1. Apt Packages (Filtering for user-installed or common apps to avoid system break)
        # For simplicity, we'll list all, but label them
        success, output = self.run_command("dpkg-query -W -f='${Package} (Apt)\\n'")
        if success:
            for line in output.splitlines():
                if line.strip():
                    apps[line.strip()] = f"apt:{line.split(' (')[0]}"

        # 2. Snap Packages
        success, output = self.run_command("snap list --short")
        if success:
            for line in output.splitlines()[1:]: # Skip header
                name = line.split()[0]
                apps[f"{name} (Snap)"] = f"snap:{name}"

        # 3. Flatpak Packages
        success, output = self.run_command("flatpak list --columns=name,application")
        if success:
            for line in output.splitlines():
                parts = line.split('\t')
                if len(parts) >= 2:
                    apps[f"{parts[0].strip()} (Flatpak)"] = f"flatpak:{parts[1].strip()}"
        
        return dict(sorted(apps.items()))

    def remove_linux_app(self, app_id):
        """Removes a linux app based on its prefix (apt:, snap:, flatpak:)."""
        if app_id.startswith("apt:"):
            pkg = app_id.replace("apt:", "")
            # Use terminal for sudo prompt
            cmd = f"echo 'Removing {pkg}...'; sudo apt-get remove --purge -y {pkg}; echo 'Finished. Press enter.'; read"
            subprocess.run(f"x-terminal-emulator -e \"bash -c '{cmd}'\"", shell=True)
            return True, "Removal process started in terminal."
        elif app_id.startswith("snap:"):
            pkg = app_id.replace("snap:", "")
            cmd = f"echo 'Removing {pkg}...'; sudo snap remove {pkg}; echo 'Finished. Press enter.'; read"
            subprocess.run(f"x-terminal-emulator -e \"bash -c '{cmd}'\"", shell=True)
            return True, "Removal process started in terminal."
        elif app_id.startswith("flatpak:"):
            pkg = app_id.replace("flatpak:", "")
            cmd = f"echo 'Removing {pkg}...'; flatpak uninstall -y {pkg}; echo 'Finished. Press enter.'; read"
            subprocess.run(f"x-terminal-emulator -e \"bash -c '{cmd}'\"", shell=True)
            return True, "Removal process started in terminal."
        return False, "Unknown package type"

    def get_third_party_apps(self):
        if self.os_type != "Windows":
            return {} # Linux apps are already combined in get_linux_apps
            
        try:
            ps_script = """
            $paths = @("HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
                       "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
                       "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*")
            $apps = Get-ItemProperty $paths -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -ne $null } | Select-Object DisplayName, UninstallString, QuietUninstallString
            if ($apps) {
                $apps | ConvertTo-Json -Depth 2
            } else {
                "[]"
            }
            """
            success, output = self.run_command(ps_script)
            if not success or not output:
                return {}
                
            import json
            apps_data = json.loads(output)
            
            if isinstance(apps_data, dict):
                apps_data = [apps_data]
                
            result = {}
            for app in apps_data:
                name = app.get('DisplayName')
                # Prioritize quiet uninstall if available
                cmd = app.get('QuietUninstallString') or app.get('UninstallString')
                if name and cmd:
                    result[name] = cmd
            return dict(sorted(result.items()))
        except Exception as e:
            print(f"Error fetching 3rd party apps: {e}")
            return {}

    def remove_third_party_app(self, uninstall_cmd):
        """Executes the uninstall command with elevation."""
        if self.os_type != "Windows":
            return False, "Not supported on this OS"
            
        try:
            ps_script = f"""
            $cmd = '{uninstall_cmd.replace("'", "''")}'
            if ($cmd -match '^"([^"]+)"\\s*(.*)$') {{
                $file = $matches[1]
                $args = $matches[2]
            }} else {{
                $parts = $cmd -split ' ', 2
                $file = $parts[0]
                $args = if ($parts.Length -gt 1) {{ $parts[1] }} else {{ "" }}
            }}
            Start-Process -FilePath $file -ArgumentList $args -Verb RunAs -Wait
            """
            success, output = self.run_command(ps_script)
            return success, "Uninstallation process started/finished. Please check for UAC prompt."
        except Exception as e:
            return False, str(e)
