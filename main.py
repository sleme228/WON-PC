import telebot
import requests

BOT_TOKEN = '6865568473:AAHUtOP1isIJdS__lKxfGZDuwV24x9UpBX8'  # Токен бота
CHAT_ID = '5260786785'  # Сюда свой чат id
SERVER_URL = "http://100.83.43.85:5000"  

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) != CHAT_ID:
        bot.send_message(message.chat.id, "⛔ Доступ запрещен!")
        return
    bot.send_message(message.chat.id, "💻 Удаленное управление ПК", reply_markup=keyboard())

def keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📸 Скриншот", "🎥 Фото с вебки")
    markup.add("🌐 Открыть ссылку", "🌙 Спящий режим", "☀️ Разбудить")
    markup.add("📊 Статус загрузки")
    return markup

@bot.message_handler(func=lambda message: message.text == "📸 Скриншот")
def screenshot(message):
    requests.post(f"{SERVER_URL}/screenshot")
    bot.send_message(message.chat.id, "📸 Скриншот сделан!")

@bot.message_handler(func=lambda message: message.text == "🎥 Фото с вебки")
def webcam_photo(message):
    requests.post(f"{SERVER_URL}/webcam")
    bot.send_message(message.chat.id, "📷 Фото с вебки сделано!")

@bot.message_handler(func=lambda message: message.text == "🌙 Спящий режим")
def sleep_mode(message):
    requests.post(f"{SERVER_URL}/sleep")
    bot.send_message(message.chat.id, "💤 ПК переведен в режим сна.")

@bot.message_handler(func=lambda message: message.text == "☀️ Разбудить")
def wakeup_pc(message):
    requests.post(f"{SERVER_URL}/wake")
    bot.send_message(message.chat.id, "☀️ ПК пробужден!")

@bot.message_handler(func=lambda message: message.text == "📊 Статус загрузки")
def system_status(message):
    response = requests.get(f"{SERVER_URL}/status")
    bot.send_message(message.chat.id, response.text)

bot.polling()
