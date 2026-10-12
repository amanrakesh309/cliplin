import subprocess
from PIL import Image, ImageDraw
import pystray
import tkinter as tk
from tkinter import ttk
from config import ConfigManager
import os

def create_icon_image():
    # ...existing code...
    # Simple placeholder icon: a clipboard-like rectangle
    img = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([14, 8, 50, 58], outline="black", width=3)
    draw.rectangle([24, 4, 40, 14], fill="black")
    return img

def copy_to_clipboard(text: str):
    subprocess.run(
        ["xclip", "-selection", "clipboard"],
        input=text, text=True
    )

def truncate(text: str, length: int = 40) -> str:
    flat = text.replace("\n", " ")
    return flat if len(flat) <= length else flat[:length] + "…"

class ClipTray:
    def __init__(self, history):
        self.history = history
        self.config = ConfigManager()
        self.icon = pystray.Icon(
            "clippy-linux",
            create_icon_image(),
            "Clippy Linux",
            menu=self.build_menu()
        )

    def build_menu(self):
        print("Building menu...")
        entries = self.history.get_all()

        if not entries:
            items = [pystray.MenuItem("No items yet", None, enabled=False)]
        else:
            items = [
                pystray.MenuItem(
                    truncate(text),
                    (lambda t: lambda icon, item: self.on_copy(t))(text)
                )
                for text in entries
            ]

        items.append(pystray.Menu.SEPARATOR)
        
        # Settings Submenu
        settings_menu = pystray.Menu(
            pystray.MenuItem("Max Entries", self.on_max_entries_click)
        )
        items.append(pystray.MenuItem("Settings", settings_menu))
        
        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Clear History", self.on_clear))
        items.append(pystray.MenuItem("Quit", self.on_quit))
        print(f"Menu built with {len(items)} items")
        return pystray.Menu(*items)

    def on_copy(self, text):
        print(f"Copying to clipboard: {truncate(text)}")
        copy_to_clipboard(text)

    def on_max_entries_click(self, icon, item):
        # Use tkinter for a simple input dialog
        root = tk.Tk()
        root.withdraw() # Hide main window
        
        current_max = self.config.get("max_entries")
        current_boot = self.config.get("start_on_boot")
        
        dialog = tk.Toplevel(root)
        dialog.title("Settings")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="Maximum History Entries:").pack(pady=(10, 0))
        entry = tk.Entry(dialog)
        entry.insert(0, str(current_max))
        entry.pack(pady=5)
        
        boot_var = tk.BooleanVar(value=current_boot)
        tk.Checkbutton(dialog, text="Start on Login", variable=boot_var).pack(pady=10)
        
        def save_settings():
            try:
                new_max = int(entry.get())
                if new_max > 0:
                    self.config.set("max_entries", new_max)
                    self.config.set("start_on_boot", boot_var.get())
                    
                    # Trim history if new limit is smaller
                    self.history.entries = self.history.entries[:new_max]
                    self.history.save()
                    
                    # Handle autostart file
                    self.update_autostart(boot_var.get())
                    
                    dialog.destroy()
                    root.destroy()
                else:
                    tk.Label(dialog, text="Please enter a positive number", fg="red").pack()
            except ValueError:
                tk.Label(dialog, text="Invalid number", fg="red").pack()

        tk.Button(dialog, text="Save", command=save_settings).pack(pady=20)
        
        dialog.mainloop()

    def update_autostart(self, enabled):
        import shutil
        autostart_dir = os.path.expanduser("~/.config/autostart")
        dest_file = os.path.join(autostart_dir, "cliplin.desktop")
        source_file = os.path.join(os.path.dirname(__file__), "com.github.amanrakesh309.Cliplin.desktop")
        
        if enabled:
            os.makedirs(autostart_dir, exist_ok=True)
            if os.path.exists(source_file):
                shutil.copy(source_file, dest_file)
        else:
            if os.path.exists(dest_file):
                os.remove(dest_file)

    def refresh_menu(self):
        self.icon.menu = self.build_menu()

    def on_clear(self, icon, item):
        self.history.clear()
        self.refresh_menu()

    def on_quit(self, icon, item):
        self.icon.stop()

    def run(self):
        self.icon.run()