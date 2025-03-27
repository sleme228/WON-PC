import logging
import os
import asyncio
import pyautogui
import cv2
import subprocess
import ctypes
import keyboard
import psutil
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

BOT_TOKEN = '6865568473:AAHUtOP1isIJdS__lKxfGZDuwV24x9UpBX8'  # Токен бота
CHAT_ID = '5260786785'  # Сюда свой чат id
SERVER_URL = "http://YOUR_NGROK_URL"  # Замени на адрес ngrok

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📸 Скриншот")],
        [KeyboardButton(text="🎥 Фото с вебки")],
        [KeyboardButton(text="🌐 Открыть ссылку")],
        [KeyboardButton(text="🌙 Спящий режим")],
        [KeyboardButton(text="☀️ Разбудить")],
        [KeyboardButton(text="📊 Статус загрузки")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id != int(CHAT_ID):
        return await message.answer("⛔ Доступ запрещен!")
    await message.answer("💻 Удаленное управление ПК", reply_markup=keyboard)

@dp.message(lambda message: message.text == "📸 Скриншот")
async def screenshot(message: types.Message):
    requests.post(f"{SERVER_URL}/screenshot")
    await message.answer("📸 Скриншот сделан!")

@dp.message(lambda message: message.text == "🎥 Фото с вебки")
async def webcam_photo(message: types.Message):
    requests.post(f"{SERVER_URL}/webcam")
    await message.answer("📷 Фото с вебки сделано!")

@dp.message(lambda message: message.text == "🌙 Спящий режим")
async def sleep_mode(message: types.Message):
    requests.post(f"{SERVER_URL}/sleep")
    await message.answer("💤 ПК переведен в режим сна.")

@dp.message(lambda message: message.text == "☀️ Разбудить")
async def wakeup_pc(message: types.Message):
    requests.post(f"{SERVER_URL}/wake")
    await message.answer("☀️ ПК пробужден!")

@dp.message(lambda message: message.text == "📊 Статус загрузки")
async def system_status(message: types.Message):
    response = requests.get(f"{SERVER_URL}/status")
    await message.answer(response.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
