import subprocess
import json

def get_3rd_party_apps():
    # PowerShell script to get installed programs from registry
    ps_script = """
    $paths = @("HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
               "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
               "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*")
    Get-ItemProperty $paths | Select-Object DisplayName, UninstallString | Where-Object { $_.DisplayName -ne $null } | ConvertTo-Json
    """
    try:
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

print(get_3rd_party_apps())
