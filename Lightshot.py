"""
Lightshot Pro v2.8.0 - Modern ttkbootstrap UI
Professional Screenshot Editor (Windows)
Tray Icon | Capture Overlay | Editor | Magnifier | Snap Guides | Modern Theme
"""

import os
import time
import threading
import ctypes
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFilter
import keyboard
import pystray
from pystray import MenuItem as item
from plyer import notification

# ================= DPI FIX =================
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# ================= CONFIG =================
SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

SNAP_DIST = 8
MAX_UNDO = 30
LAST_IMAGE_PATH = None

# ================= GLOBAL =================
start_x = start_y = end_x = end_y = 0
current_tool = "arrow"
current_color = "#ff0000"
pen_width = 3
undo_stack, redo_stack = [], []
is_capturing = False
current_theme = "dark"
tray_icon = None

# ================= UTILS =================
def timestamp():
    return time.strftime("shot_%Y%m%d_%H%M%S.png")

def push_undo(img):
    undo_stack.append(img.copy())
    if len(undo_stack) > MAX_UNDO:
        undo_stack.pop(0)
    redo_stack.clear()

def snap(val, targets):
    for t in targets:
        if abs(val - t) <= SNAP_DIST:
            return t
    return val

# ================= MAGNIFIER =================
def create_magnifier(root):
    mag = tk.Toplevel(root)
    mag.overrideredirect(True)
    mag.attributes("-topmost", True)
    canvas = tk.Canvas(mag, width=140, height=140)
    canvas.pack()
    return mag, canvas

# ================= SCREEN CAPTURE =================
def start_capture():
    global is_capturing, start_x, start_y, end_x, end_y
    if is_capturing:
        return
    is_capturing = True

    overlay = tk.Toplevel()
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-alpha", 0.25)
    overlay.attributes("-topmost", True)
    overlay.configure(bg="black" if current_theme=="dark" else "white")

    canvas = tk.Canvas(overlay, cursor="cross")
    canvas.pack(fill="both", expand=True)

    magnifier, mag_canvas = create_magnifier(overlay)
    rect = None

    def cancel(e=None):
        global is_capturing
        magnifier.destroy()
        overlay.destroy()
        is_capturing = False

    overlay.bind("<Escape>", cancel)

    def move_mag(e):
        x, y = e.x_root, e.y_root
        magnifier.geometry(f"+{x+20}+{y+20}")
        img = ImageGrab.grab(bbox=(x-20, y-20, x+20, y+20))
        img = img.resize((140, 140), Image.NEAREST)
        tk_img = ImageTk.PhotoImage(img)
        mag_canvas.delete("all")
        mag_canvas.create_image(0, 0, anchor="nw", image=tk_img)
        mag_canvas.image = tk_img

    def down(e):
        nonlocal rect
        global start_x, start_y
        start_x, start_y = e.x, e.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y,
                                       outline="#00ff00", width=2)

    def move(e):
        move_mag(e)
        if rect:
            canvas.coords(rect, start_x, start_y, e.x, e.y)

    def up(e):
        global end_x, end_y, is_capturing
        end_x, end_y = e.x, e.y
        magnifier.destroy()
        overlay.destroy()
        is_capturing = False
        capture_area_single_window()

    canvas.bind("<Motion>", move)
    canvas.bind("<ButtonPress-1>", down)
    canvas.bind("<B1-Motion>", move)
    canvas.bind("<ButtonRelease-1>", up)

# ================= CAPTURE AREA =================
def capture_area_single_window():
    global LAST_IMAGE_PATH
    time.sleep(0.05)
    x1, y1 = min(start_x, end_x), min(start_y, end_y)
    x2, y2 = max(start_x, end_x), max(start_y, end_y)
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    LAST_IMAGE_PATH = os.path.join(SCREENSHOT_DIR, timestamp())
    img.save(LAST_IMAGE_PATH)

    open_editor_single_window(img)

