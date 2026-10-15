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

def paste_to_active_window(text: str):
    # Use xdotool to simulate Ctrl+V
    # First, ensure the text is in the clipboard
    copy_to_clipboard(text)
    # Simulate Ctrl+V
    subprocess.run(["xdotool", "key", "ctrl+v"])

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
            # Clipboard items
            items = [
                pystray.MenuItem(
                    truncate(text),
                    (lambda t: lambda icon, item: self.on_copy_and_paste(t))(text)
                )
                for text in entries
            ]

        items.append(pystray.Menu.SEPARATOR)
        
        # Search Button
        items.append(pystray.MenuItem("🔍 Search History", self.on_search_click))
        
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

    def on_search_click(self, icon, item):
        root = tk.Tk()
        root.withdraw()
        
        # Create a sleek, centered search window
        dialog = tk.Toplevel(root)
        dialog.title("Cliplin Search")
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        dialog.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Make it look more like a utility bar
        dialog.configure(bg="#f0f0f0")
        
        search_frame = tk.Frame(dialog, bg="#f0f0f0")
        search_frame.pack(pady=15, padx=15, fill=tk.X)
        
        tk.Label(search_frame, text="Search Clipboard:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, font=("Arial", 11))
        search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        search_entry.focus_set()
        
        results_list = tk.Listbox(dialog, font=("Arial", 10), bd=0, highlightthickness=1)
        results_list.pack(pady=5, padx=15, expand=True, fill=tk.BOTH)
        
        def perform_search(*args):
            query = search_entry.get().lower().strip()
            results_list.delete(0, tk.END)
            if not query: 
                return
            
            all_history = self.history.get_all()
            for text in all_history:
                if query in text.lower():
                    results_list.insert(tk.END, truncate(text))

        def copy_selected(event=None):
            selection = results_list.curselection()
            if selection:
                idx = selection[0]
                query = search_entry.get().lower().strip()
                filtered = [t for t in self.history.get_all() if query in t.lower()]
                if idx < len(filtered):
                    text = filtered[idx]
                    self.on_copy_and_paste(text)
                    dialog.destroy()
                    root.destroy()

        # Bindings for a better experience
        search_entry.bind('<KeyRelease>', perform_search) # Search as you type!
        results_list.bind('<Double-1>', copy_selected)    # Double click to copy
        
        # Add a small hint
        tk.Label(dialog, text="Double-click item to copy", fg="gray", bg="#f0f0f0", font=("Arial", 8)).pack(pady=5)
        
        dialog.mainloop()

    def on_copy(self, text):
        print(f"Copying to clipboard: {truncate(text)}")
        copy_to_clipboard(text)

    def on_copy_and_paste(self, text):
        print(f"Copying and pasting: {truncate(text)}")
        paste_to_active_window(text)

    def on_max_entries_click(self, icon, item):
        # Use tkinter for a simple input dialog
        root = tk.Tk()
        root.withdraw() # Hide main window
        
        current_max = self.config.get("max_entries")
        current_boot = self.config.get("start_on_boot")
        current_theme = self.config.get("theme")
        
        dialog = tk.Toplevel(root)
        dialog.title("Settings")
        dialog.geometry("300x300")
        
        # Theme colors
        bg_color = "#333333" if current_theme == "dark" else "#f0f0f0"
        fg_color = "white" if current_theme == "dark" else "black"
        dialog.configure(bg=bg_color)
        
        tk.Label(dialog, text="Maximum History Entries:", bg=bg_color, fg=fg_color).pack(pady=(10, 0))
        entry = tk.Entry(dialog)
        entry.insert(0, str(current_max))
        entry.pack(pady=5)
        
        boot_var = tk.BooleanVar(value=current_boot)
        tk.Checkbutton(dialog, text="Start on Login", variable=boot_var, bg=bg_color, fg=fg_color, selectcolor=bg_color).pack(pady=10)
        
        theme_var = tk.StringVar(value=current_theme)
        tk.Label(dialog, text="Theme:", bg=bg_color, fg=fg_color).pack(pady=(10, 0))
        theme_menu = ttk.Combobox(dialog, textvariable=theme_var, values=["light", "dark"], state="readonly")
        theme_menu.pack(pady=5)
        
        def save_settings():
            try:
                new_max = int(entry.get())
                if new_max > 0:
                    self.config.set("max_entries", new_max)
                    self.config.set("start_on_boot", boot_var.get())
                    self.config.set("theme", theme_var.get())
                    
                    # Trim history if new limit is smaller
                    self.history.entries = self.history.entries[:new_max]
                    self.history.save()
                    
                    # Handle autostart file
                    self.update_autostart(boot_var.get())
                    
                    dialog.destroy()
                    root.destroy()
                else:
                    tk.Label(dialog, text="Please enter a positive number", fg="red", bg=bg_color).pack()
            except ValueError:
                tk.Label(dialog, text="Invalid number", fg="red", bg=bg_color).pack()

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