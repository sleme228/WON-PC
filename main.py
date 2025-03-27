import os
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "6865568473:AAHBq_sgOqJc-11OzvzjcVQE9jh2g5OMubQ"  # Замените на ваш Telegram Bot API токен
MAC_ADDRESS = "1C-CE-51-45-E3-10"  # MAC-адрес ноутбука

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)

# Функция для отправки Wake-on-LAN сигнала
def wake_on_lan(mac):
    os.system(f"wakeonlan {mac}")

# Функция для перевода ПК в гибернацию
def hibernate_pc():
    os.system("shutdown /h")

# Команда /start
@router.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 Включить ноутбук", callback_data="wake")],
        [InlineKeyboardButton(text="🌙 Ввести в гибернацию", callback_data="hibernate")]
    ])
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@router.callback_query(lambda c: c.data in ["wake", "hibernate"])
async def button_handler(callback_query: types.CallbackQuery):
    if callback_query.data == "wake":
        wake_on_lan(MAC_ADDRESS)
        await callback_query.answer("✅ Сигнал на пробуждение отправлен!")
    elif callback_query.data == "hibernate":
        hibernate_pc()
        await callback_query.answer("💤 Компьютер переведён в режим гибернации!")
    await callback_query.message.edit_text("Операция выполнена!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
