from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "8285404814:AAEjJgHYcgW_11EbKzIfHmRMBSFGsAEW5r0"

def handle_message(update, context):
    text = update.message.text.lower()
    keywords = [
        "как получить плейлист",
        "дайте плейлист",
        "я хочу плейлист",
        "я хочу получить плейлист"
    ]
    
    if any(phrase in text for phrase in keywords):
        update.message.reply_text(
            "Уважаемый подписчик! Все сервисы с плейлистами находятся в главном меню в разделе «Каналы» 👉 t.me/polzafre/22"
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
