import json
import os

CONFIG_FILE = os.path.expanduser("~/.config/cliplin/config.json")
DEFAULT_CONFIG = {
    "max_entries": 20,
    "start_on_boot": False,
}

class ConfigManager:
    def __init__(self):
        self.config = {}
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config = {**DEFAULT_CONFIG, **json.load(f)}
            except (json.JSONDecodeError, OSError):
                self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = DEFAULT_CONFIG.copy()

    def save(self):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save()
