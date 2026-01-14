# Lightshot Pro v2.8.0 – Professional Screenshot Editor & Annotation Tool (Full Source Code)

Lightshot Pro v2.8.0 is a modern Python desktop application for capturing screenshots, editing annotations, and saving or sharing images quickly.  
This repository contains the **full source code**, allowing you to customize capture behavior, editor tools, UI themes, hotkeys, tray functionality, and more for your personal or professional screenshot needs.

------------------------------------------------------------
🌟 SCREENSHOT
------------------------------------------------------------

<img alt="Lightshot Pro Main Interface" src="https://github.com/rogers-cyber/LightshotPro/blob/main/Lightshot%20Pro.jpg" />

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 📸 Fast Screenshot Capture — Use "Capture Now" button or `PrintScreen` key
- 🖌 Single-Window Editor — Draw arrows, rectangles, or blur sensitive information
- 🔍 Magnifier & Snap Guides — Helps select precise regions for accurate captures
- ↩ Undo / ↪ Redo — Easily revert or reapply changes
- 🎨 Color Picker — Choose custom annotation colors
- 💾 Save Screenshots — Save as PNG with automatic timestamp or custom filename
- 🖥 Tray Icon Support — Minimize to system tray with quick actions
    • Double-click tray icon to start capture immediately  
    • Right-click menu for Capture, Toggle Theme, Exit
- ⚡ Hotkeys — `PrintScreen` instantly starts capture
- 🌗 Light / Dark Theme — Switchable via tray or settings
- 🧵 Multithreaded Tray Setup — Background tray icon without blocking main UI
- 🛠 Fully Customizable — Modify editor tools, snap distance, pen width, or max undo stack
- 📘 Built-In About / Help — Learn key features and developer contact within the app

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:


```
git clone https://github.com/rogers-cyber/LightshotPro.git
cd LightshotPro
```

2. Install required Python packages:

```
pip install ttkbootstrap pillow pystray keyboard plyer
```

(Tkinter is included with standard Python installations.)

3. Run the application:

```
python LightshotPro.py
```

4. Optional: Build a standalone executable using PyInstaller:

```
pyinstaller --onefile --windowed LightshotPro.py
```


------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. **Capture Screenshots**:
   - Click 📸 **Capture Now** or press `PrintScreen` to select a region
   - Use the magnifier and snap guides for precise selection
   - Press `Esc` to cancel capture

2. **Edit Screenshots**:
   - Draw arrows, rectangles, or blur regions
   - Change color via 🎨 **Color Picker**
   - Undo ↩ or Redo ↪ edits
   - Save 💾 the final image to a chosen location

3. **Open Last Screenshot**:
   - Click 🖼 **Open Last Screenshot** to continue editing the most recent capture

4. **Tray Icon**:
   - Minimize app to system tray
   - Right-click for quick actions: Capture, Toggle Theme, Exit
   - Double-click to instantly capture without opening the main window

5. **Settings**:
   - Currently a placeholder; future versions may allow theme, hotkey, or editor customization

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option                     | Description
----------------------------|--------------------------------------------------
Snap Distance               | Pixels for snapping cursor to guides
Max Undo Stack              | Maximum number of undo states
Pen Width                   | Width of arrows/rectangles drawn
Current Color               | Selected annotation color
Current Tool                | Arrow / Rectangle / Blur
Theme                       | Light or Dark
Screenshot Directory        | Folder where captures are saved
Tray Icon                   | Enable background tray functionality
Hotkeys                     | `PrintScreen` triggers capture

------------------------------------------------------------
📦 OUTPUT FORMATS
------------------------------------------------------------

- PNG — Default screenshot format with timestamp
- Custom filename via Save dialog

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+
- ttkbootstrap — Modern themed UI
- Pillow (PIL) — Image capture and editing
- pystray — System tray icon and menu
- keyboard — Hotkey detection
- plyer — Desktop notifications
- Tkinter — Standard Python GUI framework
- threading / time / os / ctypes — Background tasks and DPI awareness

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- Magnifier helps with pixel-perfect selections
- Snap guides allow quick alignment to screen edges and center
- Undo/Redo stack supports up to 30 changes by default
- Tray icon runs in background without blocking main UI
- All source code is editable and fully extendable

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

Lightshot Pro v2.8.0 is maintained by **Mate Technologies**, providing a fast, professional, and modern screenshot tool.

Developer Contact: rogermodu@gmail.com  
Website: [https://github.com/rogers-cyber](https://github.com/rogers-cyber)

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as full source code.  
You may use it for personal or commercial projects.  

Redistribution, resale, or rebranding as a competing product is **not allowed**.
