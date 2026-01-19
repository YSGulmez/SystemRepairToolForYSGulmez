import subprocess
import json
import sys

def get_3rd_party_apps():
    ps_script = """
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $paths = @("HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
               "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
               "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*")
    $apps = Get-ItemProperty $paths -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -ne $null } | Select-Object DisplayName, UninstallString, QuietUninstallString
    $apps | ConvertTo-Json
    """
    try:
        # Pass script as encoded bytes to avoid shell encoding issues
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
        # Decode as utf-8 (ignoring errors if any)
        return result.stdout.decode('utf-8', errors='ignore')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    output = get_3rd_party_apps()
    print(output)
