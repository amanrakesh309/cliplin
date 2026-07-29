import subprocess
from PIL import Image, ImageDraw
import pystray

def create_icon_image():
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
        self.icon = pystray.Icon(
            "clippy-linux",
            create_icon_image(),
            "Clippy Linux",
            menu=self.build_menu()
        )

    def build_menu(self):
        entries = self.history.get_all()

        if not entries:
            items = [pystray.MenuItem("No items yet", None, enabled=False)]
        else:
            items = [
                pystray.MenuItem(
                    truncate(text),
                    (lambda t: lambda icon, item: copy_to_clipboard(t))(text)
                )
                for text in entries
            ]

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Clear History", self.on_clear))
        items.append(pystray.MenuItem("Quit", self.on_quit))
        return pystray.Menu(*items)

    def refresh_menu(self):
        self.icon.menu = self.build_menu()

    def on_clear(self, icon, item):
        self.history.clear()
        self.refresh_menu()

    def on_quit(self, icon, item):
        self.icon.stop()

    def run(self):
        self.icon.run()