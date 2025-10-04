from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "ТОКЕН_ТВОЕГО_БОТА"  # вставь сюда свой токен

KEYWORDS = [
    "как получить плейлист",
    "дайте плейлист",
    "я хочу плейлист",
    "я хочу получить плейлист"
]

REPLY_MESSAGE = (
    "Уважаемый подписчик! Все сервисы с плейлистами находятся в главном меню "
    "в разделе «Каналы» t.me/polzafre/22"
)

async def reply_to_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()
    if any(keyword in message for keyword in KEYWORDS):
        await update.message.reply_text(REPLY_MESSAGE)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_keywords))

print("Бот запущен...")
app.run_polling()
