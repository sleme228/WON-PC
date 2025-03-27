from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

TOKEN = "6865568473:AAHBq_sgOqJc-11OzvzjcVQE9jh2g5OMubQ"
MAC_ADDRESS = "1C-CE-51-45-E3-10"  # MAC-адрес ноутбука
WEBHOOK_URL = "https://ТВОЙ-ДОМЕН/webhook"  # URL для Webhook

# Функция для отправки Wake-on-LAN сигнала
def wake_on_lan(mac):
    os.system(f"wakeonlan {mac}")

# Функция для ввода ноутбука в гибернацию (Windows)
def hibernate_pc():
    os.system("shutdown /h")

# Главное меню с кнопками
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("💻 Включить ноутбук", callback_data="wake")],
        [InlineKeyboardButton("🌙 Ввести в гибернацию", callback_data="hibernate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Обработчик нажатий кнопок
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "wake":
        wake_on_lan(MAC_ADDRESS)
        await query.edit_message_text("✅ Сигнал на пробуждение отправлен!")
    elif query.data == "hibernate":
        hibernate_pc()
        await query.edit_message_text("💤 Компьютер переведён в режим гибернации!")

# Запуск бота через Webhook
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Бот запущен...")
app.run_webhook(listen="0.0.0.0", port=8443, webhook_url=WEBHOOK_URL)
