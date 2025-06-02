from flask import Flask
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Flask-заглушка для Render
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is alive!'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, Стефания! Я помогу тебе спланировать день 💫")

# Функция запуска бота
def run_bot():
    token = os.environ["BOT_TOKEN"]
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# Запуск Flask и бота параллельно
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
