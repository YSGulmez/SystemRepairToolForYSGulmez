import os
import subprocess
import sys

def build_executable():
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Attempt to add flet to PATH if not found
    import shutil
    if not shutil.which("flet"):
        print("'flet' command not found in PATH. Attempting to locate...")
        user_base = os.path.expanduser("~")
        possible_paths = [
            os.path.join(user_base, "AppData", "Roaming", "Python", "Python314", "Scripts"),
            os.path.join(os.path.dirname(sys.executable), "Scripts"),
        ]
        
        for p in possible_paths:
            if os.path.isdir(p):
                os.environ["PATH"] += os.pathsep + p
                print(f"Added to PATH: {p}")

    # Define build command
    # --onefile: Create a single executable
    # --noconsole: Don't show console window (optional, maybe keep for debug)
    # --name: Name of the exe
    # --add-data: Add assets (flet requires this implicitly, but ensuring src is there)
    
    # Flet apps often need specific handling. 
    # Usually: flet pack main.py --name "SystemRepairTool" --icon "assets/icon.ico"
    # But we'll use standard pyinstaller for more control if needed.
    
    print("Building Executable via PyInstaller...")
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "SystemRepairTool",
        "--icon", "src/assets/favicon.ico",
        "--add-data", "src;src",
        "main.py"
    ]
    
    # We will use 'flet pack' which wrapper around pyinstaller
    try:
        subprocess.check_call(cmd, shell=True)
        print("Build Successful! Check the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"Build Failed: {e}")

if __name__ == "__main__":
    build_executable()
