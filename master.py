from PIL import Image
from pynput.keyboard import Controller, Key, KeyCode
from gigachat import GigaChat
import threading
import customtkinter as ctk
import pystray
import pyautogui
import keyboard
import pyperclip
import json
import time
import os

JSON_FILE = "AIExplainerConfig.json"
Controll = Controller()

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stringe = json.loads(f.read())
API_TOKEN = stringe["API_TOKEN"]
client = GigaChat(credentials=API_TOKEN, verify_ssl_certs=False)

def re_api_token(data):
    try:
        with open(JSON_FILE, "r+", encoding="utf-8") as f:
            content = f.read()
            if not content:
                stringe = {}
            else:
                stringe = json.loads(content)

            stringe["API_TOKEN"] = data

            f.seek(0)
            f.truncate()
            json.dump(stringe, f, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        print("Файл AIExplainerConfig.json не найден. Создаётся новый.")
        with open(JSON_FILE, "w+", encoding="utf-8") as f:
            stringe = {"API_TOKEN": data}
            json.dump(stringe, f, ensure_ascii=False, indent=4)

def setting():
    window = ctk.CTk()
    window.title("Значение слова")
    window.geometry(f"300x100")

    Label = ctk.CTkLabel(master=window, text="Перезапустите, после ввода токена")
    Label.pack()

    Entry = ctk.CTkEntry(master=window, placeholder_text="Введите свой токен")
    Entry.pack()

    Button = ctk.CTkButton(master=window, text='Изменить', command=lambda: re_api_token(Entry.get()))
    Button.pack()
    window.mainloop()

def answer(word):
    x, y = pyautogui.position()

    textt = client.chat(f"Объясни значение слова/предложения '{word}' одним предложением.(Переведи на русский в случае необходимости)")

    window = ctk.CTk()
    window.title("Значение слова")
    window.geometry(f"300x200+{x}+{y}")
    window.attributes('-alpha', 0.8)

    label = ctk.CTkLabel(window, text=textt.choices[0].message.content, font=("Arial", 12), wraplength=300)
    label.pack(expand=True)
    window.after(15000, window.destroy)
    window.mainloop()

def exit(icon, item):
    try:
        keyboard.unhook_all()
    except:
        pass
    os._exit(0)

def explain():
    time.sleep(0.2)
    with Controll.pressed(Key.ctrl):
        Controll.tap(KeyCode.from_vk(0x43))
    time.sleep(0.2)
    text = pyperclip.paste().strip()
    if text:
        answer(text)

def main():
    menu = pystray.Menu(
        pystray.MenuItem("Настройки", setting),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Выход", exit)
    )

    image = Image.open("AIEplainer.ico")

    icon = pystray.Icon(
        name="AI Explainer",
        icon=image,
        title="AI Explainer",
        menu=menu
    )

    tray_thread = threading.Thread(target=icon.run, daemon=True)
    tray_thread.start()


    keyboard.add_hotkey('ctrl+alt+x', explain)
    print("Нажми Ctrl+Alt+X")

    try:
        while True:
            time.sleep(86400)
    except:
        pass
main()