# ================= EDITOR =================
def open_editor_single_window(img):
    global current_tool, current_color

    for widget in app.winfo_children():
        widget.destroy()

    app.title("Lightshot Editor")
    draw = ImageDraw.Draw(img)
    push_undo(img)

    canvas = tk.Canvas(app, bg="#111" if current_theme=="dark" else "#eee", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    tk_img = ImageTk.PhotoImage(img)
    img_id = canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img

    start = None
    w, h = img.width, img.height

    def refresh():
        canvas.image = ImageTk.PhotoImage(img)
        canvas.itemconfig(img_id, image=canvas.image)

    def undo():
        if len(undo_stack) > 1:
            redo_stack.append(undo_stack.pop())
            img.paste(undo_stack[-1])
            refresh()

    def redo():
        if redo_stack:
            state = redo_stack.pop()
            undo_stack.append(state)
            img.paste(state)
            refresh()

    def color_pick():
        global current_color
        c = colorchooser.askcolor()[1]
        if c:
            current_color = c

    def save():
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=timestamp(),
            filetypes=[("PNG Image", "*.png")]
        )
        if path:
            img.save(path)
            notification.notify(title="Lightshot Pro", message=f"Saved: {os.path.basename(path)}")

    def mouse_down(e):
        nonlocal start
        start = (e.x, e.y)
        push_undo(img)

    def mouse_up(e):
        nonlocal start
        if not start:
            return
        x1, y1 = start
        x2, y2 = e.x, e.y

        x2 = snap(x2, [0, w//2, w])
        y2 = snap(y2, [0, h//2, h])

        if current_tool == "arrow":
            draw.line((x1, y1, x2, y2), fill=current_color, width=pen_width)
            draw.polygon([(x2, y2), (x2-12, y2-6), (x2-12, y2+6)], fill=current_color)
        elif current_tool == "rect":
            draw.rectangle((x1, y1, x2, y2), outline=current_color, width=3)
        elif current_tool == "blur":
            region = img.crop((min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)))
            region = region.filter(ImageFilter.BoxBlur(8))
            img.paste(region, (min(x1,x2), min(y1,y2)))

        refresh()
        start = None

    canvas.bind("<ButtonPress-1>", mouse_down)
    canvas.bind("<ButtonRelease-1>", mouse_up)

    # ================= Toolbar =================
    bar = tb.Frame(app, bootstyle="dark", height=50)
    bar.pack(fill="x")

    def tool(t):
        global current_tool
        current_tool = t
        for b in bar.winfo_children():
            b.configure(bootstyle="secondary")
        buttons[t].configure(bootstyle="success")  # highlight active

    buttons = {}
    for t, icon in [("arrow", "➤"), ("rect", "▭"), ("blur", "◌")]:
        b = tb.Button(bar, text=icon, bootstyle="secondary", width=4, command=lambda x=t: tool(x))
        b.pack(side=LEFT, padx=2, pady=5)
        buttons[t] = b
    buttons[current_tool].configure(bootstyle="success")

    tb.Button(bar, text="🎨", bootstyle="info", width=4, command=color_pick).pack(side=LEFT, padx=2)
    tb.Button(bar, text="↩", bootstyle="warning", width=4, command=undo).pack(side=LEFT, padx=2)
    tb.Button(bar, text="↪", bootstyle="warning", width=4, command=redo).pack(side=LEFT, padx=2)
    tb.Button(bar, text="💾", bootstyle="primary", width=4, command=save).pack(side=RIGHT, padx=2)
    tb.Button(bar, text="🏠", bootstyle="secondary", width=4, command=build_main_ui).pack(side=RIGHT, padx=2)

# ================= MAIN UI =================
def build_main_ui():
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Lightshot Pro")
    app.geometry("680x550")
    app.resizable(False, False)

    # ---------------- Header Section ----------------
    tb.Label(app, text="Lightshot Pro", font=("Segoe UI", 22, "bold")).pack(pady=(10, 2))
    tb.Label(app, text="Fast, Modern & Professional Screenshot Tool", font=("Segoe UI", 10, "italic"), foreground="#9ca3af").pack(pady=(0, 10))

    # ---------------- Features / About Section ----------------
    row1 = tb.Labelframe(app, text="📌 Key Features & About Developer", padding=10)
    row1.pack(fill="x", padx=10, pady=6)

    features_text = (
        "✨ Key Features & How to Use:\n"
        "- 📸 Fast & customizable screenshot capture: Use the 'Capture Now' button or press 'PrintScreen' key.\n"
        "- 🖌 Single-window editor: Draw arrows, rectangles, or blur sensitive information instantly.\n"
        "- 🔍 Magnifier & snap guides: Helps you select precise areas quickly.\n"
        "- ↩ Undo / ↪ Redo & color picker: Easily correct mistakes or change annotation colors.\n"
        "- 🖥 Tray Icon Use Case:\n"
        "    • Minimize the app to the tray and keep it running in the background.\n"
        "    • Right-click the tray icon for quick actions: Capture Screenshot, Toggle Theme, Exit.\n"
        "    • Double-click the tray icon to start a capture immediately without opening the main window.\n"
        "- ⚡ Hotkeys: Press 'PrintScreen' to instantly capture your screen.\n"
        "\n"
        "👨‍💻 About Developer:\n"
        "Developed by Mate Technologies\n"
        "Contact: rogermodu@gmail.com\n"
        "Website: https://github.com/rogers-cyber\n"
        "License: Free to use for personal projects"
    )

    features_label = tb.Label(
        row1,
        text=features_text,
        font=("Segoe UI", 10),
        bootstyle="light",
        justify=LEFT,
        anchor="w",
        padding=10,
        wraplength=680
    )
    features_label.pack(pady=(0, 15), fill=X)

    # ---------------- Action Section ----------------
    row2 = tb.Labelframe(app, text="📌 Actions", padding=10)
    row2.pack(fill="x", padx=10, pady=6)

    action_frame = tb.Frame(row2)
    action_frame.pack(pady=5, fill=X)

    # Place buttons in a row
    tb.Button(
        action_frame,
        text="📸 Capture Now",
        bootstyle="success",
        width=18,
        command=lambda: app.after(0, start_capture)
    ).pack(side=LEFT, padx=5, pady=5)

    tb.Button(
        action_frame,
        text="🖼 Open Last Screenshot",
        bootstyle="info",
        width=25,
        command=open_last_editor
    ).pack(side=LEFT, padx=5, pady=5)

    tb.Button(
        action_frame,
        text="⚙ Settings",
        bootstyle="secondary",
        width=15,
        command=open_settings
    ).pack(side=LEFT, padx=5, pady=5)

    tb.Button(
        action_frame,
        text="✖ Exit",
        bootstyle="danger",
        width=10,
        command=app.quit
    ).pack(side=LEFT, padx=5, pady=5)

# ================= OPEN LAST =================
def open_last_editor():
    if LAST_IMAGE_PATH and os.path.exists(LAST_IMAGE_PATH):
        img = Image.open(LAST_IMAGE_PATH)
        open_editor_single_window(img)
    else:
        notification.notify(title="Lightshot Pro", message="No previous screenshot available.")

# ================= SETTINGS =================
def open_settings():
    notification.notify(title="Lightshot Pro", message="Settings placeholder")

# ================= TRAY =================
def setup_tray():
    global tray_icon
    img = Image.new("RGB", (64, 64), "black")
    d = ImageDraw.Draw(img)
    d.rectangle((16,16,48,48), outline="white", width=3)

    def on_quit(icon, item):
        icon.stop()
        app.quit()

    def on_capture(icon, item):
        app.after(0, start_capture)

    def toggle_theme(icon, item):
        global current_theme
        current_theme = "light" if current_theme=="dark" else "dark"
        notification.notify(title="Lightshot Pro", message=f"{current_theme.title()} theme applied")

    tray_icon = pystray.Icon("Lightshot", img, "Lightshot", menu=(
        item("Screenshot (PrintScreen)", on_capture),
        item("Toggle Theme", toggle_theme),
        item("Exit", on_quit)
    ))
    tray_icon.run_detached()
    tray_icon.visible = True

threading.Thread(target=setup_tray, daemon=True).start()

app = tb.Window(themename="darkly")

# ================= MINIMIZE TO TRAY =================
def on_minimize(event):
    app.withdraw()
    if tray_icon:
        notification.notify(title="Lightshot Pro", message="App minimized to tray")
app.bind("<Unmap>", on_minimize)

# ================= START =================

build_main_ui()
keyboard.add_hotkey("print screen", lambda: app.after(0, start_capture))
app.mainloop()
