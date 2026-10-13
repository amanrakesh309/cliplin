# Cliplin

A lightweight clipboard history manager for Linux — inspired by [Clipy](https://github.com/clipy/clipy) on macOS.

Cliplin sits quietly in your system tray and keeps track of your last 30 clipboard entries, most-recently-used first, so you can quickly get back something you copied a few steps ago.

## Features

- 📋 Keeps your clipboard entries (text only) with **customizable history limit**
- 🔝 **Most-recently-used ordering** — re-copying an existing entry moves it to the top instead of duplicating it
- 🖱️ **System tray icon** with a click-to-copy dropdown menu
- ⚙️ **Settings Menu** to configure app behavior
- 💾 **Persistent history** — survives restarts (stored locally, never sent anywhere)
- 🚀 **Start on Login** toggle for automatic startup
- 🧹 One-click **Clear History**

## Screenshots

![Cliplin tray menu](docs/screenshot.png)

## Requirements

Cliplin currently supports **X11-based Linux distributions** (Debian, Ubuntu, Linux Mint, Pop!_OS, and derivatives). Wayland support is not yet implemented — see [Roadmap](#roadmap).

The `.deb` package handles all dependencies automatically, including:
- Python 3
- `xclip`
- `xdotool` (for automatic pasting)
- GTK / AppIndicator bindings (`python3-gi`, `gir1.2-ayatanaappindicator3-0.1`)

## Installation

### Option 1: Download the `.deb` package (recommended)
// ...existing code...
### Option 2: Build from source
// ...existing code...
> **Important**: The `--system-site-packages` flag is required so the virtual environment can access the system-installed GTK bindings (`gi`), which cannot be installed via pip.

Make sure `xclip`, `xdotool`, and the AppIndicator GTK bindings are installed on your system first:
```bash
sudo apt install xclip xdotool python3-gi gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0
```

### Option 3: Packaging for Distribution

If you want to package Cliplin for other users, you can use the following methods:

#### Creating a `.deb` package
The project includes a `build-dir/` and a `.yml` configuration for packaging. You can use `dpkg-deb` to build the package:
```bash
dpkg-deb --build build-dir cliplin_1.0.0_amd64.deb
```

#### Creating an AppImage
To create a portable AppImage, it is recommended to use `appimagetool`. 
1. Prepare an `AppDir` structure containing the Python interpreter, dependencies, and the `cliplin` source.
2. Use a tool like `python-appimage` or manually bundle the `venv` into the AppDir.
3. Run `appimagetool AppDir Cliplin.AppImage`.

## Usage
// ...existing code...


- **Copy anything** as normal (Ctrl+C, right-click → Copy, etc.) — Cliplin picks it up automatically.
- **Right-click the tray icon** to see your copied items, most recent at the top.
- **Click any entry** to copy it back to your clipboard, ready to paste.
- **Settings**: Access the settings menu from the tray icon to change the maximum number of history entries or toggle "Start on Login".
- **Clear History** wipes everything.
- **Quit** stops the app.

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

Inspired by [Clipy](https://github.com/clipy/clipy) for macOS. Built with [pystray](https://github.com/moses-palmer/pystray) and [Pillow](https://python-pillow.org/).

