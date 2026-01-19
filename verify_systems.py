import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.core.debloater_logic import DebloaterLogic
from src.core.installer_logic import InstallerLogic
from src.core.update_logic import UpdateLogic
from src.core.desktop_logic import DesktopLogic
from src.core.system_logic import SystemLogic

def check_logic():
    print("--- Starting System Logic Verification ---")
    
    # 1. Debloater Logic
    print("\n[DebloaterLogic]")
    deb = DebloaterLogic()
    apps = deb.get_windows_apps()
    if isinstance(apps, dict) and len(apps) > 0:
        print(f"PASS: App list retrieved ({len(apps)} items)")
        print(f"Keys: {list(apps.keys())}")
    else:
        print("FAIL: App list empty or invalid")

    # 2. Installer Logic
    print("\n[InstallerLogic]")
    inst = InstallerLogic()
    print(f"Winget Available: {inst.winget_avail}")
    apps_list = inst.get_apps_list()
    if isinstance(apps_list, list) and len(apps_list) > 0:
        print(f"PASS: Installer apps list retrieved ({len(apps_list)} items)")
    else:
        print("FAIL: Installer apps list invalid")

    # 3. Desktop Logic
    print("\n[DesktopLogic]")
    dsk = DesktopLogic()
    try:
        # Just checking if methods exist and don't crash on init
        res = getattr(dsk, "set_wallpaper")
        print("PASS: Methods present")
    except:
        print("FAIL: Methods missing")

    # 4. Update Logic
    print("\n[UpdateLogic]")
    upd = UpdateLogic()
    print("PASS: Init success")

    # 5. System Logic
    print("\n[SystemLogic]")
    sys_l = SystemLogic()
    print("PASS: Init success")
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    check_logic()
