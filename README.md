# System Repair Tool For YSGulmez

A modern system repair and optimization tool for Windows built with Python and Flet.

## Features

- Dashboard with system statistics.
- Windows Debloater (requires Admin).
- System Updates management.
- Desktop Customization.
- App Installer.
- Dark/Light Theme Support.

## How to Use (Pre-built Binary)

If you don't want to deal with Python and code, you can use the pre-built version in the `dist/` folder or download it from the Releases page.

1. Download `SystemRepairTool.exe`.
2. Right-click and **Run as Administrator** (required for Debloater and Updates).
   - *Note: You might see a Windows SmartScreen warning. Click 'More Info' and 'Run anyway'.*

## Installation & Setup (For Developers)

1. Install Python 3.10+.
2. Clone the repository.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## Building Executable

```bash
python build_exe.py
```

This produces a single-file executable in the `dist/` folder.

## Project Structure

- `main.py`: Main entry point.
- `src/ui/`: UI components (Flet).
- `src/core/`: Logic and backend functionalities.
- `src/assets/`: Images and other static files.
- `build_exe.py`: Windows build script.
