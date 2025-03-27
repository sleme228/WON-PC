from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/wake", methods=["POST"])
def wake():
    os.system("wakeonlan 1C-CE-51-45-E3-10")  # Укажи свой MAC-адрес
    return "Wake-on-LAN сигнал отправлен!"

@app.route("/hibernate", methods=["POST"])
def hibernate():
    os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    return "Компьютер переведен в гибернацию!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Сервер будет слушать на порту 5000
