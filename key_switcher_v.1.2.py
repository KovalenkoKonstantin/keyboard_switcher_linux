import subprocess
import logging
import os
import time
import pyautogui
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key

logging.basicConfig(filename="keyboard_switcher.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Функция для создания и настройки systemd сервиса
def create_systemd_service():
    user = os.getenv("USER")  # Получаем имя текущего пользователя
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
        # Записываем файл сервиса
        with open("keyboard_switcher.service", "w") as f:
            f.write(service_content)
        # Перемещаем файл в нужную директорию
        subprocess.run(["sudo", "mv", "keyboard_switcher.service", service_path])
        subprocess.run(["sudo", "systemctl", "enable", "keyboard_switcher.service"])
        subprocess.run(["sudo", "systemctl", "start", "keyboard_switcher.service"])
        logging.info("Systemd service created and started successfully.")
    except Exception as e:
        logging.error(f"Failed to create systemd service: {e}")

# Функция для переключения раскладки клавиатуры
def switch_layout():
    try:
        # Получаем текущую раскладку клавиатуры
        current_layout = subprocess.getoutput("setxkbmap -query | grep layout | awk '{print $2}'")
        # Переключаем раскладку с английской на русскую и наоборот
        new_layout = 'ru' if current_layout == 'us' else 'us'
        subprocess.run(['setxkbmap', '-layout', new_layout])
        logging.info(f"Switched layout to {new_layout}")
    except Exception as e:
        logging.error(f"Error switching layout: {e}")

# Функция для преобразования последнего слова с учётом соответствия раскладок
def convert_last_word():
    pyautogui.hotkey('ctrl', 'shift', 'left')  # Выбираем последнее слово
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'x')  # Вырезаем выбранное слово
    time.sleep(0.1)
    
    # Получаем вырезанное слово из буфера обмена
    word = pyperclip.paste()  
    # Преобразуем слово в соответствии с русской раскладкой
    converted_word = convert_word_layout(word)
    
    # Копируем преобразованное слово обратно в буфер обмена
    pyperclip.copy(converted_word)  
    # Вставляем преобразованное слово
    pyautogui.hotkey('ctrl', 'v')  
    logging.info("Converted last word layout")

# Функция для конвертации символов на основе соответствия раскладок
def convert_word_layout(word):
    # Создаём таблицу соответствий для русской и английской раскладок
    conversion_map = str.maketrans(
        "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",  # Английские буквы
        "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"  # Русские буквы
    )
    
    # Используем регулярные выражения для замены только букв, оставляя другие символы неизменными
    return re.sub(r'[a-zA-Zа-яА-Я]', lambda match: match.group(0).translate(conversion_map), word)

# Обработчик нажатий клавиш
def on_press(key):
    try:
        # Когда нажата клавиша Pause
        if key == keyboard.Key.pause:
            # Двигаем курсор на одно слово влево для выделения последнего слова
            pyautogui.hotkey('ctrl', 'left')
            time.sleep(0.1)
            
            # Проверяем, стоит ли курсор перед пробелом
            pyautogui.press('left')  # Двигаем курсор влево для проверки пробела
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'right')  # Двигаем курсор обратно вправо
            
            # Если после курсора пробел, просто меняем раскладку
            if pyautogui.typewrite(" "):  # Если обнаружен пробел
                switch_layout()
            else:
                # Иначе конвертируем последнее слово
                convert_last_word()
    except AttributeError:
        logging.error("Unhandled key press error")

# Функция для начала прослушивания клавиш
def start_listener():
    logging.info("Keyboard Switcher started")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Главная функция
if __name__ == "__main__":
    # Создаём и настраиваем systemd сервис
    create_systemd_service()
    # Запускаем слушатель клавиш
    start_listener()
