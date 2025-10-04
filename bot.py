from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "8285404814:AAEjJgHYcgW_11EbKzIfHmRMBSFGsAEW5r0"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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

@dp.message_handler(lambda message: any(k in message.text.lower() for k in KEYWORDS))
async def send_playlist_info(message: types.Message):
    await message.reply(REPLY)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
