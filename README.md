# Cliplin

A lightweight clipboard history manager for Linux — inspired by [Clippy](https://github.com/notpushkin/clippy) on macOS.

Cliplin sits quietly in your system tray and keeps track of your last 30 clipboard entries, most-recently-used first, so you can quickly get back something you copied a few steps ago.

## Features

- 📋 Keeps your last **30 clipboard entries** (text only)
- 🔝 **Most-recently-used ordering** — re-copying an existing entry moves it to the top instead of duplicating it
- 🖱️ **System tray icon** with a click-to-copy dropdown menu
- 💾 **Persistent history** — survives restarts (stored locally, never sent anywhere)
- 🚀 **Starts automatically on login**
- 🧹 One-click **Clear History**

## Screenshots

> _Add a screenshot of the tray menu here, e.g. `![Cliplin tray menu](docs/screenshot.png)`_

## Requirements

Cliplin currently supports **X11-based Linux distributions** (Debian, Ubuntu, Linux Mint, Pop!_OS, and derivatives). Wayland support is not yet implemented — see [Roadmap](#roadmap).

The `.deb` package handles all dependencies automatically, including:
- Python 3
- `xclip`
- GTK / AppIndicator bindings (`python3-gi`, `gir1.2-ayatanaappindicator3-0.1`)

## Installation

### Option 1: Download the `.deb` package (recommended)

1. Download the latest `.deb` from the [Releases](../../releases) page.
2. Install it:
   ```bash
   sudo apt install ./cliplin_1.0.0_amd64.deb
   ```
3. Log out and back in (or reboot) — Cliplin will start automatically and appear in your system tray.

You can also launch it manually anytime from your application launcher, or run:
```bash
gtk-launch cliplin
```

### Option 2: Build from source

```bash
git clone https://github.com/<your-username>/cliplin.git
cd cliplin
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

> The `--system-site-packages` flag is required so the virtual environment can access the system-installed GTK bindings (`gi`), which cannot be installed via pip.

Make sure `xclip` and the AppIndicator GTK bindings are installed on your system first:
```bash
sudo apt install xclip python3-gi gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0
```

## Usage

- **Copy anything** as normal (Ctrl+C, right-click → Copy, etc.) — Cliplin picks it up automatically.
- **Click the tray icon** to see your last 30 copied items, most recent at the top.
- **Click any entry** to copy it back to your clipboard, ready to paste.
- **Clear History** wipes everything.
- **Quit** stops the app (it will restart automatically on your next login).

## How it works

Cliplin polls the X11 clipboard via `xclip` in a background thread, storing new entries in a local JSON file at:
```
~/.config/cliplin/history.json
```
No data ever leaves your machine.

## Uninstalling

```bash
sudo apt remove cliplin     # removes the app, keeps your history file
sudo apt purge cliplin      # removes the app and its virtual environment
```

Your clipboard history at `~/.config/cliplin/history.json` is left untouched unless you delete it manually.

## Roadmap

- [ ] Wayland support (`wl-clipboard`-based watcher)
- [ ] Flatpak package
- [ ] `.rpm` package for Fedora/openSUSE
- [ ] Search/filter in the tray menu
- [ ] Pin favorite entries
- [ ] Optional image support
- [ ] Global keyboard shortcut

## Contributing

Issues and pull requests are welcome! If you'd like to help with Wayland support, Flatpak/RPM packaging, or new features from the roadmap, feel free to open an issue first to discuss the approach.

## License

[MIT](LICENSE) — feel free to use, modify, and distribute.

## Acknowledgements

Inspired by [Clippy](https://github.com/notpushkin/clippy) for macOS. Built with [pystray](https://github.com/moses-palmer/pystray) and [Pillow](https://python-pillow.org/).