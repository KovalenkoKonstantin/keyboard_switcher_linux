import subprocess
import logging
import os
from pynput import keyboard

logging.basicConfig(filename="keyboard_switcher.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def create_systemd_service():
    user = os.getenv("USER")
    service_content = f"""[Unit]
Description=Keyboard Layout Switcher
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {os.path.abspath(__file__)}
Restart=always
User={user}

[Install]
WantedBy=multi-user.target
"""
    service_path = f"/etc/systemd/system/keyboard_switcher.service"
    try:
        with open("keyboard_switcher.service", "w") as f:
            f.write(service_content)
        subprocess.run(["sudo", "mv", "keyboard_switcher.service", service_path])
        subprocess.run(["sudo", "systemctl", "enable", "keyboard_switcher.service"])
        subprocess.run(["sudo", "systemctl", "start", "keyboard_switcher.service"])
        logging.info("Systemd service created and started successfully.")
    except Exception as e:
        logging.error(f"Failed to create systemd service: {e}")

def switch_layout():
    try:
        current_layout = subprocess.getoutput("setxkbmap -query | grep layout | awk '{print $2}'")
        new_layout = 'ru' if current_layout == 'us' else 'us'
        subprocess.run(['setxkbmap', new_layout])
        logging.info(f"Switched layout to {new_layout}")
    except Exception as e:
        logging.error(f"Error switching layout: {e}")

def on_press(key):
    try:
        if key == keyboard.Key.pause:
            switch_layout()
    except AttributeError:
        logging.error("Unhandled key press error")

def start_listener():
    logging.info("Keyboard Switcher started")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    create_systemd_service()
    start_listener()