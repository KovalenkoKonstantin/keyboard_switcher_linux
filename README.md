# Keyboard Switcher for Linux

This script allows you to switch keyboard layouts (e.g., between English and Russian) using the `Pause` key.

## 📌 Requirements

- Python **3.10** or higher
- Installed `pynput` library

## 📥 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/KovalenkoKonstantin/keyboard_switcher_linux.git
   cd keyboard_switcher_linux
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

# Optional

**Enable automatic startup:
Create a systemd service to run the script at boot:**

```bash
sudo nano /etc/systemd/system/keyboard_switcher.service
```

  Add the following content:

```bash
[Unit]
Description=Keyboard Layout Switcher
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/keyboard_switcher/main_v.1.0.py
Restart=always
User=your-username

[Install]
WantedBy=multi-user.target
```

Save the file, then enable and start the service:

```bash
sudo systemctl enable keyboard_switcher.service
sudo systemctl start keyboard_switcher.service
```

## 🚀 Usage

Run the script manually with:

```bash
python3 key_switcher_v.1.0.py
```

Once running, you can switch keyboard layouts using the `Pause` key.

## 🔥 Features

✅ Automatically starts at system boot (optional, via systemd service)

✅ Runs in the background without a graphical interface

✅ Supports GNOME (can be adapted for other desktop environments, but may need tweaks for Wayland)

✅ Uses pynput to track key presses

✅ Proper error handling and status logging (logs errors for debugging)

## 🎯 Who is this for?

For **Linux** users who frequently switch keyboard layouts and want to do it with a single key.

💡 **Simplicity > Complexity** – minimal code, maximum benefit!

