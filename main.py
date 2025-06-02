import os
import logging
import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from replit import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Дни недели
DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_LABELS = {
    "Понедельник": "monday",
    "Вторник": "tuesday",
    "Среда": "wednesday",
    "Четверг": "thursday",
    "Пятница": "friday",
    "Суббота": "saturday",
    "Воскресенье": "sunday",
    "Сегодня": DAY_NAMES[datetime.datetime.now().weekday()],
    "Завтра": DAY_NAMES[(datetime.datetime.now().weekday() + 1) % 7],
}

# Главное меню
MAIN_MENU = ReplyKeyboardMarkup([
    ["➕ Добавить задачу", "📋 Показать задачи"],
    ["✅ Завершить задачу", "🗑 Удалить задачу"],
    ["📅 День недели"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет, Стефания 🌸

Я — твой мягкий планировщик. Помогаю записывать важное, не забывать о нужном и спокойно держать фокус.

Вот что я умею:

➕ Добавить задачу — нажми и выбери день, потом напиши, что хочешь сделать  
📋 Показать задачи — выбери день, и я покажу, что ты запланировала  
🗑 Удалить — если задача уже неактуальна  
✅ Завершить — если ты выполнила что-то (в будущем это будет красиво сохраняться как «сделанное»)  
📅 День недели — если хочешь быстро выбрать нужный день  

Ты можешь нажимать кнопки ниже, и я всё подскажу сам 😊",
        reply_markup=MAIN_MENU
    )

# Добавление задачи
async def handle_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("На какой день добавить задачу? (Напиши или выбери)",
        reply_markup=ReplyKeyboardMarkup([
            ["Сегодня", "Завтра"],
            ["Понедельник", "Вторник", "Среда"],
            ["Четверг", "Пятница", "Суббота", "Воскресенье"]
        ], resize_keyboard=True, one_time_keyboard=True))
    context.user_data['state'] = 'awaiting_day_for_add'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get('state')

    if state == 'awaiting_day_for_add':
        day_key = DAY_LABELS.get(update.message.text)
        if not day_key:
            await update.message.reply_text("Не понял день. Попробуй снова.")
            return
        context.user_data['selected_day'] = day_key
        context.user_data['state'] = 'awaiting_task_text'
        await update.message.reply_text("Напиши задачу:", reply_markup=ReplyKeyboardRemove())

    elif state == 'awaiting_task_text':
        task = update.message.text
        day_key = context.user_data.get('selected_day')
        tasks = db.get(day_key, [])
        tasks.append(task)
        db[day_key] = tasks
        context.user_data.clear()
        await update.message.reply_text("Задача добавлена!", reply_markup=MAIN_MENU)

    elif state == 'awaiting_day_for_view':
        day_key = DAY_LABELS.get(update.message.text)
        if not day_key:
            await update.message.reply_text("Не понял день. Попробуй снова.")
            return
        tasks = db.get(day_key, [])
        if not tasks:
            await update.message.reply_text("На этот день пока ничего нет.", reply_markup=MAIN_MENU)
        else:
            text = f"Задачи на {update.message.text}:\n" + '\n'.join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
            await update.message.reply_text(text, reply_markup=MAIN_MENU)
        context.user_data.clear()

# Показ задач
async def handle_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Задачи на какой день показать?", reply_markup=ReplyKeyboardMarkup([
        ["Сегодня", "Завтра"],
        ["Понедельник", "Вторник", "Среда"],
        ["Четверг", "Пятница", "Суббота", "Воскресенье"]
    ], resize_keyboard=True, one_time_keyboard=True))
    context.user_data['state'] = 'awaiting_day_for_view'

def main():
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^➕ Добавить задачу$"), handle_add))
    app.add_handler(MessageHandler(filters.Regex("^📋 Показать задачи$"), handle_view))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
