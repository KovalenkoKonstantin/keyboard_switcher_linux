import subprocess
import logging
from pynput import keyboard

# Функция логирования
logging.basicConfig(filename="keyboard_switcher.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Функция для переключения раскладки клавиатуры
def switch_layout():
    # Получаем текущую раскладку
    current_layout = subprocess.getoutput("setxkbmap -query | grep layout | awk '{print $2}'")
    
    if current_layout == 'us':
        # Если текущая раскладка английская, переключаем на русскую
        subprocess.run(['setxkbmap', 'ru'])
    else:
        # Если текущая раскладка русская, переключаем на английскую
        subprocess.run(['setxkbmap', 'us'])

# Обработчик нажатий клавиш
def on_press(key):
    try:
        if key == keyboard.Key.pause:
            switch_layout()
    except AttributeError:
        pass

# Настройка слушателя клавиш
def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    logging.info("Keyboard Switcher started")
    start_listener()