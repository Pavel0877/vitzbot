
import json
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка контента из JSON
def load_data(filename):
    try:
        with open(f"data/{filename}", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [f"[{filename}] файл не найден или ошибка чтения"]

jokes = load_data("jokes.json")
anekdots = load_data("anekdots.json")
pozdravleniya = load_data("pozdravleniya.json")

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
        category = context.user_data.get('category')
        if category == 'jokes':
            await update.message.reply_text(random.choice(jokes))
        elif category == 'anekdots':
            await update.message.reply_text(random.choice(anekdots))
        elif category == 'pozdravleniya':
            await update.message.reply_text(random.choice(pozdravleniya))
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
