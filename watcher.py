import subprocess
import threading
import time

class X11Watcher:
    def __init__(self, history, on_change=None, poll_interval=0.5):
        self.history = history
        self.on_change = on_change
        self.poll_interval = poll_interval
        self._last_value = None
        self._running = False

    def _get_clipboard(self):
        try:
            result = subprocess.run(
                ["xclip", "-selection", "clipboard", "-o"],
                capture_output=True, text=True, timeout=1
            )
            return result.stdout
        except Exception:
            return None

    def _loop(self):
        while self._running:
            current = self._get_clipboard()
            if current and current != self._last_value:
                self._last_value = current
                self.history.add(current)
                if self.on_change:
                    self.on_change()
            time.sleep(self.poll_interval)

    def start(self):
        self._running = True
        thread = threading.Thread(target=self._loop, daemon=True)
        thread.start()

    def stop(self):
        self._running = False