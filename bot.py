#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram-бот на aiogram 3.x
Реагирует на фразы вроде:
  "как получить плейлист", "дайте плейлист", "я хочу плейлист", "я хочу получить плейлист"
и отвечает фиксированным сообщением.
"""

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
import logging
import os

# ================== НАСТРОЙКИ ==================
TOKEN = "8285404814:AAEjJgHYcgW_11EbKzIfHmRMBSFGsAEW5r0"

KEYWORDS = [
    "как получить плейлист",
    "дайте плейлист",
    "я хочу плейлист",
    "я хочу получить плейлист"
]

REPLY = (
    "Уважаемый подписчик! Все сервисы с плейлистами находятся "
    "в главном меню в разделе «Каналы» — https://t.me/polzafre/22"
)

# =================================================

# Настроим логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Создаём экземпляры бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply(
        "Здравствуйте! Я бот, который помогает вам найти плейлисты. "
        "Просто напишите, например: «Как получить плейлист»."
    )

# Команда /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.reply(
        "Чтобы получить информацию о плейлистах, напишите: "
        "«Как получить плейлист» или похожие фразы."
    )

# Основной обработчик текстовых сообщений
@dp.message()
async def keyword_handler(message: types.Message):
    text = (message.text or "").lower().strip()
    if any(keyword in text for keyword in KEYWORDS):
        await message.reply(REPLY)

# Основная точка входа
async def main():
    logging.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен вручную.")
