
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

main_menu_keyboard = [['Шутки'], ['Анекдоты'], ['Поздравления']]
back_keyboard = [['Старт'], ['Назад в меню']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выбери категорию:",
        reply_markup=ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == 'Шутки':
        context.user_data['category'] = 'jokes'
        await update.message.reply_text("Жми 'Старт', чтобы получить шутку.",
                                        reply_markup=ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True))
    elif text == 'Анекдоты':
        context.user_data['category'] = 'anekdots'
        await update.message.reply_text("Жми 'Старт', чтобы получить анекдот.",
                                        reply_markup=ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True))
    elif text == 'Поздравления':
        context.user_data['category'] = 'pozdravleniya'
        await update.message.reply_text("Жми 'Старт', чтобы получить поздравление.",
                                        reply_markup=ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True))
    elif text == 'Старт':
        category = context.user_data.get('category', None)
        if category:
            await update.message.reply_text(f"[{category}] Заглушка: тут будет контент.")
        else:
            await update.message.reply_text("Сначала выбери категорию.")
    elif text == 'Назад в меню':
        await start(update, context)
    else:
        await update.message.reply_text("Я тебя не понял. Нажми кнопку.")

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
