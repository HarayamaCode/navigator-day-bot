import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой Навигатор дня. Напиши /help, чтобы узнать, что я умею.")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — начать работу\n"
        "/help — помощь\n"
        "(Скоро добавим команды для задач и планирования)"
    )

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        raise Exception("Переменная окружения BOT_TOKEN не задана")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()

if __name__ == "__main__":
    main()
