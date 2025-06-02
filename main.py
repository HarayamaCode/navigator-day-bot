from flask import Flask
import threading
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Flask-заглушка
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is alive!'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, Стефания! Я помогу тебе спланировать день 🧭")

# Запуск бота с ручным event loop
def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    async def main():
        token = os.environ["BOT_TOKEN"]
        app_telegram = ApplicationBuilder().token(token).build()
        app_telegram.add_handler(CommandHandler("start", start))
        await app_telegram.run_polling(stop_signals=None)

    loop.run_until_complete(main())

# Запуск Flask и бота
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
