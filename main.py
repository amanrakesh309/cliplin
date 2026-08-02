import shutil
import sys

sys.path.insert(0, "/app/lib/cliplin")

from history import ClipboardHistory
from watcher import X11Watcher
from tray import ClipTray

def check_dependencies():
    if shutil.which("xclip") is None:
        print("Error: 'xclip' is not installed.")
        print("Install it with: sudo apt install xclip")
        sys.exit(1)

def main():
    check_dependencies()

    history = ClipboardHistory()
    tray = ClipTray(history)

    watcher = X11Watcher(history, on_change=tray.refresh_menu)
    watcher.start()

    tray.run()  # blocks until Quit is clicked

if __name__ == "__main__":
    main()