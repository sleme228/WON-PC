from flask import Flask, request, send_file
import os
import ctypes
import pyautogui
import cv2
import psutil
import subprocess
import keyboard
import threading

app = Flask(__name__)

# Делает скриншот
@app.route("/screenshot", methods=["POST"])
def screenshot():
    screenshot_path = "screenshot.png"
    pyautogui.screenshot(screenshot_path)
    return send_file(screenshot_path, mimetype="image/png")

# Фото с веб-камеры
@app.route("/webcam", methods=["POST"])
def webcam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        photo_path = "webcam.jpg"
        cv2.imwrite(photo_path, frame)
        cap.release()
        return send_file(photo_path, mimetype="image/jpeg")
    return "Ошибка при получении фото", 500

# Функция для ожидания нажатия "S" и выхода из сна
def wait_for_wake_key():
    keyboard.wait("s")  # Ожидаем нажатия "S"
    ctypes.windll.user32.mouse_event(1, 0, 0, 0, 0)  # Включаем мышь
    keyboard.unhook_all()  # Разблокируем клавиши
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome.exe", "discord.exe", "steam.exe"]:
                proc.resume()
        except psutil.NoSuchProcess:
            pass
    print("Пробуждение выполнено!")

# Перевод ПК в режим сна
@app.route("/sleep", methods=["POST"])
def sleep():
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)  # Отключаем экран
    keyboard.block_key("ctrl")
    keyboard.block_key("alt")
    keyboard.block_key("delete")
    keyboard.block_key("win")
    keyboard.block_key("s")  # Блокируем клавишу "S", чтобы избежать случайного пробуждения

    os.system("powercfg -h on")  # Включаем гибернацию
    os.system("rundll32.exe powrprof.dll,SetSuspendState Hibernate")  # Сон

    threading.Thread(target=wait_for_wake_key, daemon=True).start()  # Ждем "S" в фоне
    return "💤 ПК переведен в экономный режим."

# Пробуждение через Wake-on-LAN
@app.route("/wake", methods=["POST"])
def wake():
    mac_address = "1C-CE-51-45-E3-10"  # Замени на MAC-адрес своего ПК
    subprocess.run(["wakeonlan", mac_address])  # Отправляем Wake-on-LAN сигнал
    return "✅ Сигнал на пробуждение отправлен!"

# Получение статуса загрузки CPU и RAM
@app.route("/status", methods=["GET"])
def status():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return f"📊 Загрузка системы:\n💾 CPU: {cpu_usage}%\n🖥 RAM: {ram_usage}%"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
