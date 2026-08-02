import json
import os

HISTORY_FILE = os.path.expanduser("~/.config/cliplin/history.json")
MAX_ENTRIES = 30

class ClipboardHistory:
    def __init__(self):
        self.entries = []  # most recent first
        self.load()

    def add(self, text: str):
        text = text.strip()
        if not text:
            return
        if text in self.entries:
            self.entries.remove(text)  # dedup, move to top
        self.entries.insert(0, text)
        self.entries = self.entries[:MAX_ENTRIES]
        self.save()

    def get_all(self):
        return list(self.entries)

    def clear(self):
        self.entries = []
        self.save()

    def load(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.entries = []

    def save(self):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.entries, f)