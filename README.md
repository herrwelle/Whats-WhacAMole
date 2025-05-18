# Whats Game - Whac-A-Mole with a Twist
<sub>*My first game, dedicated to everyone who seeks a little joy.*</sub>

A humorous take on the classic Whac-A-Mole game, built with Pygame.  
Follow these steps to set up and build the project locally.

![Game Demo GIF](Demo/Whats_demo.gif)


# 📂 Initial Setup
Create a project folder** (e.g., `Whats_Game`) on your Desktop or any preferred location.  


# 🛠️ Build Instructions
```bash
1. Set Up Virtual Environment (venv)
Navigate to your project folder and create a virtual environment:

cd ~/Desktop/Whats_Game          # Or your custom path
cd C:\Users\YourUsername\...     # Or your custom path (Windows)

python3 -m venv venv             # Create virtual environment
python -m venv venv              # Create virtual environment (Windows)

source venv/bin/activate         # macOS
venv\Scripts\activate            # Windows
After activation, your terminal prompt should show (venv).



2. Install Dependencies
<BASH>
pip3 install jaraco.text pygame py2app  # macOS
pip install pygame py2app               # Windows
⚠️ Windows users, please use main_win.py and rename it to main.py by removing the _win suffix.


3. Test the Game
<BASH>
python3 main.py  # macOS
python main.py   # Windows

⚠️ If you encounter the error pygame.error: Unsupported image format on Windows:
Cause: PNG files generated on macOS may use an incompatible format.
Fix: Open the problematic image(s) in an editor (e.g., Paint, Photoshop, GIMP) and re-save them as PNG.
Use Pre-fixed Images (Recommended):
Download the images_win folder (included in this project) and overwrite the files in the images folder with the Windows-compatible versions.



4. Build macOS/Windows Executable
<BASH>
python3 setup.py py2app       # macOS
The app bundle will be generated in dist/Whats.app.
⚠️ For ARM64, use the file setup.py_ARM64 and For x64, use the file setup.py_x64.
⚠️ Important: Before using, remove "_ARM64" or "_x64" from the filename, keeping only setup.py


Windows Packaging Instructions
To create a standalone .exe file using PyInstaller, run the following command in Command Prompt:

pip install pyinstaller
pyinstaller --onefile --windowed ^
  --add-data "images;images" ^
  --add-data "sounds;sounds" ^
  --add-data "appicon.ico;." ^
  --icon "C:\Users\YourUsername\Desktop\Whats_game\appicon.ico" ^
  --name Whats ^
  main.py
⚠️ No icon in the .exe? Change the filename to bypass cache.



5. Create DMG (macOS Only)
First, install create-dmg (if needed):

<BASH>
brew install create-dmg
cd ~/Desktop/Whats_Game    # Or your custom path

<BASH>
create-dmg \
  --volname "Whats 1.0.1" \
  --volicon "appicon.icns" \
  --window-pos 200 120 \
  --window-size 500 300 \
  --icon-size 100 \
  --icon "Whats.app"    100 100 \
  --icon "CREDITS.txt"  250 100 \
  --hide-extension "Whats.app" \
  --hide-extension "CREDITS.txt" \
  --app-drop-link 400 100 \
  "../Whats_1.0.1.dmg" \
  "dist/"



Creating an Installer (Windows Only)
Install Inno Setup

Download and install from the official website:
https://jrsoftware.org/isinfo.php

Compile the Installer
Open Whats.iss in Inno Setup Compiler, then click the "Compile" button.

Output
Once completed, the installer Whats_Setup.exe will be generated in the Output folder (located in the script directory).

```
❗ Important Copyright Notice:

Some audio assets are restricted to non-commercial use only (see CREDITS.txt for details).
You MUST include CREDITS.txt (Path to CREDITS for DMG/Installer: dist/CREDITS.txt) in all distributed packages to comply with licensing terms.
For commercial use, replace them with CC0/licensed audio or obtain permission from the original authors.

📦 Pre-Built Releases
Download ready-to-play versions for:
macOS (Intel/ARM64)
Windows
See Releases page.

❓ Troubleshooting
macOS 10.15 (Catalina) or older: Not officially supported (tested on macOS 12+).
Permission errors: Use venv or --user flag instead of --break-system-packages.
DMG creation fails: Ensure Whats.app is in dist/ and paths are correct.


Design by 3995 Hz
Proudly presented by Musimanda
